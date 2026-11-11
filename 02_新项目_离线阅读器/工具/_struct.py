# -*- coding: utf-8 -*-
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E
from lxml import html as LH

for rel in sys.argv[1:]:
    p = os.path.join(E.ROOT, rel)
    doc = LH.fromstring(io.open(p, encoding="utf-8", errors="replace").read())
    body = doc.find("body")
    print("=" * 70)
    print(rel)
    for i, ch in enumerate(body):
        tag = ch.tag if isinstance(ch.tag, str) else "?"
        txt = (ch.text_content() or "").strip().replace("\n", " ")[:60]
        cls = ch.get("class") or ""
        eid = ch.get("id") or ""
        print("  [%d] %-8s id=%-10s class=%-12s %s" % (i, tag, eid, cls, txt))
