# -*- coding: utf-8 -*-
import re, io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
for fn in ["SA_杂阿含全经.html", "SN_相应部全经.html"]:
    c = io.open(os.path.join(D, fn), encoding="utf-8").read()
    arts = re.findall(r"<article id='([^']+)'>", c)
    print(fn, "articles:", len(arts), "demo:", [a for a in arts if "demo" in a])
    empty = 0
    for a in arts[:99999]:
        i = c.find("<article id='%s'>" % a)
        j = c.find("</article>", i)
        seg = c[i:j]
        body = seg.split("<div class='body'>", 1)[-1]
        if len(re.sub(r"<[^>]+>", "", body).strip()) < 5:
            empty += 1
    print("  empty bodies:", empty)
    key = "SN_SN0530" if "SN" in fn else "SA_SA0001"
    i = c.find("<article id='%s'>" % key)
    j = c.find("</article>", i)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c[i:j]))
    print("  sample:", txt[:180])
