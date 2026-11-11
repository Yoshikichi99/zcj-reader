# -*- coding: utf-8 -*-
"""把使用说明转成简体（用项目自己的繁简表，保护 明覆 / 祇）。"""
import os, io, gzip, json

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
D = json.loads(gzip.open(os.path.join(BASE, "前端", "proto", "data", "t2s.json.gz"), "rt", encoding="utf-8").read())
PHRASES = D.get("p", [])
CHARS = dict(D.get("c", {}))
CHARS.pop("祇", None)

PROT = "\uE000"

def to_simp(s):
    out = s.replace("明覆", PROT)
    for t, c in PHRASES:
        if t in out:
            out = out.replace(t, c)
    out = "".join(CHARS.get(ch, ch) for ch in out)
    return out.replace(PROT, "明覆")

for rel in ("dist/莊春江讀經站/使用说明.txt", "dist/單文件版/使用说明.txt"):
    src = os.path.join(BASE, "构建", "Windows", rel)
    if not os.path.exists(src):
        print("missing", rel)
        continue
    text = io.open(src, encoding="utf-8").read()
    out = to_simp(text)
    dst = src.replace("使用说明.txt", "使用说明-简体.txt")
    io.open(dst, "w", encoding="utf-8").write(out)
    print("wrote", os.path.basename(os.path.dirname(dst)) + "/" + os.path.basename(dst), len(out))
