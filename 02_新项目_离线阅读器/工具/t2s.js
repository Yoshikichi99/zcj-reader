/**
 * 繁 → 简 转换引擎（浏览器 / Node 通用）
 * 数据来自 OpenCC：TSPhrases（短语）+ TSCharacters（单字）
 *
 * 规则：
 *   1. 先保护「明覆」（避免 OpenCC 的 明覆→明复 误伤「無明覆蓋」）
 *   2. 按短语替换（长的优先，顺序与 OpenCC 一致）
 *   3. 按单字映射；「祇」固定不转（祇樹/祇陀）
 *   4. 还原保护的「明覆」
 *   5. 人名「莊春江」固定不转（转完再改回）
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.T2S = factory();
})(typeof self !== "undefined" ? self : this, function () {
  var phrases = null;
  var chars = null;
  var PROT = "\uE000";   // 私用区占位符

  function init(data) {
    phrases = data.p || [];
    chars = Object.assign({}, data.c || {});
    delete chars["祇"];
  }

  function toSimp(s) {
    if (s == null) return "";
    var out = String(s).split("明覆").join(PROT);
    for (var i = 0; i < phrases.length; i++) {
      var k = phrases[i][0];
      if (out.indexOf(k) >= 0) out = out.split(k).join(phrases[i][1]);
    }
    var arr = new Array(out.length);
    for (var j = 0; j < out.length; j++) {
      var ch = out[j];
      arr[j] = chars[ch] || ch;
    }
    var res = arr.join("").split(PROT).join("明覆");
    return res.replace(/庄春江/g, "莊春江");
  }

  return { init: init, toSimp: toSimp, get ready() { return !!phrases; } };
});
