# -*- coding: utf-8 -*-
"""诊断拼装差异：是标题差异，还是正文差异。"""
import os, io, sys, json, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_model as M
import extract as E

stats = collections.Counter()
body_bad = []
title_bad = []

for pid, m in M.page_model.items():
    r = next((x for x in M.recs if x["p"] == pid), None)
    if r is None:
        continue
    orig = M.clean("".join(E.strip_tags(h) for k, s, h in r["blk"] if k == "zh"))
    comp = M.clean("".join(E.strip_tags(M.canon[k]) for k in m["keys"] if k in M.canon))
    if orig == comp:
        stats["exact"] += 1
        continue
    i = 0
    while i < len(orig) and i < len(comp) and orig[i] == comp[i]:
        i += 1
    # 第一行长度：取原文第一个换行（clean 已去换行，用标题长度近似）
    title_len = len(M.clean(m["nm"]))
    if i < max(title_len + 40, 60):
        stats["title"] += 1
        title_bad.append((pid, i, orig[i:i + 12], comp[i:i + 12]))
    else:
        stats["body"] += 1
        body_bad.append((pid, i, len(orig), len(comp), orig[i:i + 16], comp[i:i + 16]))

print("分类:", dict(stats))
print("\n标题差异样例:")
for x in title_bad[:10]:
    print("   ", x)
print("\n正文差异样例:")
for x in body_bad[:20]:
    print("   ", x)

rep = ["# 页面视图拼装差异\n"]
rep.append("分类统计：%s\n" % dict(stats))
rep.append("## 标题差异（可接受，统一用独立页标题）\n")
for x in title_bad[:40]:
    rep.append("- `%s` 位置 %d：原「%s」/ 拼装「%s」" % x)
rep.append("\n## 正文差异（需保留原块 override）\n")
for x in body_bad[:80]:
    rep.append("- `%s` 位置 %d，原 %d 字 / 拼装 %d 字：原「%s」/ 拼装「%s」" % x)
io.open(os.path.join(M.BASE, "验证", "页面视图", "拼装差异.md"), "w", encoding="utf-8").write("\n".join(rep))
print("\n写入 验证/页面视图/拼装差异.md")
