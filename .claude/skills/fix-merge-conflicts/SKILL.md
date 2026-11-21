---
name: fix-merge-conflicts
description: Resolve git merge conflicts after pulling work done on the other machine (the user codes from two PCs). Use when the user says "merge errors", "merge conflict", "conflict", "diverged", "can't pull", "GitHub Desktop says resolve conflicts", or shows the "Use the modified file from main / origin/main" choice. Claude fixes the files; the user commits and pushes in GitHub Desktop.
---

# Fix merge conflicts (two-machine workflow)

The user works on this repo from two PCs. When one PC commits without pulling the other's
work first, `main` and `origin/main` diverge and the pull stops with conflicts.

**Never run `git commit`, `git push`, `git merge --abort`, `git reset` or `publish.bat`.** The user
does all git actions in GitHub Desktop. Claude only reads git state and edits files in the working tree.

## The rule

GitHub Desktop's "Use the modified file from main / origin/main" swaps the **whole file**. Every other
change to that file from the losing side is thrown away, not just the conflicting lines.

- **Generated file** → either side is fine; the rebuild overwrites it. Take origin/main.
- **Hand-written file** → never take a whole side. Edit only the `<<<<<<<` / `=======` / `>>>>>>>`
  blocks and normally keep both changes.

| Generated (take either side) | Hand-written (merge by hand) |
|---|---|
| `data/*.json`, `data/*.xlsx`, `data/*.csv` written by generators | `*.py`, `sql/*.sql`, `lib/`, `generators/`, `scripts/`, `tests/` |
| `html/*.html` | `docs/*.md`, `notes/*.md`, `CLAUDE.md` |
| `graphify-out/**` | `.gitignore`, `*.bat`, `.vscode/*`, `dashboard_pages.json` |

If unsure whether a `data/` file is generated, grep `generators/` and `scripts/` for its name.
Hand-edited inputs such as `data/new_products.txt` and `data/deals_kenya.csv` are **hand-written**.

## Steps

1. **See the state.**
   ```
   git status --short          # UU = still conflicted
   git log --oneline -3 HEAD; git log --oneline -3 MERGE_HEAD
   ```
   If no merge is in progress yet but the branch has diverged, preview the conflicts without touching
   anything: `git merge-tree --write-tree --name-only HEAD origin/main`.

2. **Sort the UU files** into generated and hand-written using the table above.

3. **Generated files:** take origin/main for each one.
   ```
   git checkout --theirs -- <file>
   ```
   (`--theirs` = origin/main during a pull/merge.) Don't stage them; GitHub Desktop sees the markers gone.

4. **Hand-written files:** for each conflict block:
   - Show what each side changed since the split, so you know *why* each line differs:
     `git diff $(git merge-base HEAD MERGE_HEAD) HEAD -- <file>` and `... MERGE_HEAD -- <file>`.
   - Write one version that keeps both intents (e.g. the other PC's renamed variable **and** this PC's
     new line). Only edit inside the markers; Git already merged the rest.
   - If the two sides truly contradict each other (same line changed to two different values for
     different reasons), ask the user which to keep. Don't guess.

5. **Check.**
   - No markers left: `grep -rn "^<<<<<<<\|^>>>>>>>" --include=*.py --include=*.sql --include=*.md .`
   - Python parses: `python -c "import ast;ast.parse(open('<file>',encoding='utf-8').read())"`
   - Run the tests: `python -m pytest tests -q`.

6. **Rebuild the pages** so the generated files contain both machines' code. Use the `denri` conda env
   (its path differs per PC; see CLAUDE.md) with `DENRI_LAUNCHER=1` and `PYTHONUTF8=1` so no browser opens:
   `DENRI_LAUNCHER=1 PYTHONUTF8=1 python generators/<page>.py` for each page touched by the merged
   code (or all of `main.py`'s `SCRIPTS` list in that order).

7. **Hand back.** Tell the user, in a short table, what was taken from origin/main, what was merged by
   hand (and what each side contributed), and the test result. Then say: "In GitHub Desktop: commit
   the merge, then push." Never commit for them.

## Preventing it

Tell the user this when it seems useful (not every time):

- **Starting on a PC:** Fetch → Pull in GitHub Desktop *before* editing or rebuilding anything.
- **Leaving a PC:** commit and push before switching machines.
- Rebuilds rewrite `data/` and `html/` every time, so two PCs that both rebuild without pulling
  will always conflict on those files. They're harmless (step 3), but the code files are what matter.
