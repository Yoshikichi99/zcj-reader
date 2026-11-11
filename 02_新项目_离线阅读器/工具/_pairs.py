# -*- coding: utf-8 -*-
"""把原站页面的 trad/simp 块配对抽出来，供 JS 转换器做全量对照。"""
import os, io, sys, json, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_pairs.jsonl")
DIV_RE = re.compile(r"<div\b[^>]*>", re.I)
SCRIPT_RE = E.SCRIPT_RE
STYLE_RE = E.STYLE_RE

def class_of(tag):
    m = re.search(r'class\s*=\s*"([^"]*)"', tag) or re.search(r"class\s*=\s*'([^']*)'", tag)
    return m.group(1).split() if m else []

def find_div_end(s, start):
    depth = 1
    pos = start
    pat = re.compile(r"<(/?)div\b", re.I)
    while True:
        m = pat.search(s, pos)
        if not m:
            return -1
        depth += -1 if m.group(1) else 1
        pos = m.end()
        if depth == 0:
            j = s.find(">", m.end())
            return j + 1 if j >= 0 else -1

def text(h):
    h = re.sub(r"<br\s*/?>", "\n", h, flags=re.I)
    h = re.sub(r"<[^>]+>", "", h)
    h = html.unescape(h)
    h = h.replace("\u3000", " ")
    return re.sub(r"\s+", "", h)

pairs = []
files = E.list_files()
for rel in files:
    raw = io.open(os.path.join(E.ROOT, rel), encoding="utf-8", errors="replace").read()
    raw = raw.lstrip("\ufeff \r\n\t")
    i = raw.lower().find("<html")
    if i > 0:
        raw = raw[i:]
    pre = STYLE_RE.sub("", SCRIPT_RE.sub("", raw))
    blocks = []
    for m in DIV_RE.finditer(pre):
        cls = class_of(m.group(0))
        if not cls or "trad" not in cls and "simp" not in cls:
            continue
        end = find_div_end(pre, m.end())
        if end < 0:
            continue
        key = tuple(sorted(c for c in cls if c not in ("trad", "simp")))
        blocks.append((key, "simp" if "simp" in cls else "trad", pre[m.end():end]))
    # 同一 key 的 trad/simp 配对
    bykey = {}
    for key, kind, inner in blocks:
        bykey.setdefault(key, {})[kind] = inner
    for key, d in bykey.items():
        if "trad" in d and "simp" in d:
            t = text(d["trad"])
            s = text(d["simp"])
            if len(t) > 20:
                pairs.append({"p": rel, "k": ".".join(key) or "body", "t": t, "s": s})

with io.open(OUT, "w", encoding="utf-8") as f:
    for x in pairs:
        f.write(json.dumps(x, ensure_ascii=False) + "\n")
print("配对块:", len(pairs), "写入", OUT)
