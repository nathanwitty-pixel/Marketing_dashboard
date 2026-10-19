"""Sticky-controls checks (docs/sticky-controls.md › Checks).

    python notes/sticky_test/run.py <page.html> <bar selector> [--click SEL --read SEL]

(i)  standalone — a probe copy of the page (in html/, so relative assets load) scrolled to 3,000 px: the bar's top
     in the window (pass: 0–8 px).
(ii) embedded — a harness page with a fixed 56 px .tn-bar and the page in a srcdoc iframe (local scripts inlined, as
     streamlit_app.py does) sized to its full height; the parent scrolled 3,000 px: the bar's top in the parent's
     viewport (pass: 56–72 px).
Both report JS errors (pass: none). --click / --read: while pinned, click SEL then report the text of --read SEL
(the redraw check). Prints one JSON line per mode and exits 1 if anything fails.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HTML = os.path.join(ROOT, "html")
EDGE = os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"), "Microsoft", "Edge", "Application", "msedge.exe")
ERR_HOOK = ("<script>window.__errs=[];window.addEventListener('error',function(e){__errs.push((e.message||'error')+' @'+(e.lineno||''));});"
            "var __ce=console.error;console.error=function(){__errs.push('console.error: '+[].slice.call(arguments).join(' ').slice(0,200));__ce.apply(console,arguments);};</script>")


def js_str(s):
    return json.dumps(s)


def action_js(win, click, read, setv=None):
    """JS act(d, cb): optionally set a <select> (setv = "SEL=VALUE", fires change), click `click`, then cb(text of `read`)."""
    if not (click or setv):
        return "function act(d,cb){cb(null);}"
    js = "function act(d,cb){"
    if setv:
        sel, val = setv.split("=", 1)
        js += "var s=d.querySelector(%s);if(s){s.value=%s;s.dispatchEvent(new Event('change',{bubbles:true}));}" % (js_str(sel), js_str(val))
    if click:
        js += "var c=d.querySelector(%s);if(c){c.click();}" % js_str(click)
    js += "setTimeout(function(){var r=d.querySelector(%s);cb(r?r.textContent.replace(/\\s+/g,' ').trim():'(not found)');},700);}" % js_str(read)
    return js


def edge_dump(path):
    out = subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--virtual-time-budget=14000", "--window-size=1400,900",
                          "--dump-dom", "file:///" + path.replace("\\", "/")], capture_output=True, text=True,
                         encoding="utf-8", errors="replace", timeout=180).stdout
    m = re.search(r'<pre id="probe">(.*?)</pre>', out, re.S)
    if not m:
        return {"error": "no probe output"}
    import html as _h
    return json.loads(_h.unescape(m.group(1)))


def inline_local(page_html):
    def rep(m):
        src = m.group(1)
        if src.startswith(("http:", "https:", "//")):
            return m.group(0)
        p = os.path.normpath(os.path.join(HTML, src))
        try:
            return "<script>" + open(p, encoding="utf-8").read().replace("</script", "<\\/script") + "</script>"
        except OSError:
            return m.group(0)
    return re.sub(r'<script\s+src="([^"]+\.js)"\s*>\s*</script>', rep, page_html)


def standalone(page, sel, click, read, setv=None, at=None):
    s = open(os.path.join(HTML, page), encoding="utf-8").read()
    probe = ("<script>(function(){" + action_js("window", click, read, setv) +
             "setTimeout(function(){var at=__AT__?document.querySelector(__AT__):null;window.scrollTo({top:at?Math.round(at.getBoundingClientRect().top+window.scrollY+150):3000,behavior:'instant'});document.dispatchEvent(new Event('scroll',{bubbles:true}));"
             "setTimeout(function(){document.dispatchEvent(new Event('scroll',{bubbles:true}));},350);setTimeout(function(){var b=document.querySelector(__SEL__);var top=b?Math.round(b.getBoundingClientRect().top):null;var dbg0={sy:window.scrollY,rt:b?Math.round(b.getBoundingClientRect().top):null,t:(window.StickyControls&&StickyControls._bars[0])?StickyControls._bars[0].t:null,disp:b?getComputedStyle(b).display:null,mt:b?getComputedStyle(b).marginTop:null};"
             "act(document,function(txt){document.dispatchEvent(new Event('scroll',{bubbles:true}));setTimeout(function(){"
             "var b2=document.querySelector(__SEL__);var p=document.createElement('pre');p.id='probe';"
             "p.textContent=JSON.stringify({top:top,topAfter:b2?Math.round(b2.getBoundingClientRect().top):null,read:txt,"
             "pinned:b?b.classList.contains('sc-pinned'):null,scrollY:window.scrollY,docH:document.documentElement.scrollHeight,innerH:window.innerHeight,bars:(window.StickyControls?StickyControls._bars.map(function(x){return {t:x.t,pinned:x.pinned,box:!!x.box,h:x.el.offsetHeight};}):null),dbg0:dbg0,errors:window.__errs});document.body.appendChild(p);},300);});"
             "},500);},4000);})();</script></body>").replace("__SEL__", js_str(sel)).replace("__AT__", js_str(at) if at else "null")
    s = s.replace("<head>", "<head>" + ERR_HOOK, 1)
    j = s.rindex("</body>")
    tmp = os.path.join(HTML, "_sticky_probe.html")
    open(tmp, "w", encoding="utf-8").write(s[:j] + probe + s[j + 7:])
    try:
        return edge_dump(tmp)
    finally:
        os.remove(tmp)


def embedded(page, sel, click, read, setv=None, at=None):
    s = inline_local(open(os.path.join(HTML, page), encoding="utf-8").read())
    s = s.replace("<head>", "<head>" + ERR_HOOK, 1)
    srcdoc = s.replace("&", "&amp;").replace('"', "&quot;")
    harness = ("<!doctype html><html><head><meta charset='utf-8'><style>body{margin:0;background:#0f1117}"
               ".tn-bar{position:fixed;top:0;left:0;right:0;height:56px;background:#222;z-index:1000}"
               "iframe{display:block;width:1360px;border:0;margin-top:56px}</style></head><body>"
               "<div class='tn-bar'></div><iframe id='f' height='900' srcdoc=\"" + srcdoc + "\"></iframe>"
               "<script>(function(){var f=document.getElementById('f');" + action_js("f", click, read, setv) +
               "setTimeout(function(){var d=f.contentDocument;f.style.height=d.documentElement.scrollHeight+'px';setInterval(function(){var h=d.documentElement.scrollHeight;if(Math.abs(f.offsetHeight-h)>1)f.style.height=h+'px';},100);"
               "setTimeout(function(){f.style.height=d.documentElement.scrollHeight+'px';var at=__AT__?d.querySelector(__AT__):null;window.scrollTo({top:at?Math.round(f.getBoundingClientRect().top+window.scrollY+at.getBoundingClientRect().top-56+150):3000,behavior:'instant'});"
               "document.dispatchEvent(new Event('scroll',{bubbles:true}));"
               "setTimeout(function(){document.dispatchEvent(new Event('scroll',{bubbles:true}));},350);setTimeout(function(){var b=d.querySelector(__SEL__);var fr=f.getBoundingClientRect().top;"
               "var top=b?Math.round(fr+b.getBoundingClientRect().top):null;"
               "act(d,function(txt){f.style.height=d.documentElement.scrollHeight+'px';document.dispatchEvent(new Event('scroll',{bubbles:true}));setTimeout(function(){var b2=d.querySelector(__SEL__);"
               "var p=document.createElement('pre');p.id='probe';p.textContent=JSON.stringify({top:top,"
               "topAfter:b2?Math.round(f.getBoundingClientRect().top+b2.getBoundingClientRect().top):null,read:txt,"
               "pinned:b?b.classList.contains('sc-pinned'):null,scrollY:window.scrollY,errors:f.contentWindow.__errs});"
               "document.body.appendChild(p);},300);});},600);},600);},4500);})();</script></body></html>").replace("__SEL__", js_str(sel)).replace("__AT__", js_str(at) if at else "null")
    tmp = os.path.join(HTML, "_sticky_harness.html")
    open(tmp, "w", encoding="utf-8").write(harness)
    try:
        return edge_dump(tmp)
    finally:
        os.remove(tmp)


def main():
    a = sys.argv[1:]
    page, sel = a[0], a[1]
    click = a[a.index("--click") + 1] if "--click" in a else None
    read = a[a.index("--read") + 1] if "--read" in a else None
    setv = a[a.index("--set") + 1] if "--set" in a else None
    at = a[a.index("--at") + 1] if "--at" in a else None
    ok = True
    for mode, fn, lo, hi in (("standalone", standalone, 0, 8), ("embedded", embedded, 56, 72)):
        r = fn(page, sel, click, read, setv, at)
        top = r.get("top")
        good = top is not None and lo <= top <= hi and not r.get("errors")
        if click or setv:
            ta = r.get("topAfter")
            good = good and ta is not None and lo <= ta <= hi
        r.update({"mode": mode, "page": page, "pass": bool(good), "range": [lo, hi]})
        ok = ok and good
        print(json.dumps(r, ensure_ascii=False))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
