# -*- coding: utf-8 -*-
"""对比几种存储形式的体积：HTML / 纯文本 / SQLite / gzip。"""
import os, io, json, gzip, sqlite3, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
recs = [json.loads(l) for l in io.open(os.path.join(BASE, "数据", "_pages.jsonl"), encoding="utf-8")]
recs = [r for r in recs if any(b[2].strip() for b in r["blk"])]
print("pages:", len(recs))

html_all, text_all = [], []
for r in recs:
    h = "".join(b[2] for b in r["blk"])
    t = E.strip_tags(h)
    html_all.append(h)
    text_all.append(t)
html_join = "\n".join(html_all).encode("utf-8")
text_join = "\n".join(text_all).encode("utf-8")

def gz(b):
    return len(gzip.compress(b, 9, mtime=0))

print("HTML    utf8 %7.2f MB   gzip %6.2f MB" % (len(html_join)/1048576, gz(html_join)/1048576))
print("纯文本  utf8 %7.2f MB   gzip %6.2f MB" % (len(text_join)/1048576, gz(text_join)/1048576))

# SQLite：纯文本
db = os.path.join(BASE, "数据", "_test_plain.db")
if os.path.exists(db): os.remove(db)
con = sqlite3.connect(db)
con.execute("CREATE TABLE p(id TEXT PRIMARY KEY, t TEXT)")
con.executemany("INSERT INTO p VALUES(?,?)", [(r["p"], t) for r, t in zip(recs, text_all)])
con.commit(); con.close()
print("SQLite 纯文本      %7.2f MB" % (os.path.getsize(db)/1048576))

# SQLite：每页 gzip 压缩块（BLOB）
dbb = os.path.join(BASE, "数据", "_test_blob.db")
if os.path.exists(dbb): os.remove(dbb)
con = sqlite3.connect(dbb)
con.execute("CREATE TABLE p(id TEXT PRIMARY KEY, b BLOB)")
con.executemany("INSERT INTO p VALUES(?,?)", [(r["p"], gzip.compress(t.encode("utf-8"), 9, mtime=0)) for r, t in zip(recs, text_all)])
con.commit(); con.close()
print("SQLite 压缩块      %7.2f MB" % (os.path.getsize(dbb)/1048576))

# 当前做法：按栏目 JSON + gzip
tot = 0
d = os.path.join(BASE, "前端", "data", "pages")
for fn in os.listdir(d):
    tot += os.path.getsize(os.path.join(d, fn))
print("当前(JSON+gzip)   %7.2f MB" % (tot/1048576))
