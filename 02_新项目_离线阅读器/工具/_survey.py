# -*- coding: utf-8 -*-
"""勘察页面模板：给每个页面打特征标签，统计有多少种结构。"""
import os, re, io, json, collections

ROOT = r"D:\Deepseek\Fatfish Workplace\agama.buddhason.org_simp"
OUT = r"D:\Deepseek\Fatfish Workplace\新项目\_survey.tsv"

def has(s, pat):
    return 1 if re.search(pat, s, re.I | re.S) else 0

rows = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in filenames:
        if not fn.lower().endswith((".htm", ".html")):
            continue
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        try:
            c = io.open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        feat = {
            "p": rel,
            "kb": round(len(c.encode("utf-8")) / 1024, 1),
            "center": has(c, r'<div id="center"'),
            "east": has(c, r'<div id="east"'),
            "south": has(c, r'<div id="south"'),
            "north": has(c, r'<div id="north"'),
            "extjs": has(c, r"ext-all\.js|ext-base\.js"),
            "agama_trad": has(c, r'class="agama trad"'),
            "nikaya_trad": has(c, r'class="nikaya trad"'),
            "comp_trad": has(c, r'class="comp trad"'),
            "plain_trad": has(c, r'<div class="trad"'),
            "plain_simp": has(c, r'<div class="simp"'),
            "simp_any": has(c, r'class="[^"]*simp"'),
            "title": has(c, r"<title>"),
            "txt_trad": has(c, r"莊春江"),
        }
        if rel.startswith("book/"):
            feat["tpl"] = "book"
        elif rel.startswith("note/"):
            feat["tpl"] = "note"
        elif rel.startswith("SN/") or rel.startswith("AN/") or rel.startswith("SA/") or rel.startswith("MA/") or rel.startswith("DA/") or rel.startswith("MN/") or rel.startswith("DN/") or rel.startswith("AA/") or rel.startswith("Ud/") or rel.startswith("It/"):
            feat["tpl"] = "nikaya"
        elif "/" not in rel:
            feat["tpl"] = "root"
        else:
            feat["tpl"] = "small"
        rows.append(feat)

# 组合特征分组
key = lambda r: (r["tpl"], r["center"], r["east"], r["south"], r["agama_trad"], r["nikaya_trad"], r["comp_trad"], r["plain_trad"], r["extjs"])
groups = collections.Counter(key(r) for r in rows)
print("pages", len(rows))
hdr = ("tpl center east south agama nikaya comp plainT extjs")
print(hdr)
for k, v in groups.most_common():
    print("%-8s %d %d %d %d %d %d %d %d  -> %d" % (k + (v,)))

# 输出每个 tpl 的样例
with io.open(OUT, "w", encoding="utf-8") as f:
    cols = ["p", "tpl", "kb", "center", "east", "south", "north", "extjs", "agama_trad", "nikaya_trad", "comp_trad", "plain_trad", "plain_simp", "simp_any", "title", "txt_trad"]
    f.write("\t".join(cols) + "\n")
    for r in rows:
        f.write("\t".join(str(r[c]) for c in cols) + "\n")
print("wrote", OUT)

