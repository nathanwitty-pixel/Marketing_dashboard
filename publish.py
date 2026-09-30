#!/usr/bin/env python3
"""
publish.py — one-click, VERIFIED publish of the dashboard to GitHub (Streamlit Cloud redeploys from main).
Spec: docs/README.md › Where changes go.

    python publish.py --dry-run          # run every check and show what would be published; changes nothing
    python publish.py "What changed"     # checks → change list → confirm (y/N) → commit + push
    python publish.py --yes "message"    # same, without the confirmation prompt

Refuses (nothing is committed) when:
  • a secret file would be committed (.env*, Google / service-account credentials, secrets*.json,
    *.pem, *.key, .streamlit/secrets.toml)                                        → exit 2
  • a check fails: every .py compiles, every shared .js and every page's inline <script> passes
    `node --check`, every *_DATA_START / *_DATA_END pair appears exactly once, dashboard_pages.json
    loads and each page it lists exists                                           → exit 1
  • this copy is behind GitHub (someone else published) — pull first              → exit 3
"""
import argparse, datetime, fnmatch, json, os, py_compile, re, shutil, subprocess, sys, tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SECRET_PATTERNS = [".env", ".env.*", "*.env", "google_credentials.json", "google_token.json",
                   "service_account*.json", "secrets*.json", "*.pem", "*.key", ".streamlit/secrets.toml"]
SKIP_DIRS = ("graphify-out/", "export/", ".git/")


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode:
        raise SystemExit(f"git {' '.join(args)} failed:\n{r.stderr.strip()}")
    return r.stdout


def changed_files(repo):
    """(status, path) for every change that `git add -A` would stage (untracked included, ignored excluded)."""
    out = []
    for line in git(repo, "status", "--porcelain", "-uall", "-z").split("\0"):
        if not line:
            continue
        st, path = line[:2], line[3:]
        out.append((st.strip() or "?", path))
    return out


def is_secret(path):
    name = path.replace("\\", "/")
    base = name.rsplit("/", 1)[-1]
    return any(fnmatch.fnmatch(base, p) or fnmatch.fnmatch(name, p) for p in SECRET_PATTERNS)


def group(path):
    p = path.replace("\\", "/")
    if p.startswith("graphify-out/"):
        return "knowledge graph (graphify)"
    if p.startswith("docs/") or p.endswith(".md"):
        return "docs"
    if p.endswith((".py", ".js", ".css", ".bat", ".toml")) or p in ("shell.html", "dashboard_pages.json", "requirements.txt"):
        return "code"
    if p.endswith(".html"):
        return "pages"
    if p.endswith((".json", ".csv", ".txt", ".xlsx")):
        return "data refresh"
    return "other"


def run_checks(repo):
    problems, notes = [], []
    tracked = [f for f in git(repo, "ls-files").splitlines()]
    untracked = [p for st, p in changed_files(repo) if st == "??"]
    files = sorted(set(f for f in tracked + untracked if not f.startswith(SKIP_DIRS) and os.path.exists(os.path.join(repo, f))))

    # 1) every .py compiles
    for f in (f for f in files if f.endswith(".py")):
        try:
            py_compile.compile(os.path.join(repo, f), doraise=True, cfile=os.path.join(tempfile.gettempdir(), "publish_pyc.tmp"))
        except py_compile.PyCompileError as e:
            problems.append(f"{f}: does not compile — {str(e).strip().splitlines()[-1]}")

    # 2) shared .js + every page's inline scripts pass node --check
    node = shutil.which("node")
    pages = [f for f in files if f.endswith(".html") and "/" not in f]
    if not node:
        notes.append("node not found — JavaScript syntax checks skipped (install Node.js to enable them)")
    else:
        tmp = tempfile.mkdtemp(prefix="publish_js_")
        jobs = [(f, os.path.join(repo, f)) for f in files if f.endswith(".js") and "/" not in f]
        for f in pages:
            src = open(os.path.join(repo, f), encoding="utf-8").read()
            inline = re.findall(r"<script(?![^>]*\bsrc=)(?![^>]*type=\"application/json\")[^>]*>(.*?)</script>", src, re.S)
            if inline:
                p = os.path.join(tmp, re.sub(r"\W+", "_", f) + ".js")
                open(p, "w", encoding="utf-8").write("\n;\n".join(inline))
                jobs.append((f + " (inline scripts)", p))
        for label, p in jobs:
            r = subprocess.run([node, "--check", p], capture_output=True, text=True, encoding="utf-8")
            if r.returncode:
                problems.append(f"{label}: JavaScript syntax error — {(r.stderr.strip().splitlines() or ['?'])[-1][:160]}")
        shutil.rmtree(tmp, ignore_errors=True)

    # 3) every *_DATA_START / *_DATA_END marker pair exactly once (the generators rely on them)
    for f in pages:
        src = open(os.path.join(repo, f), encoding="utf-8").read()
        for name in sorted(set(re.findall(r"<!-- (\w+)_START -->", src))):
            a, b = src.count(f"<!-- {name}_START -->"), src.count(f"<!-- {name}_END -->")
            if a != 1 or b != 1:
                problems.append(f"{f}: {name} markers START×{a} END×{b} (must be exactly 1 each)")

    # 4) the page list loads and every page it names exists
    mf = os.path.join(repo, "dashboard_pages.json")
    if os.path.exists(mf):
        try:
            m = json.load(open(mf, encoding="utf-8"))
            for p in m.get("pages", []):
                if not os.path.exists(os.path.join(repo, p["html"])):
                    problems.append(f"dashboard_pages.json: page '{p.get('label')}' → {p['html']} does not exist")
        except Exception as e:
            problems.append(f"dashboard_pages.json does not load — {e}")
    return problems, notes


