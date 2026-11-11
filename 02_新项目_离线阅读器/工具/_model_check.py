# -*- coding: utf-8 -*-
"""逐部经比对：页面自己嵌的那一份 vs 语料库权威副本。"""
import os, io, sys, json, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_model as M
import extract as E

ANN = re.compile(r"\[(?:\u21dd)?[A-Za-z]{1,4}\.[\d.]+\]")

def body_only(h):
    """去掉标题行，只留正文。"""
    parts = re.split(r"<br\s*/?>", h, flags=re.I)
    return "<br>".join(parts[1:]) if len(parts) > 1 else ""

def clean2(s):
    s = ANN.sub("", s)
    out = []
    for ln in s.split("\n"):
        t = ln.strip()
        if not t:
            continue
        if re.match(r"^\d+[.\/].*(品|相應|篇|分)\]?$", t):
            continue
        out.append(re.sub(r"\s+", "", t))
    return "".join(out)

safe = 0
bad_pages = []
for pid, m in M.page_model.items():
    bad = []
    for k in m["keys"]:
        copies = M.texts.get(k, [])
        own = [h for p, h in copies if p == pid]
        if not own:
            continue
        a, b = clean2(body_only(own[0])), clean2(body_only(M.canon[k]))
        if a != b:
            i = 0
            while i < len(a) and i < len(b) and a[i] == b[i]:
                i += 1
            bad.append((k, i, len(a), len(b)))
    if bad:
        bad_pages.append((pid, len(m["keys"]), bad[:3]))
    else:
        safe += 1

print("页面总数:", len(M.page_model))
print("逐部一致:", safe)
print("有差异的页:", len(bad_pages))
for x in bad_pages[:20]:
    print("   ", x[0], x[1], x[2])

rep = ["# 页面视图逐部比对\n"]
rep.append("对每一页的每一部经，比较「页面自己嵌的副本」和「语料库权威副本」。\n")
rep.append("- 页面总数：%d" % len(M.page_model))
rep.append("- 全部一致：%d" % safe)
rep.append("- 有差异：%d" % len(bad_pages))
rep.append("\n## 差异页\n")
for pid, n, bad in bad_pages[:200]:
    rep.append("- `%s`（%d 部）" % (pid, n))
    for k, i, a, b in bad:
        rep.append("  - `%s` 位置 %d：原 %d 字 / 权威 %d 字" % (".".join(str(x) for x in k), i, a, b))
io.open(os.path.join(M.BASE, "验证", "页面视图", "逐部比对.md"), "w", encoding="utf-8").write("\n".join(rep))
print("写入 验证/页面视图/逐部比对.md")
