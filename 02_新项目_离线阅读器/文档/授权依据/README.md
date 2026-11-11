# 授权依据（存档）

本目录存放原站 CC 授权声明的**原始出处**，供日后核验。因为该声明是由 JavaScript 动态注入的，
普通网页存档（另存为 HTML、纯文本抓取、截图以外的抓取工具）都看不到它，所以特意保留原始文件。

## 一、抓取记录

| 项目 | 内容 |
|---|---|
| 抓取时间 | 2026-11-11 19:33 (UTC+8)／2026-11-11T11:33:47Z |
| 来源 1 | `https://agama.buddhason.org/menu.js` — HTTP 200，25,758 字节 |
| SHA-256（menu.js） | `a7bcd980ad7a024ee5f8b0c2586fe56e38038287988c1928d4bdda8dc6a06e63` |
| 来源 2 | `https://agama.buddhason.org/index.htm` — HTTP 200，5,595 字节 |
| SHA-256（index.htm） | `c5060f9d67311b48a49f8af4c2138717e3c4345f5bc9eeecf3b80a032c2c1b0e` |

本目录内的 `menu.js`、`index.htm` 为上述地址的**逐字节原始副本**，未经任何修改，编码与线上一致。

## 二、声明位置

`index.htm` 末尾只有一句调用：

```html
<script>show_foot();</script>
```

页脚内容由 `menu.js` 中的 `show_foot()` 生成：

```js
function show_foot() {
    var licenseContent =
        '<div style="text-align: center; font-size: 0.9em; ...">' +
            '<p style="font-size: 1.2em;">莊春江讀經站</p>' +
            '<p>本站內容由莊春江老師翻譯、整理與著述，現由家屬決議採創用 CC 授權開放分享。</p>' +
            '<p>除另有註明外，本站內容採用 ' +
                '<a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hant" target="_blank">' +
                    '創用 CC 姓名標示-非商業性-相同方式分享 4.0 國際</a> 授權條款釋出。</p>' +
            '<a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hant" target="_blank">' +
                '<img alt="創用 CC 授權條款" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" />' +
            '</a>' +
        '</div>';

    var container = document.getElementById('license-container');
    if (container) { container.innerHTML = licenseContent; }
    else { document.write(licenseContent); }
}
```

声明文本（转录）：

> 莊春江讀經站
> 本站內容由莊春江老師翻譯、整理與著述，現由家屬決議採創用 CC 授權開放分享。
> 除另有註明外，本站內容採用 創用 CC 姓名標示-非商業性-相同方式分享 4.0 國際 授權條款釋出。

授权链接：<https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hant>

## 三、为什么必须单独存档

1. **页脚是 JS 注入的**：`index.htm` 本身不含任何授权文字，用 `curl`、网页另存为、
   或以纯 HTML 文本方式抓取，都只会得到 `<script>show_foot();</script>`，看不到声明。
2. **本地镜像早于该声明**：本仓库 `01_旧项目_庄春江镜像/站点_纯净版/` 的抓取时间早于此变更，
   其中 `menu.js` 的 `show_foot()` 只输出一行「莊春江工作站」，不含 CC 条款；
   `book/*/menu.js` 里的同名函数也只有旧的 `<hr>` 与站名。也就是说，
   **线上当前版本才是授权声明的唯一出处**，一旦原站下线或再改版，此存档即为凭据。
3. 因此这里保留的是线上的**原始文件副本 + 哈希**，并记录抓取时间与状态码。

## 四、自行校验

```powershell
cd "02_新项目_离线阅读器\文档\授权依据"
Get-FileHash .\menu.js   -Algorithm SHA256   # a7bcd980...
Get-FileHash .\index.htm -Algorithm SHA256   # c5060f9d...
curl.exe -s https://agama.buddhason.org/menu.js | Select-String "by-nc-sa"
```

若线上内容已变，以上哈希可用于确认本存档与抓取当时一致。
