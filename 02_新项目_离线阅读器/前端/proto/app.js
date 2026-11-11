/* 莊春江讀經站 · 離線版原型 */
(function () {
  "use strict";

  const S = {
    toc: null, pages: null, pali: null, corpus: {}, notes: null, t2s: null,
    books: {}, docs: {},
    lang: localStorage.getItem("agama_lang") || "trad",
    loaded: false,
  };

  /* ---------------- 基础工具 ---------------- */
  const $ = (sel, root) => (root || document).querySelector(sel);
  const app = () => $("#app");

  async function loadGz(url) {
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("載入失敗：" + url);
    if (!("DecompressionStream" in window)) {
      throw new Error("此瀏覽器不支援 DecompressionStream");
    }
    const ds = new DecompressionStream("gzip");
    const stream = res.body.pipeThrough(ds);
    return await new Response(stream).json();
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, c =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  }

  /* ---------------- 简繁转换 ---------------- */
  let T2S_PHRASES = null, T2S_CHARS = null, T2S_RPHRASES = null, T2S_RCHARS = null;
  const PROT = "\uE000";

  function initT2S(data) {
    T2S_PHRASES = data.p || [];
    T2S_CHARS = Object.assign({}, data.c || {});
    delete T2S_CHARS["祇"];
    // 简 -> 繁 反查表（搜索时把简体关键词转回繁体）
    T2S_RCHARS = {};
    for (const t in T2S_CHARS) {
      const s = T2S_CHARS[t];
      if (s && !T2S_RCHARS[s]) T2S_RCHARS[s] = t;
    }
    T2S_RPHRASES = T2S_PHRASES
      .map(x => [x[1], x[0]])
      .sort((a, b) => b[0].length - a[0].length);
  }

  function toTrad(s) {
    if (s == null || !T2S_RPHRASES) return s == null ? "" : String(s);
    let out = String(s);
    for (const [k, v] of T2S_RPHRASES) {
      if (out.indexOf(k) >= 0) out = out.split(k).join(v);
    }
    const arr = new Array(out.length);
    for (let i = 0; i < out.length; i++) arr[i] = T2S_RCHARS[out[i]] || out[i];
    return arr.join("").replace(/莊春江/g, "莊春江");
  }
  function toSimp(s) {
    if (s == null) return "";
    if (!T2S_PHRASES) return String(s);
    let out = String(s).split("明覆").join(PROT);
    for (let i = 0; i < T2S_PHRASES.length; i++) {
      const k = T2S_PHRASES[i][0];
      if (out.indexOf(k) >= 0) out = out.split(k).join(T2S_PHRASES[i][1]);
    }
    const arr = new Array(out.length);
    for (let j = 0; j < out.length; j++) {
      const ch = out[j];
      arr[j] = T2S_CHARS[ch] || ch;
    }
    return arr.join("").split(PROT).join("明覆").replace(/庄春江/g, "莊春江");
  }
  function tr(html) {
    return S.lang === "simp" ? toSimp(html) : html;
  }
  const TRCACHE = new Map();
  function trCached(key, html) {
    if (S.lang !== "simp") return html;
    const ck = S.lang + "|" + key;
    if (TRCACHE.has(ck)) return TRCACHE.get(ck);
    const out = toSimp(html);
    if (TRCACHE.size > 40) TRCACHE.clear();
    TRCACHE.set(ck, out);
    return out;
  }

  /* ---------------- 启动 ---------------- */
  function fatal(msg, detail) {
    document.body.innerHTML = '<div style="max-width:720px;margin:60px auto;padding:24px;' +
      'font-family:Tahoma,SimSun,sans-serif;color:#333;background:#fff;border:1px solid #ccc">' +
      '<h1 style="font-size:20pt;color:#a33">資料載入失敗</h1>' +
      '<p style="font-size:13pt;line-height:1.8">' + esc(msg) + '</p>' +
      '<pre style="background:#f6f6f6;padding:10px;white-space:pre-wrap;font-size:10pt">' +
      esc(detail || "") + '</pre>' +
      '<p style="font-size:12pt;color:#666">請重新解壓縮完整的程式資料夾，或重新下載。</p></div>';
  }

  async function boot() {
    let stage = "目錄";
    try {
      showBoot(0, "載入目錄…");
      S.toc = await loadGz("data/toc.json.gz");
      stage = "繁簡轉換表";
      S.t2s = await loadGz("data/t2s.json.gz").catch(() => null);
      if (S.t2s) initT2S(S.t2s);
    } catch (err) {
      fatal("載入「" + stage + "」時出錯。", err && err.message ? err.message : String(err));
      return;
    }

    S.loaded = true;
    buildBookIdx();
    hideBoot();
    window.addEventListener("hashchange", route);
    route();
    applyLangLabel();

    stage = "經文索引";
    showToast("正在載入經文資料…");
    try {
      S.pages = await loadGz("data/pages.json.gz");
      stage = "巴利原文";
      showToast("正在載入巴利原文…");
      S.pali = await loadGz("data/pali.json.gz");
      stage = "經文語料";
      showToast("正在載入經文語料…");
      const series = ["SA", "SN", "MA", "MN", "DA", "DN", "AA", "AN", "ZA", "OTHER"];
      const missing = [];
      for (const code of series) {
        try {
          const d = await loadGz("data/corpus/" + code + ".json.gz");
          Object.assign(S.corpus, d);
        } catch (e) {
          missing.push(code);
        }
      }
      if (missing.length) {
        showToast("警告：缺少語料檔 " + missing.join("、") + "，部分經文可能無法顯示");
      }
      S.notes = await loadGz("data/notes.json.gz").catch(() => ({}));
      S.docs = await loadGz("data/docs.json.gz").catch(() => ({}));
      S.dataReady = true;
      buildSeq();
      buildDocSeq();
      hideToast();
      route();
    } catch (err) {
      hideToast();
      fatal("載入「" + stage + "」時出錯。", err && err.message ? err.message : String(err));
    }
  }
  function showToast(msg) {
    let el = document.getElementById("toast");
    if (!el) {
      el = document.createElement("div");
      el.id = "toast";
      document.body.appendChild(el);
    }
    el.textContent = msg;
    el.style.display = "block";
  }
  function hideToast() {
    const el = document.getElementById("toast");
    if (el) el.style.display = "none";
  }

  function showBoot(pct, text) {
    let el = $("#boot");
    if (!el) {
      el = document.createElement("div");
      el.id = "boot";
      el.innerHTML = '<div class="box"><div id="boottext"></div><div class="bar"><i></i></div></div>';
      document.body.appendChild(el);
    }
    $("#boottext").textContent = text || "載入中…";
    el.querySelector(".bar i").style.width = pct + "%";
  }
  function hideBoot() {
    const el = $("#boot");
    if (el) el.remove();
  }

  /* ---------------- 路由 ---------------- */
  const VISITED = new Set((function () {
    try { return JSON.parse(localStorage.getItem("zcj_visited") || "[]"); } catch (e) { return []; }
  })());

  function markVisited() {
    document.querySelectorAll('a[href^="#/"]').forEach(a => {
      const h = a.getAttribute("href");
      if (VISITED.has(h)) a.classList.add("visited");
      a.addEventListener("click", () => {
        VISITED.add(h);
        try {
          localStorage.setItem("zcj_visited", JSON.stringify(Array.from(VISITED).slice(-800)));
        } catch (e) { }
      });
    });
  }

  function route() {
    render();
    markVisited();
  }

  function render() {
    if (!S.loaded) return;
    const h = (location.hash || "#/").slice(1);
    const parts = h.split("/").filter(Boolean);
    const view = parts[0] || "home";
    if (view === "c") return viewCat(parts[1]);
    if (view === "p") return viewPage(parts.slice(1).join("/"));
    if (view === "b") return viewBook(parts.slice(1).join("/"));
    if (view === "d") return viewDoc(parts.slice(1).join("/"));
    if (view === "notice") return viewNotice();
    if (view === "s") return viewSearch(parts[1] || "", decodeURIComponent(parts.slice(2).join("/")));
    return viewHome();
  }

  /* ---------------- 公共部分 ---------------- */
  function topBar(opts) {
    const o = opts || {};
    const home = '<a href="#/">首 頁</a>';
    const cat = o.cat ? '<a href="#/c/' + esc(o.cat) + '">目 錄</a>' : "";
    const back = '<a href="#/">回 首 頁</a>';
    const prev = o.prev ? '<a href="#/p/' + esc(o.prev) + '">« 上一經</a>' : "";
    const next = o.next ? '<a href="#/p/' + esc(o.next) + '">下一經 »</a>' : "";
    return `
      <div class="titlebar">${home}　${cat || back}　${prev}　${next}</div>
      <div class="searchrow">
        <form onsubmit="return false">
          <span>經號：</span>
          <input type="text" id="q-id" size="6" value="">
          <input type="submit" value="進入" id="go-id">
        </form>
        <form onsubmit="return false">
          <input type="text" id="q-text" size="14" placeholder="全文檢索">
          <input type="submit" value="檢索" id="go-text">
        </form>
        <span class="update_time">${esc(o.time || "")}</span>
      </div>`;
  }

  /* 静态页导航：首頁 / 目錄 / 上一節 / 下一節 */
  function siteNav(ctx, bottom) {
    const c = ctx || {};
    return `<div class="sitenav${bottom ? " bottom" : ""}">
      <a href="#/">首頁</a>
      ${c.toc ? '<a href="' + c.toc + '">目錄</a>' : ""}
      ${c.prevHref ? '<a href="' + c.prevHref + '">« 上一節</a>' : ""}
      ${c.nextHref ? '<a href="' + c.nextHref + '">下一節 »</a>' : ""}
    </div>`;
  }

  /* 页内锚点：原站的「請點選各相應之編號」「點選經號」等 */
  function bindAnchors() {
    document.querySelectorAll(".orig a[data-anchor]").forEach(a => {
      a.style.cursor = "pointer";
      a.addEventListener("click", ev => {
        ev.preventDefault();
        const name = a.getAttribute("data-anchor");
        if (!name) return;
        let t = null;
        try {
          t = document.querySelector('.orig [name="' + CSS.escape(name) + '"]') ||
            document.querySelector('.orig [id="' + CSS.escape(name) + '"]');
        } catch (e) { }
        if (t) t.scrollIntoView({ block: "start", behavior: "auto" });
      });
    });
  }

  function bindTop(cat) {
    const goId = $("#go-id"), goText = $("#go-text");
    if (goId) goId.onclick = () => {
      const v = ($("#q-id").value || "").trim().toUpperCase();
      if (!v) return;
      // SA0001 / SN0544 形式
      const catCode = (v.match(/^[A-Z]+/) || [""])[0];
      if (catCode && /^\d+$/.test(v.replace(catCode, ""))) {
        location.hash = "#/p/" + catCode + "/" + v;
      } else {
        location.hash = "#/s/" + encodeURIComponent(cat || "") + "/" + encodeURIComponent(v);
      }
    };
    if (goText) goText.onclick = () => {
      const v = ($("#q-text").value || "").trim();
      if (v) location.hash = "#/s/" + encodeURIComponent(cat || "") + "/" + encodeURIComponent(v);
    };
  }

  /* ---------------- 首页 ---------------- */
  const LINKS = {
    sa: "SA", ma: "MA", da: "DA", aa: "AA", sn: "SN", mn: "MN", dn: "DN", ann: "AN",
    ud: "Ud", it: "It", ps: "Ps", ni: "Ni", kh: "Kh", dh: "Dh", su: "Su", vi: "Vi",
    pv: "Pv", th: "Th", ti: "Ti", ap: "Ap", bv: "Bv", cp: "Cp", ja: "Ja", mi: "Mi",
  };
  const BOOK_LINKS = {
    "b1.gif": "book/bb", "b2.gif": "book/buhis", "b3.gif": "book/as",
    "b4.gif": "book/nn20", "b5.gif": "book/mn12", "b6.gif": "book/tb",
  };

  function imgLink(src, alt, href) {
    const img = '<img src="assets/' + src + '" alt="' + esc(alt) + '">';
    return href ? '<a href="' + href + '">' + img + "</a>" : img;
  }

  function viewHome() {
    if (S.toc && S.toc.home) {
      app().innerHTML = '<div class="orig">' + trCached("home", S.toc.home) + "</div>";
      document.title = "莊春江讀經站 · 離線版";
      return;
    }
    app().innerHTML = '<div class="cat"><p>首頁資料缺失</p></div>';
  }

  /* ---------------- 上一篇 / 下一篇 ---------------- */
  const SEQ = {};
  function buildSeq() {
    for (const cat of S.toc.cats) {
      cat.items.forEach((it, i) => {
        SEQ[it.p] = {
          prev: i > 0 ? cat.items[i - 1].p : null,
          next: i < cat.items.length - 1 ? cat.items[i + 1].p : null,
        };
      });
    }
    for (const b of S.toc.books) {
      b.chapters.forEach((ch, i) => {
        SEQ[ch.id] = {
          prev: i > 0 ? b.chapters[i - 1].id : null,
          next: i < b.chapters.length - 1 ? b.chapters[i + 1].id : null,
        };
      });
    }
  }

  const DOCSEQ = {};
  const BOOK_IDX = {};
  function buildBookIdx() {
    (S.toc.books || []).forEach(b => { if (b.idx) BOOK_IDX[b.id] = b.idx; });
  }
  function buildDocSeq() {
    const ds = S.toc.docs || [];
    ds.forEach((d, i) => {
      DOCSEQ[d.id] = {
        prev: i > 0 ? ds[i - 1].id : null,
        next: i < ds.length - 1 ? ds[i + 1].id : null,
      };
    });
  }

  function pagerHtml(pid) {
    const s = SEQ[pid];
    if (!s) return "";
    return `<div class="pager">
      ${s.prev ? '<a href="#/p/' + esc(s.prev) + '">« 上一經</a>' : "<span></span>"}
      ${s.next ? '<a href="#/p/' + esc(s.next) + '">下一經 »</a>' : "<span></span>"}
    </div>`;
  }

  function subGroup(pid) {
    const rec = S.pages[pid + ".htm"];
    const sub = rec && rec[8] ? rec[8] : "";
    const m = sub.match(/^\(([^)]*)\)/);
    if (m) {
      const name = m[1].split("/")[0].trim();
      // 只认「相應 / 品 / 篇 / 分 / 集」这类栏目名，排除「莊春江譯」之类
      if (/(相應|品|篇|分|集)$/.test(name)) return name;
    }
    return "";
  }

  let SN_NAMES = null;
  function buildSnNames() {
    const m = {};
    for (const pid in S.pages) {
      const rec = S.pages[pid];
      if (rec[5] !== "SN") continue;
      const k = (rec[1] || [])[0] || "";
      const parts = k.split(".");
      if (parts.length < 2) continue;
      const mm = (rec[8] || "").match(/^\(([^)]*)\)/);
      if (mm) m[parts[1]] = mm[1].split("/")[0].trim();
    }
    return m;
  }
  function keyGroup(k) {
    if (!k) return "";
    const p = k.split(".");
    if (p[0] === "SN") {
      if (!SN_NAMES) SN_NAMES = buildSnNames();
      return SN_NAMES[p[1]] || (p[1] + "相應");
    }
    if (p[0] === "AN") return p[1] + "集";
    return "";
  }

  function viewCat(code) {
    const cat = S.toc.cats.find(c => c.id === code);
    if (!cat) return viewHome();
    if (cat.page) {
      app().innerHTML = '<div class="orig">' + trCached("cat:" + code, cat.page) + "</div>";
      document.title = (cat.n || code) + " · 莊春江讀經站";
      // 栏目页的检索框：接到本栏目全文搜索
      document.querySelectorAll(".orig form").forEach(f => {
        f.addEventListener("submit", ev => {
          ev.preventDefault();
          const action = (f.getAttribute("action") || "").toLowerCase();
          if (/dm\.html|mx\.php|fx\.php/.test(action)) {
            location.hash = "#/notice";
            return;
          }
          const inp = f.querySelector('input[name="keyword"]') || f.querySelector('input[type="text"]');
          const v = inp ? inp.value.trim() : "";
          if (!v) return;
          location.hash = "#/s/" + encodeURIComponent(code) + "/" + encodeURIComponent(v);
        });
      });
      bindAnchors();
      return;
    }
    app().innerHTML = '<div class="cat"><h1>' + esc(cat.n) + '</h1><p>此欄目無目錄頁</p></div>';
  }

  /* ---------------- 页面渲染 ---------------- */
  function seriesOfKey(k) { return k.split(".")[0]; }

  function buildPageBody(pid) {
    const rec = S.pages[pid];
    if (!rec) return null;
    const nm = rec[0], keys = rec[1], ov = rec[2], cmp = rec[3], paliIds = rec[4],
      cat = rec[5], num = rec[6], pres = rec[7] || {};
    const parts = [];
    for (const k of keys) {
      const html = ov[k] || S.corpus[k] || "";
      if (!html) continue;
      const pre = pres[k] ? "<div class='pre'>" + pres[k] + "</div>" : "";
      parts.push(pre + html);
    }
    const content = parts.join("");
    const paliHtml = (paliIds || []).map(id => S.pali[id] || "").join("<br>");
    const cmpHtml = cmp || "";
    const series = new Set(keys.map(seriesOfKey));
    const hasNorth = ["SA", "MA", "DA", "AA", "ZA", "OTHER"].some(x => series.has(x));
    const hasSouth = ["SN", "AN", "MN", "DN"].some(x => series.has(x));
    return { nm, content, paliHtml, cmpHtml, cat, num, both: hasNorth && hasSouth, hasPali: !!paliHtml };
  }

  function paneHtml(title, body, foldable) {
    return `<div class="pane">
      <div class="ph"><span class="ttl">${esc(title)}</span>${foldable ? '<span class="fold" title="隱藏本欄">»</span>' : ""}</div>
      <div class="pb">${body}</div></div>`;
  }

  function docRec(pid) {
    const base = pid.replace(/\.htm$/, "");
    return S.books[base] || S.docs[base] || null;
  }

  function buildDocBody(pid) {
    const rec = docRec(pid);
    if (!rec) return null;
    const html = (rec[1] || []).map(b => b[2] || "").join("");
    return { nm: rec[0] || pid, content: html, paliHtml: "", cmpHtml: "", cat: "", num: 0, both: false, single: true };
  }

  function viewPage(pidRaw) {
    const pid = pidRaw.endsWith(".htm") ? pidRaw : pidRaw + ".htm";
    const key = pidRaw.replace(/\.htm$/i, "");
    if (S.toc.static && S.toc.static[key]) {
      const bookid = key.startsWith("book/") ? key.split("/").slice(0, 2).join("/") : "";
      const tocHref = bookid && BOOK_IDX[bookid] ? "#/p/" + BOOK_IDX[bookid] : "#/";
      const ctx = {
        toc: tocHref,
        prevHref: SEQ[key] && SEQ[key].prev ? "#/p/" + SEQ[key].prev : null,
        nextHref: SEQ[key] && SEQ[key].next ? "#/p/" + SEQ[key].next : null,
      };
      app().innerHTML = siteNav(ctx, false) +
        '<div class="orig">' + trCached("p:" + key, S.toc.static[key]) + "</div>" +
        siteNav(ctx, true);
      bindAnchors(); bindDeadForms();
      document.title = key + " · 莊春江讀經站";
      try { localStorage.setItem("last_page", pidRaw); } catch (e) { }
      return;
    }
    if (!S.dataReady) {
      app().innerHTML = '<div class="cat"><p style="padding:60px 0;text-align:center;color:#777">經文資料載入中，請稍候…</p></div>';
      return;
    }
    const d = buildPageBody(pid) || buildDocBody(pid);
    if (!d) { app().innerHTML = topBar() + '<div class="cat"><p>找不到頁面：' + esc(pidRaw) + "</p></div>"; return; }
    if (d.single) {
      app().innerHTML = topBar({ cat: d.cat, prev: (SEQ[pidRaw] || {}).prev, next: (SEQ[pidRaw] || {}).next }) +
        '<div class="panes"><div class="pane" style="flex:1"><div class="pb">' + tr(d.content) + "</div></div></div>";
      bindNotes(); bindLinks();
      document.title = d.nm + " · 莊春江讀經站";
      return;
    }
    const full = d.content + (d.paliHtml ? '<div class="pali">' + d.paliHtml + "</div>" : "") +
      (d.cmpHtml ? '<div class="comp">' + d.cmpHtml + "</div>" : "");
    let left, right, leftTitle, rightTitle;
    if (d.both) {
      left = full; right = full;
      leftTitle = "拉動本欄右邊滑桿，可選擇「任一經文」";
      rightTitle = "拉動本欄右邊滑桿，可選擇「對讀經文」(點右端»隱藏本欄)";
    } else {
      left = d.content + (d.cmpHtml ? '<div class="comp">' + d.cmpHtml + "</div>" : "");
      right = d.paliHtml ? '<div class="pali">' + d.paliHtml + "</div>" : "";
      leftTitle = "漢譯經文";
      rightTitle = "巴利語經文(點右端»隱藏本欄)";
    }
    app().innerHTML = topBar({ cat: d.cat, prev: (SEQ[pidRaw] || {}).prev, next: (SEQ[pidRaw] || {}).next }) +
      '<div class="panes">' +
      paneHtml(leftTitle, tr(left), false) +
      (right ? paneHtml(rightTitle, tr(right), true) : "") +
      "</div>";
    bindTop(d.cat);
    bindNotes();
    bindLinks();
    bindFold();
    document.title = d.nm + " · 莊春江讀經站";
    try { localStorage.setItem("last_page", pidRaw); } catch (e) { }
  }

  /* ---------------- 注释 ---------------- */
  function bindNotes() {
    document.querySelectorAll(".pb a.n, .pb a.l").forEach(a => {
      a.onclick = ev => {
        ev.preventDefault();
        const n = a.getAttribute("data-n");
        let html = "";
        if (a.classList.contains("n")) html = S.notes[n] || "（此註解不存在）";
        else {
          const el = document.getElementById("note" + n);
          html = el ? el.innerHTML : "（此註解不存在）";
        }
        showNote(html, ev.clientX, ev.clientY);
      };
    });
  }
  function showNote(html, x, y) {
    const pop = $("#notediv");
    pop.innerHTML = tr(html);
    pop.classList.add("show");
    const w = Math.min(700, window.innerWidth - 40);
    pop.style.width = w + "px";
    pop.style.left = Math.max(10, Math.min(x + 12, window.innerWidth - w - 10)) + "px";
    pop.style.top = Math.max(10, Math.min(y + 16, window.innerHeight - 200)) + "px";
  }
  document.addEventListener("click", ev => {
    const pop = $("#notediv");
    if (pop && pop.classList.contains("show") && !pop.contains(ev.target) && !ev.target.closest("a.n,a.l")) {
      pop.classList.remove("show");
    }
  });

  /* ---------------- 站内链接 ---------------- */
  function bindLinks() {
    document.querySelectorAll(".pb a[href]").forEach(a => {
      const href = a.getAttribute("href");
      if (!href || href.startsWith("http") || href.startsWith("#")) return;
      a.onclick = ev => {
        ev.preventDefault();
        const clean = href.replace(/^\.\//, "").replace(/\.htm.*$/, "");
        location.hash = "#/p/" + clean;
      };
    });
  }

  /* ---------------- 折叠栏目 ---------------- */
  function bindFold() {
    document.querySelectorAll(".pane .ph .fold").forEach(f => {
      f.onclick = () => f.closest(".pane").classList.toggle("collapsed");
    });
  }

  /* ---------------- 著作 ---------------- */
  function viewBook(bookid) {
    const b = S.toc.books.find(x => x.id === bookid);
    if (!b) return viewHome();
    if (b.idx && S.toc.static && S.toc.static[b.idx]) {
      // 统一走页面路由，避免 /b/... 与 /p/... 两套地址
      location.hash = "#/p/" + b.idx;
      return;
    }
    const rows = b.chapters.map(ch =>
      `<li><a href="#/p/${esc(ch.id)}">${esc(tr(ch.t))}</a></li>`).join("");
    app().innerHTML = topBar() +
      `<div class="cat"><h1>${esc(b.n)}</h1><div class="meta">共 ${b.chapters.length} 篇</div><ul>${rows}</ul></div>`;
    bindTop();
    document.title = b.n + " · 莊春江讀經站";
  }

  function firstLine(html) {
    const t = (html || "").replace(/<[^>]+>/g, "");
    for (const ln of t.split("\n")) {
      const s = ln.trim();
      if (s) return s;
    }
    return "";
  }

  /* ---------------- 未实装功能提示 ---------------- */
  function viewNotice() {
    app().innerHTML = topBar() +
      `<div class="cat notice">
        <h1>此功能未實裝</h1>
        <p>本離線版未包含這項功能。</p>
        <p>如有需要，請訪問莊春江工作站原站：</p>
        <p class="url"><a href="https://agama.buddhason.org/" target="_blank" rel="noopener">https://agama.buddhason.org/</a></p>
        <p class="tip">原站需要聯網；本離線版不會主動連接網路。</p>
      </div>`;
    bindTop();
    document.title = "功能未實裝 · 莊春江讀經站";
  }

  /* 把原站里需要服务器/外部资源才能用的表单，统一导向提示页 */
  function bindDeadForms() {
    document.querySelectorAll(".orig form").forEach(f => {
      f.addEventListener("submit", ev => {
        ev.preventDefault();
        location.hash = "#/notice";
      });
    });
  }

  function viewDoc(id) {
    const key = id.replace(/\.htm$/i, "");
    if (S.toc.static && S.toc.static[key]) {
      const ds = DOCSEQ[key] || {};
      const ctx = {
        toc: "#/",
        prevHref: ds.prev ? "#/d/" + ds.prev : null,
        nextHref: ds.next ? "#/d/" + ds.next : null,
      };
      app().innerHTML = siteNav(ctx, false) +
        '<div class="orig">' + trCached("d:" + key, S.toc.static[key]) + "</div>" +
        siteNav(ctx, true);
      bindAnchors(); bindDeadForms();
      document.title = key + " · 莊春江讀經站";
      return;
    }
    const pid = id.endsWith(".htm") ? id : id + ".htm";
    const d = buildDocBody(pid);
    if (!d) {
      app().innerHTML = topBar() + '<div class="cat"><p>找不到：' + esc(id) + "</p></div>";
      return;
    }
    app().innerHTML = topBar() +
      '<div class="panes"><div class="pane" style="flex:1"><div class="pb">' + tr(d.content) + "</div></div></div>";
    bindNotes(); bindLinks();
    document.title = d.nm + " · 莊春江讀經站";
  }

  /* ---------------- 全文搜索（限本栏目） ---------------- */
  const TEXT_CACHE = new Map();
  function stripHtml(h) {
    return String(h || "")
      .replace(/<script[\s\S]*?<\/script>/gi, "")
      .replace(/<[^>]+>/g, "")
      .replace(/&nbsp;/g, " ").replace(/&amp;/g, "&")
      .replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"');
  }
  function pageText(pid) {
    if (TEXT_CACHE.has(pid)) return TEXT_CACHE.get(pid);
    let t = "";
    const rec = S.pages[pid];
    if (rec) {
      let s = "";
      for (const k of rec[1]) s += (rec[2][k] || S.corpus[k] || "");
      s += rec[3] || "";
      t = stripHtml(s);
    } else {
      const st = S.toc.static && S.toc.static[pid.replace(/\.htm$/i, "")];
      if (st) t = stripHtml(st);
    }
    TEXT_CACHE.set(pid, t);
    return t;
  }
  function snippet(text, idx, len, q) {
    const a = Math.max(0, idx - 30), b = Math.min(text.length, idx + q.length + 30);
    let s = text.slice(a, b).replace(/\s+/g, " ");
    s = esc(s);
    const qq = esc(q);
    if (qq) s = s.split(qq).join("<mark>" + qq + "</mark>");
    return (a > 0 ? "…" : "") + s + (b < text.length ? "…" : "");
  }
  function searchCat(cat, q) {
    const qq = toTrad(q);
    if (!qq) return { hits: [], qq };
    const catObj = S.toc.cats.find(c => c.id === cat);
    if (!catObj) return { hits: [], qq };
    const hits = [];
    for (const it of catObj.items) {
      const pid = it.p + ".htm";
      const t = pageText(pid);
      const idx = t.indexOf(qq);
      if (idx >= 0) {
        const rec = S.pages[pid];
        hits.push({ p: it.p, t: (rec && rec[0]) || it.t || it.p, sn: snippet(t, idx, 0, qq) });
        if (hits.length >= 500) break;
      }
    }
    return { hits, qq };
  }

  async function viewSearch(cat, q) {
    q = (q || "").trim();
    const catObj = S.toc.cats.find(c => c.id === cat);
    if (!S.dataReady) {
      app().innerHTML = '<div class="cat"><p style="padding:60px 0;text-align:center;color:#777">經文資料載入中，請稍候…</p></div>';
      return;
    }
    if (!q) {
      app().innerHTML = topBar({ cat }) + '<div class="search"><h1>請輸入關鍵字</h1></div>';
      bindTop(cat);
      return;
    }
    app().innerHTML = topBar({ cat }) + '<div class="search"><h1>搜尋中…</h1></div>';
    await new Promise(r => setTimeout(r, 20));
    const { hits } = searchCat(cat, q);
    const rows = hits.map(h => `
      <div class="hit">
        <a href="#/p/${esc(h.p)}">${esc(tr(h.t))}</a>
        <span class="from">（${esc(catObj ? catObj.n : cat)}）</span>
        <div class="snip">${tr(h.sn)}</div>
      </div>`).join("");    app().innerHTML = topBar({ cat }) +
      `<div class="search">
        <h1>「${esc(q)}」在${esc(catObj ? catObj.n : cat)}中共 ${hits.length} 筆</h1>
        <div class="searchbox2">
          <input id="s-q" type="text" value="${esc(q)}" placeholder="在本欄目內搜尋">
          <button id="s-go">搜尋</button>
        </div>
        ${rows || "<p>沒有找到。</p>"}
      </div>`;
    bindTop(cat);
    const go = () => {
      const v = ($("#s-q").value || "").trim();
      if (v) location.hash = "#/s/" + encodeURIComponent(cat) + "/" + encodeURIComponent(v);
    };
    const btn = $("#s-go"); if (btn) btn.onclick = go;
    const inp = $("#s-q");
    if (inp) inp.onkeydown = e => { if (e.key === "Enter") go(); };
    document.title = "檢索：" + q;
  }

  /* ---------------- 简繁开关 ---------------- */
  function applyLangLabel() {
    const a = $("#langtoggle");
    if (!a) return;
    a.textContent = S.lang === "simp" ? "繁體" : "简体";
    a.onclick = ev => {
      ev.preventDefault();
      S.lang = S.lang === "simp" ? "trad" : "simp";
      try { localStorage.setItem("agama_lang", S.lang); } catch (e) { }
      applyLangLabel();
      route();
    };
  }

  /* ---------------- 启动 ---------------- */
  window.addEventListener("DOMContentLoaded", () => {
    boot().catch(err => {
      hideBoot();
      app().innerHTML = '<div class="cat"><h1>載入失敗</h1><p>' + esc(err.message) + "</p></div>";
    });
  });
})();
