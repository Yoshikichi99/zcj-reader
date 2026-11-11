# -*- coding: utf-8 -*-
"""生成音频扩展包：mp3 按原站标题重命名 + 可播放索引页 + 映射表。"""
import os, io, re, shutil
from lxml import html as LH

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(BASE, "源数据", "agama.buddhason.org_simp", "pa")
OUT = os.path.join(BASE, "构建", "Windows", "dist", "音频扩展包")
MP3 = os.path.join(OUT, "mp3")
os.makedirs(MP3, exist_ok=True)

doc = LH.parse(os.path.join(SRC, "index.htm")).getroot()
titles = {}
for a in doc.xpath('//a[contains(@href,".mp3")]'):
    name = os.path.basename(a.get("href"))
    ts = [" ".join(t.split()) for t in a.xpath("preceding::text()")]
    ts = [t for t in ts if t]
    text = ts[-1] if ts else ""
    if name not in titles and text:
        titles[name] = text

files = sorted([f for f in os.listdir(SRC) if f.lower().endswith(".mp3")])

def safe(name, ext=".mp3"):
    s = re.sub(r'[\\/:*?"<>|]', " ", name)
    s = re.sub(r"\s+", " ", s).strip().strip(".")
    if len(s) > 60:
        s = s[:60].rstrip()
    return (s or "未命名") + ext

used = {}
rows, mapping = [], ["音頻文件對照（新檔名 ← 原站檔名）", ""]
for f in files:
    t = titles.get(f) or os.path.splitext(f)[0]
    new = safe(t)
    base, ext = os.path.splitext(new)
    n = used.get(base, 0)
    used[base] = n + 1
    if n:
        new = "%s(%d)%s" % (base, n + 1, ext)
    shutil.copy2(os.path.join(SRC, f), os.path.join(MP3, new))
    rows.append(
        '<div class="item"><div class="t">%s</div>'
        '<div class="src">原檔名：%s</div>'
        '<audio controls preload="none" src="mp3/%s"></audio></div>' % (t, f, new)
    )
    mapping.append("%s ← %s" % (new, f))

html = """<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>禪修開示 · 音頻</title>
<style>
body{margin:0;background:#EFFFDE;font-family:Tahoma,"新細明體",SimSun,sans-serif;color:#333}
.wrap{max-width:880px;margin:0 auto;padding:20px 16px 60px}
h1{font-size:22pt;color:#525000;margin:0 0 6px}
.note{color:#666;font-size:11pt;margin-bottom:18px;line-height:1.8}
.item{border-bottom:1px solid #cfe0b8;padding:14px 0}
.item .t{font-size:15pt;margin-bottom:4px}
.item .src{font-size:10pt;color:#999;margin-bottom:8px}
audio{width:100%%;max-width:640px}
</style></head><body><div class="wrap">
<h1>禪修開示</h1>
<div class="note">共 %d 段錄音。文件已按原站標題命名，括號內為原站檔名。<br>
本包與主程序分開放置，不占離線閱讀器體積。</div>
%s
</div></body></html>""" % (len(files), "\n".join(rows))

io.open(os.path.join(OUT, "音频.html"), "w", encoding="utf-8").write(html)
io.open(os.path.join(OUT, "文件对照.txt"), "w", encoding="utf-8").write("\n".join(mapping))
total = sum(os.path.getsize(os.path.join(MP3, f)) for f in os.listdir(MP3))
print("音频包：%d 个，%.1f MB；有标题 %d/%d" % (len(files), total / 1048576, len(titles), len(files)))
