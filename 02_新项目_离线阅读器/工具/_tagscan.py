# -*- coding: utf-8 -*-
"""统计正文区域里出现的标签/属性，决定清洗白名单。"""
import os, io, random, collections
from lxml import html as LH

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROOT = os.path.join(BASE, "源数据", "agama.buddhason.org_simp")
random.seed(7)

pages = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in filenames:
        if fn.lower().endswith((".htm", ".html")) and not fn.lower().endswith("_s.htm"):
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace("\\", "/")
            pages.append(rel)
random.shuffle(pages)
sample = pages[:400]

tags = collections.Counter()
attrs = collections.Counter()
classes = collections.Counter()
hrefs = collections.Counter()
onmouse = collections.Counter()

def walk(el):
    for e in el.iter():
        if not isinstance(e.tag, str):
            continue
        tags[e.tag] += 1
        for k, v in e.attrib.items():
            attrs[(e.tag, k)] += 1
            if k == "class":
                for c in v.split():
                    classes[c] += 1
            if k == "href":
                hrefs[v.split("?")[0][:60]] += 1
            if k.lower().startswith("on"):
                onmouse[(k, (v.split("(")[0]))] += 1

n = 0
for rel in sample:
    p = os.path.join(ROOT, rel)
    try:
        doc = LH.parse(p).getroot()
    except Exception:
        continue
    roots = []
    for eid in ("center", "east", "south"):
        el = doc.get_element_by_id(eid, None)
        if el is not None:
            roots.append(el)
    if not roots:
        for el in doc.xpath('//div[contains(@class,"trad")]'):
            roots.append(el)
    if not roots:
        body = doc.find("body")
        if body is not None:
            roots.append(body)
    for r in roots:
        if r is not None:
            walk(r)
            n += 1

print("pages sampled", len(sample), "roots", n)
print("\n-- tags --")
for t, c in tags.most_common(40):
    print(f"  {t:12s} {c}")
print("\n-- tag.attr --")
for (t, a), c in attrs.most_common(40):
    print(f"  {t}.{a:12s} {c}")
print("\n-- classes --")
for t, c in classes.most_common(30):
    print(f"  {t:20s} {c}")
print("\n-- href prefixes --")
for t, c in hrefs.most_common(30):
    print(f"  {t!r:45s} {c}")
print("\n-- on* handlers --")
for t, c in onmouse.most_common(20):
    print(f"  {t} {c}")
