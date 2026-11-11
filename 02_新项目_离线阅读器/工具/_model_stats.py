# -*- coding: utf-8 -*-
"""统计页面模型：纯引用可拼的比例、需要 override 的量、体积影响。"""
import os, io, sys, json, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_model as M
import extract as E
import _model_check as C

pages_total = len(M.page_model)
pure = 0
override_pages = 0
override_keys = 0
override_chars = 0
ratio_buckets = collections.Counter()

for pid, m in M.page_model.items():
    bad = []
    for k in m["keys"]:
        own = [h for p, h in M.texts.get(k, []) if p == pid]
        if not own:
            continue
        a = C.clean2(C.body_only(own[0]))
        b = C.clean2(C.body_only(M.canon[k]))
        if a != b:
            bad.append((k, len(a), len(b)))
            override_chars += len(own[0])
            ratio_buckets[round(min(len(a), len(b)) / max(len(a), len(b), 1) * 10) / 10] += 1
    if not bad:
        pure += 1
    if bad:
        override_pages += 1
        override_keys += len(bad)

print("页面总数:", pages_total)
print("纯引用可拼:", pure, "（%.1f%%）" % (pure / pages_total * 100))
print("需要 override 的页:", override_pages, "（%.1f%%）" % (override_pages / pages_total * 100))
print("override 段数:", override_keys, "字符数:", override_chars)
print("长度比分布:", dict(sorted(ratio_buckets.items())))
