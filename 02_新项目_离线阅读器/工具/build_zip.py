# -*- coding: utf-8 -*-
"""把前端打成 ui.zip（.gz 等已压缩文件直接存储）。"""
import os, sys, zipfile

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UI = os.path.join(BASE, "前端", "proto")
OUT = os.path.join(BASE, "构建", "Windows", "build", "ui.zip")

STORED = {".gz", ".png", ".jpg", ".jpeg", ".gif", ".zip", ".woff", ".woff2"}

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for root, dirs, files in os.walk(UI):
        dirs[:] = [d for d in dirs if not d.startswith("_")]
        for f in files:
            if f.startswith("_"):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, UI).replace("\\", "/")
            ext = os.path.splitext(f)[1].lower()
            comp = zipfile.ZIP_STORED if ext in STORED else zipfile.ZIP_DEFLATED
            z.write(full, rel, compress_type=comp)

print("ui.zip: %.2f MB" % (os.path.getsize(OUT) / 1048576))
