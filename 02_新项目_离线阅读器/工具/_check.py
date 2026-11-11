# -*- coding: utf-8 -*-
import sys, os, re, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E
from lxml import html as LH

for rel in sys.argv[1:]:
    path = os.path.join(E.ROOT, rel)
    rec = E.parse_page(path, rel)
    doc = LH.fromstring(io.open(path, encoding="utf-8", errors="replace").read())
    print("=" * 70)
    print(rel, "| kind:", E.classify(rel))
    for k in ("t", "nm", "sub", "n", "s", "tp", "cat", "num"):
        v = rec[k]
        print("  %-4s %s" % (k, (v[:100] if isinstance(v, str) else v)))
    print("  blocks:", [(b[0], b[1], len(b[2])) for b in rec["blk"]])
    print("  total chars:", sum(len(E.strip_tags(b[2])) for b in rec["blk"]))
    print("  html head:", rec["blk"][0][2][:200] if rec["blk"] else "(empty)")
