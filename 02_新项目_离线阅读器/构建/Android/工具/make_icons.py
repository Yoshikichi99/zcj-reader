# -*- coding: utf-8 -*-
"""
从项目根目录的「图标_透明.png」生成 Android 图标资源。

用法（在 构建/Android 目录下）：
  python 工具/make_icons.py

产物：
  app/src/main/res/mipmap-{m,h,xh,xxh,xxxh}dpi/ic_launcher.png           48/72/96/144/192
  app/src/main/res/mipmap-{m,h,xh,xxh,xxxh}dpi/ic_launcher_foreground.png 108/162/216/324/432
  app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml                    自适应图标

说明：
- 自适应图标的前景只占画布 66%（Android 的安全区），四周留透明；
- 传统图标用底色 #EFFFDE 铺满，与原站页面同色，避免白底方块；
- 只在源图或尺寸规则变化时才需要重跑。
"""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ANDROID = os.path.dirname(HERE)
PROJECT = os.path.dirname(os.path.dirname(ANDROID))  # 02_新项目_离线阅读器
SRC = os.path.join(PROJECT, "图标_透明.png")
RES = os.path.join(ANDROID, "app", "src", "main", "res")

BG = (0xEF, 0xFF, 0xDE, 255)

DENSITIES = [
    ("mdpi", 1.0),
    ("hdpi", 1.5),
    ("xhdpi", 2.0),
    ("xxhdpi", 3.0),
    ("xxxhdpi", 4.0),
]


def fit(im, box):
    """等比缩放到 box，居中贴到同尺寸透明画布上。"""
    w, h = im.size
    k = min(box / w, box / h)
    im = im.resize((max(1, int(w * k)), max(1, int(h * k))), Image.LANCZOS)
    canvas = Image.new("RGBA", (box, box), (0, 0, 0, 0))
    canvas.paste(im, ((box - im.size[0]) // 2, (box - im.size[1]) // 2), im)
    return canvas


def main():
    if not os.path.exists(SRC):
        sys.exit("找不到源图：%s" % SRC)
    src = Image.open(SRC).convert("RGBA")

    for name, scale in DENSITIES:
        d = os.path.join(RES, "mipmap-" + name)
        os.makedirs(d, exist_ok=True)

        legacy = int(48 * scale)
        bg = Image.new("RGBA", (legacy, legacy), BG)
        bg.alpha_composite(fit(src, int(legacy * 0.92)))
        bg.convert("RGB").save(os.path.join(d, "ic_launcher.png"), "PNG")

        fg = int(108 * scale)
        fit(src, int(fg * 0.66)).save(os.path.join(d, "ic_launcher_foreground.png"), "PNG")

    anydpi = os.path.join(RES, "mipmap-anydpi-v26")
    os.makedirs(anydpi, exist_ok=True)
    with open(os.path.join(anydpi, "ic_launcher.xml"), "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background" />
    <foreground android:drawable="@mipmap/ic_launcher_foreground" />
</adaptive-icon>
""")
    print("图标已生成：", RES)


if __name__ == "__main__":
    main()
