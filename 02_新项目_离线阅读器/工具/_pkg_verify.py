# -*- coding: utf-8 -*-
"""完整性校验：用数据包拼出来的页面正文 / 巴利，是否与原页面一字不差。"""
import os, io, sys, json, gzip, re, collections

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PKG = os.path.join(BASE, "数据", "package")

def load(name):
    return json.loads(gzip.open(os.path.join(PKG, name), "rt", encoding="utf-8").read())

pages = load("pages.json.gz")
pali = load("pali.json.gz")
corpus = {}
for fn in os.listdir(os.path.join(PKG, "corpus")):
    d = load(os.path.join("corpus", fn))
    corpus.update(d)

recs = {r["p"]: r for r in (json.loads(l) for l in io.open(os.path.join(BASE, "数据", "_pages.jsonl"), encoding="utf-8"))}

def norm(s):
    return re.sub(r"\s+", "", s)

zh_ok = zh_bad = 0
pali_ok = pali_bad = 0
bad_zh = []
bad_pali = []

for pid, rec in pages.items():
    nm, keys, ov, cmp_html, pids, cat, num, pres = rec
    r = recs.get(pid)
    if not r:
        continue
    # 中文
    comp = "".join(pres.get(k, "") + (ov.get(k) if k in ov else corpus.get(k, "")) for k in keys)
    orig = "".join(h for kind, s, h in r["blk"] if kind == "zh")
    if norm(re.sub(r"<[^>]+>", "", comp)) == norm(re.sub(r"<[^>]+>", "", orig)):
        zh_ok += 1
    else:
        zh_bad += 1
        if len(bad_zh) < 10:
            bad_zh.append(pid)
    # 巴利
    orig_p = "".join(h for kind, s, h in r["blk"] if kind == "pali")
    if orig_p.strip():
        comp_p = "\n".join(pali[h] for h in pids)
        if norm(re.sub(r"<[^>]+>", "", comp_p)) == norm(re.sub(r"<[^>]+>", "", orig_p)):
            pali_ok += 1
        else:
            pali_bad += 1
            if len(bad_pali) < 10:
                bad_pali.append(pid)

print("页面总数:", len(pages))
print("中文正文逐字一致:", zh_ok, " 不一致:", zh_bad, bad_zh)
print("巴利逐字一致:", pali_ok, " 不一致:", pali_bad, bad_pali)