def main():
    ap = argparse.ArgumentParser(description="Verified one-click publish to GitHub → Streamlit Cloud.")
    ap.add_argument("message", nargs="*", help="commit message (default: 'Publish YYYY-MM-DD HH:MM')")
    ap.add_argument("--dry-run", action="store_true", help="run every check and list the changes; commit nothing")
    ap.add_argument("--yes", action="store_true", help="skip the y/N confirmation")
    ap.add_argument("--repo", default=os.path.dirname(os.path.abspath(__file__)), help=argparse.SUPPRESS)
    a = ap.parse_args()
    repo = a.repo

    print("Denri dashboard · publish" + ("  (DRY RUN — nothing will be committed)" if a.dry_run else ""))
    changes = changed_files(repo)
    if not changes:
        print("Nothing to publish: this copy matches the last commit.")
        return 0

    secrets = [p for _, p in changes if is_secret(p)]
    if secrets:
        print("\n✖ REFUSED — these look like secret files and must never be pushed:")
        for p in secrets:
            print("   ", p)
        print("  Keep them out of the repo (they belong in .gitignore / Streamlit Cloud → Secrets).")
        return 2

    print("\nChecking…")
    problems, notes = run_checks(repo)
    for n in notes:
        print("  ! " + n)
    if problems:
        print(f"\n✖ {len(problems)} check(s) failed — nothing was published:")
        for p in problems:
            print("   • " + p)
        return 1
    print("  ✓ Python compiles · JavaScript syntax · data markers · page list")

    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    has_remote = bool(git(repo, "remote", check=False).strip())
    if has_remote:
        git(repo, "fetch", "--quiet", "origin", check=False)
        up = git(repo, "rev-parse", "--abbrev-ref", f"{branch}@{{u}}", check=False).strip()
        if up:
            behind, ahead = (int(x) for x in git(repo, "rev-list", "--left-right", "--count", f"{up}...HEAD").split())
            if behind:
                print(f"\n✖ REFUSED — GitHub has {behind} newer commit(s) than this copy. Pull first:  git pull --rebase")
                return 3
            print(f"  ✓ up to date with {up}")

    groups = {}
    for st, p in changes:
        groups.setdefault(group(p), []).append((st, p))
    print(f"\n{len(changes)} change(s) to publish on '{branch}':")
    for g in ("code", "pages", "docs", "data refresh", "knowledge graph (graphify)", "other"):
        if g in groups:
            print(f"  {g} ({len(groups[g])})")
            for st, p in groups[g][:25]:
                print(f"     {st:2s} {p}")
            if len(groups[g]) > 25:
                print(f"     … and {len(groups[g]) - 25} more")

    if a.dry_run:
        print("\nDry run finished — every check passed; nothing was committed or pushed.")
        return 0

    msg = " ".join(a.message).strip() or "Publish " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if not a.yes:
        if input(f"\nCommit and push these changes as “{msg}”? [y/N] ").strip().lower() not in ("y", "yes"):
            print("Cancelled — nothing was committed.")
            return 0
    git(repo, "add", "-A")
    git(repo, "commit", "-m", msg)
    if has_remote:
        git(repo, "push", "origin", branch)
        print(f"\n✓ Published to GitHub ({branch}). Streamlit Cloud redeploys from main in a minute or two.")
    else:
        print("\n✓ Committed (no remote configured, nothing pushed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
