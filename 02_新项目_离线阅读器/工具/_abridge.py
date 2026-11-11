# -*- coding: utf-8 -*-
"""查北传页里嵌入的南传/巴利文本，相对独立页是否有「节略」。"""
import os, io, sys, json, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
recs = [json.loads(l) for l in io.open(os.path.join(BASE, "数据", "_pages.jsonl"), encoding="utf-8")]
by = {r["p"]: r for r in recs}

def nz(s):
    return re.sub(r"\s+", "", s)

def text_of(r, kind, src=None):
    out = []
    for k, s, h in r["blk"]:
        if k == kind and (src is None or s == src):
            out.append(E.strip_tags(h))
    return nz("".join(out))

# 索引
index = {}
for r in recs:
    nm, cat, pid = r["nm"], r["cat"], r["p"][:-4]
    for pat, key in ((r"相應部(\d+)相應(\d+)經", "SN"), (r"增支部(\d+)集(\d+)經", "AN"),
                     (r"中部(\d+)經", "MN"), (r"長部(\d+)經", "DN"),
                     (r"中阿含(\d+)經", "MA"), (r"長阿含(\d+)經", "DA"),
                     (r"增壹阿含(\d+)品(\d+)經", "AA")):
        m = re.match(pat, nm)
        if m:
            g = m.groups()
            if len(g) == 2:
                index[(key, int(g[0]), int(g[1]))] = pid
            else:
                index[(key, 0, int(g[0]))] = pid
            break

def expand(s):
    refs = []
    for m in re.finditer(r"(相應部|增支部)(\d+)(相應|集)(\d+(?:[,-]\d+)*)經", s):
        kind = "SN" if m.group(1) == "相應部" else "AN"
        a = int(m.group(2))
        for part in m.group(4).split(","):
            if "-" in part:
                x, y = part.split("-")
                for k in range(int(x), int(y) + 1):
                    refs.append((kind, a, k))
            else:
                refs.append((kind, a, int(part)))
    for m in re.finditer(r"(中部|長部)(\d+(?:[,-]\d+)*)經", s):
        kind = "MN" if m.group(1) == "中部" else "DN"
        for part in m.group(2).split(","):
            if "-" in part:
                x, y = part.split("-")
                for k in range(int(x), int(y) + 1):
                    refs.append((kind, 0, k))
            else:
                refs.append((kind, 0, int(part)))
    return refs

north = {"SA", "MA", "DA", "AA"}
ratios = []
low = []
pali_ratios = []
unresolved = collections.Counter()
n_pages = 0
for r in recs:
    if r["cat"] not in north or not r["s"]:
        continue
    if "律藏" in r["s"] or "大品" in r["s"]:
        unresolved["律藏"] += 1
        continue
    refs = expand(r["s"])
    if not refs:
        continue
    ids = [index.get(x) for x in refs]
    if any(i is None for i in ids):
        unresolved["引用找不到对应页"] += 1
        continue
    emb = text_of(r, "zh", "nikaya")
    if not emb:
        continue
    std = "".join(text_of(by[i + ".htm"], "zh") for i in ids)
    if not std:
        continue
    n_pages += 1
    ratio = len(emb) / len(std)
    ratios.append((ratio, r["p"], len(emb), len(std)))
    if ratio < 0.9:
        low.append((ratio, r["p"], len(emb), len(std)))
    # 巴利
    embp = text_of(r, "pali")
    stdp = "".join(text_of(by[i + ".htm"], "pali") for i in ids)
    if embp and stdp:
        pali_ratios.append((len(embp) / len(stdp), r["p"], len(embp), len(stdp)))

print("可完整解析引用的北传页:", n_pages)
print("无法解析的页:", dict(unresolved))
rs = sorted(x[0] for x in ratios)
def pct(p):
    return rs[int(len(rs) * p)] if rs else 0
print("南传嵌入/独立 字数比：min %.2f  p10 %.2f  中位 %.2f  p90 %.2f  max %.2f"
      % (min(rs), pct(.1), pct(.5), pct(.9), max(rs)))
print("比值 <0.9 的页数:", len(low))
for x in sorted(low)[:10]:
    print("   %.2f  %s  嵌入%d字 / 独立%d字" % x)
print()
if pali_ratios:
    pr = sorted(x[0] for x in pali_ratios)
    print("巴利嵌入/独立 字数比：min %.2f  p10 %.2f  中位 %.2f  p90 %.2f  max %.2f"
          % (min(pr), pr[len(pr)//10], pr[len(pr)//2], pr[len(pr)*9//10], max(pr)))
