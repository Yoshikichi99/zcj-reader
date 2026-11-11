# -*- coding: utf-8 -*-
"""扩展包内附的授权说明：内容依 CC BY-NC-SA 4.0，需随包分发。"""
import io, os

NOTICE = """授權說明

本文所附之經文、譯文、註釋、音頻與 PDF，均由莊春江老師翻譯、整理與著述，
現由家屬決議採創用 CC 授權開放分享。

著作人：莊春江（家屬授權開放分享）
來源：https://agama.buddhason.org/
授權：創用 CC 姓名標示-非商業性-相同方式分享 4.0 國際
      https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hant

本版本僅重新命名、重新打包，未改動內容本身。
轉載或再散布時，請保留本說明、標示作者與授權並附上連結，
且不得用於商業目的；衍生作品須以相同條款分享。

本離線閱讀器為讀者自行製作之非官方版本，與原作者及家屬無隸屬或背書關係。
"""


def write_notice(out_dir):
    path = os.path.join(out_dir, "授權說明.txt")
    io.open(path, "w", encoding="utf-8").write(NOTICE)
    return path
