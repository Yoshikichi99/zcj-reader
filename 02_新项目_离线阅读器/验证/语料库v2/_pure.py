# -*- coding: utf-8 -*-
import re, io, os

D = os.path.dirname(os.path.abspath(__file__))

def check(fn, prefix):
    c = io.open(os.path.join(D, fn), encoding="utf-8").read()
    arts = re.findall(r"<article id='([^']+)'>", c)
    bad = []
    for a in arts:
        i = c.find("<article id='%s'>" % a)
        j = c.find("</article>", i)
        seg = c[i:j]
        m = re.search(r"<h2>(.*?)</h2>", seg, re.S)
        t = re.sub(r"<[^>]+>", "", m.group(1)) if m else ""
        if prefix and not t.startswith(prefix):
            bad.append((a, t[:40]))
    print(fn, "articles:", len(arts), "非%s标题:" % prefix, len(bad))
    for b in bad[:8]:
        print("   ", b)

check("SA_杂阿含全经.html", "雜阿含")
check("SN_相应部全经.html", "相應部")
check("其他文本.html", "")

