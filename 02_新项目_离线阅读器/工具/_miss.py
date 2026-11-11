# -*- coding: utf-8 -*-
import json, io, sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E
import proto_corpus as P

for cat in ("SA", "SN"):
    miss = []
    for r in P.recs:
        if r["cat"] != cat or r["num"] == 0:
            continue
        hs = "".join(h for k, s, h in r["blk"] if k == "zh")
        m = P.SN_RE.search(hs)
        if not m:
            mu = P.U_RE.search(hs[:300])
            title = mu.group(1) if mu else ""
        else:
            title = m.group(1)
        key, name = P.key_of(title)
        if not key or key[0] != cat:
            miss.append((r["p"], re.sub(r"<[^>]+>", "", title)[:50], key))
    print(cat, "未归入本系统的页:", len(miss))
    for x in miss[:12]:
        print("   ", x)
