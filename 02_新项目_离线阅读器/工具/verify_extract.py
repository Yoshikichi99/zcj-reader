# -*- coding: utf-8 -*-
"""抽取质量体检：读 _pages.jsonl + 源文件，找异常页。"""
import sys, os, io, re, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "数据", "_pages.jsonl")
recs = [json.loads(l) for l in io.open(PATH, encoding="utf-8")]
print("records:", len(recs))

kinds = collections.Counter()
cats = collections.Counter()
chars = 0
no_zh = []
nm_empty = []
short = []
redirects = []
for r in recs:
    rel = r["p"]
    k = E.classify(rel)
    kinds[k] += 1
    cats[r["cat"] or "-"] += 1
    t = "".join(E.strip_tags(b[2]) for b in r["blk"])
    chars += len(t)
    if not t.strip():
        continue
    if k == "sutra" and not any(b[0] == "zh" for b in r["blk"]):
        no_zh.append(rel)
    if k == "sutra" and not r["nm"]:
        nm_empty.append(rel)
    try:
        size = os.path.getsize(os.path.join(E.ROOT, rel))
    except OSError:
        size = 1
    if len(t.encode("utf-8")) < size * 0.15 and size > 3000:
        short.append((rel, len(t), size))
    if "<meta" in io.open(os.path.join(E.ROOT, rel), encoding="utf-8", errors="replace").read(400).lower() and "refresh" in io.open(os.path.join(E.ROOT, rel), encoding="utf-8", errors="replace").read(400).lower():
        redirects.append(rel)

print("kinds:", dict(kinds))
print("cats:", dict(cats))
print("total chars:", chars)
print("sutra without zh block:", len(no_zh), no_zh[:20])
print("sutra without nm:", len(nm_empty), nm_empty[:20])
print("redirect stubs:", len(redirects), redirects[:20])
print("short vs file size:", len(short))
for s in short[:25]:
    print("   ", s)
