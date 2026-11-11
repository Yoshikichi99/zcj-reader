# -*- coding: utf-8 -*-
"""巴利去重后的 override 统计与体积估算。"""
import os, io, sys, json, re, gzip, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E
import _pali as P

bykey = collections.defaultdict(list)
pages = collections.defaultdict(list)
for pid, key, txt in P.segs:
    bykey[key].append((pid, txt))
    pages[pid].append((key, txt))

canon = {k: max(v, key=lambda x: len(x[1]))[1] for k, v in bykey.items()}

def norm(s):
    return re.sub(r"\s+", "", s)

ov_pages = 0
ov_segs = 0
ov_chars = 0
for pid, lst in pages.items():
    bad = []
    for key, txt in lst:
        if key == "_pre":
            continue
        if norm(txt) != norm(canon[key]):
            bad.append(key)
            ov_chars += len(txt)
    if bad:
        ov_pages += 1
        ov_segs += len(bad)

print("巴利页数:", len(pages))
print("需 override 的页:", ov_pages, " 段:", ov_segs, " 字符:", ov_chars)
print("权威巴利字数:", sum(len(v) for v in canon.values()))

uniq = "".join(canon.values())
print("巴利权威副本 gzip: %.2f MB" % (len(gzip.compress(uniq.encode(), 9, mtime=0)) / 1048576))
