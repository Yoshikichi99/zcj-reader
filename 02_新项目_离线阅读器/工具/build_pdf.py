# -*- coding: utf-8 -*-
"""生成 PDF 扩展包：7 本著作，文件名改成书名。"""
import os, io, shutil

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(BASE, "源数据", "agama.buddhason.org_simp")
OUT = os.path.join(BASE, "构建", "Windows", "dist", "PDF扩展包")
os.makedirs(OUT, exist_ok=True)

BOOKS = [
    ("book/ann/ann.pdf", "阿含經南北傳對讀摘記.pdf"),
    ("book/as/as.pdf", "阿含經故事選.pdf"),
    ("book/bb/bb.pdf", "學佛的基本認識.pdf"),
    ("book/buhis/buhis.pdf", "印度佛教思想史要略.pdf"),
    ("book/mn12/mn12.pdf", "中阿含經十二選.pdf"),
    ("book/nn20/nn20.pdf", "雜阿含經二十選.pdf"),
    ("book/tb/tb.pdf", "阿含經隨身剪輯.pdf"),
]

lines = ["PDF 扩展包", "", "文件已按书名命名；括号内为原站文件名。", ""]
for rel, name in BOOKS:
    src = os.path.join(SRC, rel.replace("/", os.sep))
    if not os.path.exists(src):
        print("缺少:", rel)
        continue
    shutil.copy2(src, os.path.join(OUT, name))
    lines.append("%s（原站 %s）" % (name, os.path.basename(rel)))
    print("copy", rel, "->", name)

lines += ["", "本包与主程序分开，不影响离线阅读器的体积。",
          "", "内容授权：CC BY-NC-SA 4.0，详见同目录 授權說明.txt。"]
io.open(os.path.join(OUT, "说明.txt"), "w", encoding="utf-8").write("\n".join(lines))

import license_note
license_note.write_notice(OUT)
total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT) if f.endswith(".pdf"))
print("PDF 包：%d 个，%.1f MB" % (len(BOOKS), total / 1048576))
