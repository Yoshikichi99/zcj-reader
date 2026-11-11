# -*- coding: utf-8 -*-
"""校验数据包：引用是否都能解析、拼装是否完整。"""
import os, io, sys, json, gzip, re, collections

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PKG = os.path.join(BASE, "数据", "package")

def load(name):
    p = os.path.join(PKG, name)
    return json.loads(gzip.open(p, "rt", encoding="utf-8").read())

pages = load("pages.json.gz")
pali = load("pali.json.gz")
corpus = {}
for fn in os.listdir(os.path.join(PKG, "corpus")):
    d = load(os.path.join("corpus", fn))
    series = fn.split(".")[0]
    for k, v in d.items():
        corpus[k] = v

missing_key = collections.Counter()
missing_pali = 0
bad_pages = 0
total_text = 0
for pid, rec in pages.items():
    nm, keys, ov, cmp_html, pids, cat, num = rec
    miss = [k for k in keys if k not in corpus and k not in ov]
    if miss:
        bad_pages += 1
        for k in miss[:3]:
            missing_key[k] += 1
    for h in pids:
        if h not in pali:
            missing_pali += 1
    total_text += sum(len(corpus.get(k, "")) for k in keys)

print("页面:", len(pages))
print("语料条目:", len(corpus), " 巴利段:", len(pali))
print("有缺失引用的页:", bad_pages)
print("缺失 key 样例:", list(missing_key.items())[:10])
print("缺失巴利段引用:", missing_pali)
print("页面正文总量: %.1f M 字符" % (total_text / 1e6))

# 抽查 SA/SA0073
rec = pages.get("SA/SA0073.htm")
if rec:
    nm, keys, ov, cmp_html, pids, cat, num = rec
    print("\nSA/SA0073:", nm)
    print("  keys:", keys)
    print("  overrides:", list(ov.keys()))
    print("  pali:", pids, "存在:", all(h in pali for h in pids))
    for k in keys:
        src = ov.get(k) or corpus.get(k, "")
        print("   ", k, len(src), "字")
