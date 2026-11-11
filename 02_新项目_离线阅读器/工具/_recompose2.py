# -*- coding: utf-8 -*-
"""精确重组测试：去掉品名/标注后，嵌入文本是否等于独立页文本的拼接。"""
import os, io, sys, json, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _abridge as A   # 复用索引与引用展开

BASE = A.BASE
recs = A.recs
by = A.by
index = A.index
expand = A.expand

def clean(s):
    s = re.sub(r"\[[A-Z]{1,4}\.\d+(?:\.\d+)*\]", "", s)
    lines = []
    for ln in s.split("\n"):
        t = ln.strip()
        if not t:
            continue
        if re.match(r"^\d+\.\S+品$", t):
            continue
        lines.append(t)
    return re.sub(r"\s+", "", "".join(lines))

north = {"SA", "MA", "DA", "AA"}
eq = 0
diff = []
for r in recs:
    if r["cat"] not in north or not r["s"]:
        continue
    if "律藏" in r["s"] or "大品" in r["s"]:
        continue
    refs = expand(r["s"])
    ids = [index.get(x) for x in refs]
    if not refs or any(i is None for i in ids):
        continue
    emb = clean(A.text_of(r, "zh", "nikaya"))
    if not emb:
        continue
    std = clean("".join(A.text_of(by[i + ".htm"], "zh") for i in ids))
    if emb == std:
        eq += 1
    else:
        # 判断是否只是节略：嵌入是否基本是独立文本的子集
        diff.append((r["p"], len(emb), len(std), emb[:20], std[:20]))

print("可比较页数:", eq + len(diff), " 完全一致:", eq, " 不一致:", len(diff))
print()
for d in sorted(diff, key=lambda x: x[1] / max(x[2], 1))[:12]:
    print("  %-16s 嵌入%6d 独立%6d" % (d[0], d[1], d[2]))
    print("     嵌入: %s" % d[3])
    print("     独立: %s" % d[4])
