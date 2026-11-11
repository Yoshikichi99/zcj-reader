# -*- coding: utf-8 -*-
import re, io, os

D = os.path.dirname(os.path.abspath(__file__))
c = io.open(os.path.join(D, "SN_相应部全经.html"), encoding="utf-8").read()
for m in re.finditer(r"<article id='([^']+)'>", c):
    a = m.group(1)
    i, j = m.start(), c.find("</article>", m.start())
    seg = c[i:j]
    body = seg.split("<div class='body'>", 1)[-1]
    if len(re.sub(r"<[^>]+>", "", body).strip()) < 5:
        print(a, "|", re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", seg))[:150])
