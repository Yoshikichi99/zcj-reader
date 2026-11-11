# -*- coding: utf-8 -*-
"""检查语料库拆分（标题/品/正文）有没有丢字。"""
import os, io, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E
import proto_sasn as P

bad = 0
tot = 0
for cat, items in (("SA", P.SA), ("SN", P.SN)):
    for pid, t, pin, b in items:
        r = P.by[pid + ".htm"]
        if cat == "SA":
            src = "".join(E.strip_tags(h) for k, s, h in r["blk"] if k == "zh" and s in ("agama", ""))
        else:
            src = "".join(E.strip_tags(h) for k, s, h in r["blk"] if k == "zh" and s in ("nikaya", ""))
        rebuilt = "".join([pin, t, E.strip_tags(b)])
        a = re.sub(r"\s+", "", src)
        c = re.sub(r"\s+", "", rebuilt)
        # 去掉标注差异
        a = re.sub(r"\[[A-Z]{1,4}\.\d+(?:\.\d+)*\]", "", a)
        c = re.sub(r"\[[A-Z]{1,4}\.\d+(?:\.\d+)*\]", "", c)
        tot += 1
        if a != c:
            bad += 1
            if bad <= 10:
                print("差异:", pid, len(a), len(c))
                for i in range(min(len(a), len(c))):
                    if a[i] != c[i]:
                        print("   源:", a[max(0, i - 20):i + 20])
                        print("   库:", c[max(0, i - 20):i + 20])
                        break
print("检查 %d 页，不一致 %d 页" % (tot, bad))
