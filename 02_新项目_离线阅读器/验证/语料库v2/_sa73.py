# -*- coding: utf-8 -*-
import re, io, os

D = os.path.dirname(os.path.abspath(__file__))
sa = io.open(os.path.join(D, "SA_杂阿含全经.html"), encoding="utf-8").read()
i = sa.find("id='SA__73'")
j = sa.find("</article>", i)
seg = sa[i:j]
print("SA.73 段落含：增壹阿含 =", "增壹阿含" in seg, "| 相應部 =", "相應部" in seg, "| 別譯 =", "別譯" in seg)
print(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", seg))[:260])

other = io.open(os.path.join(D, "其他文本.html"), encoding="utf-8").read()
print()
print("其他文本含「增壹阿含25品4經」:", "增壹阿含25品4經" in other)

