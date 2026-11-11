# -*- coding: utf-8 -*-
"""用页面模型拼出几个样例页，供人工核对。"""
import os, io, sys, json, html, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_model as M
import extract as E

OUT = os.path.join(M.BASE, "验证", "页面视图")
os.makedirs(OUT, exist_ok=True)

CSS = """
body{font-family:"Noto Serif CJK SC","Songti SC",SimSun,serif;max-width:780px;margin:0 auto;
 padding:24px 18px 80px;line-height:1.95;color:#26231f;background:#fbfaf7}
h1{font-size:22px;margin:0 0 6px}.meta{color:#7d756a;font-size:13px;margin-bottom:16px}
h2{font-size:14px;margin:22px 0 8px;color:#8a5a2b;letter-spacing:.08em}
h3{font-size:16px;margin:14px 0 6px;color:#2f6b4f}
.pali{font-family:Georgia,serif;font-size:15px;color:#4a463f}
a.n,a.l{border-bottom:1px dotted #c9a06a;text-decoration:none;color:inherit}
.idtag{font-family:system-ui,sans-serif;font-size:11px;color:#a09a90}
"""

def page_html(pid):
    m = M.page_model[pid]
    r = next((x for x in M.recs if x["p"] == pid), None)
    parts = ["<div class='idtag'>%s</div>" % html.escape(pid),
             "<h1>%s</h1>" % html.escape(m["nm"]),
             "<div class='meta'>%s %s</div>" % (html.escape(m["n"]), html.escape(m["s"]))]
    parts.append("<h2>漢譯（按原頁順序拼裝）</h2>")
    for k in m["keys"]:
        parts.append("<h3>%s</h3>" % html.escape(".".join(str(x) for x in k)))
        parts.append(M.canon[k])
    if m["pali"]:
        parts.append("<h2>巴利</h2><div class='pali'>%s</div>" % m["pali"])
    if m["cmp"]:
        parts.append("<h2>比對</h2>%s" % m["cmp"])
    body = "\n".join(parts)
    return "<!doctype html><html lang='zh-Hant'><head><meta charset='utf-8'><style>%s</style></head><body>%s</body></html>" % (CSS, body)

targets = [("SA/SA0073.htm", "样例_SA0073.html"),
           ("SA/SA0001.htm", "样例_SA0001.html"),
           ("SN/SN0530.htm", "样例_SN0530.html")]
for pid, fn in targets:
    if pid not in M.page_model:
        print("缺失", pid)
        continue
    io.open(os.path.join(OUT, fn), "w", encoding="utf-8").write(page_html(pid))
    print("写出", fn)
