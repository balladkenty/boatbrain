(function(){if(window.__bbBmInit)return;window.__bbBmInit=1;var css="/* BOAT BRAIN \u6b6a\u307f\u30ec\u30fc\u30c0\u30fc \u2014 overlay styles (scoped under #bb-root) */\n#bb-fab{position:fixed;right:18px;bottom:18px;z-index:2147483646;\n  background:#21406b;color:#fff;border:none;border-radius:24px;padding:11px 16px;\n  font:600 13px/1 \"Hiragino Mincho ProN\",\"Yu Mincho\",serif;letter-spacing:.12em;\n  box-shadow:0 3px 10px rgba(0,0,0,.25);cursor:pointer;}\n#bb-fab:hover{background:#2d568c;}\n#bb-backdrop{position:fixed;inset:0;z-index:2147483646;background:rgba(20,15,10,.45);display:none;}\n#bb-backdrop.bb-open{display:block;}\n#bb-root{position:fixed;top:50%;right:16px;transform:translateY(-50%);z-index:2147483647;\n  width:min(700px,92vw);max-height:92vh;overflow:auto;\n  background:#efe7d3;border:1px solid #cdbd98;border-radius:14px;box-shadow:0 14px 44px rgba(0,0,0,.42);\n  font-family:\"Hiragino Mincho ProN\",\"Yu Mincho\",serif;color:#2a2520;display:none;}\n#bb-root.bb-open{display:block;}\n#bb-root *{box-sizing:border-box;}\n#bb-head{display:flex;align-items:center;justify-content:space-between;padding:11px 14px;border-bottom:2px solid #21406b;}\n#bb-head .bb-brand{font-size:10px;letter-spacing:.3em;color:#5b7aa6;}\n#bb-head h3{margin:1px 0 0;font-size:17px;color:#21406b;letter-spacing:.06em;}\n#bb-close{background:none;border:none;font-size:20px;cursor:pointer;color:#8a7f6c;line-height:1;}\n#bb-body{padding:16px 20px 24px;}\n.bb-ctl{display:flex;align-items:center;gap:8px;font-size:12px;margin-bottom:10px;flex-wrap:wrap;}\n.bb-ctl label{display:flex;align-items:center;gap:5px;cursor:pointer;background:#fffaf0;border:1px solid #d9ccae;border-radius:7px;padding:6px 9px;}\n.bb-ctl .bb-exp{font-size:9px;color:#fff;background:#d8472b;border-radius:10px;padding:1px 6px;letter-spacing:.06em;}\n.bb-mode{font-size:11px;color:#d8472b;}\n.bb-go{background:#21406b;color:#fff;border:none;border-radius:7px;padding:7px 14px;font:inherit;font-size:13px;letter-spacing:.1em;cursor:pointer;}\n.bb-loading{padding:26px 0;text-align:center;color:#5b7aa6;letter-spacing:.1em;font-size:13px;}\n.bb-panel{background:#f7f1e2;border:1px solid #d9ccae;border-radius:10px;padding:12px;margin-bottom:14px;}\n.bb-panel h4{margin:0 0 9px;font-size:12px;letter-spacing:.14em;color:#21406b;border-left:3px solid #d8472b;padding-left:8px;}\n.bb-legend{display:flex;flex-wrap:wrap;gap:10px;font-size:11px;margin-bottom:8px;}\n.bb-legend span{display:flex;align-items:center;gap:5px;}\n.bb-legend i{width:12px;height:12px;border-radius:50%;display:inline-block;}\n#bb-root svg{width:100%;height:auto;display:block;background:#fffdf6;border:1px solid #d9ccae;border-radius:8px;}\n.bb-note{font-size:11px;color:#8a7f6c;margin-top:8px;line-height:1.55;}\n.bb-card{display:grid;grid-template-columns:30px 1fr auto;gap:9px;align-items:center;border:1px solid #d9ccae;border-radius:9px;padding:8px 10px;margin-bottom:7px;background:#fffaf0;}\n.bb-lane{width:28px;height:28px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;color:#fff;font-family:sans-serif;}\n.bb-l1{background:#fff;color:#222;border:1px solid #ccc}.bb-l2{background:#111}.bb-l3{background:#d8472b}.bb-l4{background:#1f6fb2}.bb-l5{background:#e0a52e;color:#222}.bb-l6{background:#2f9e54}\n.bb-nm{font-size:15px;}.bb-nm .bb-g{font-size:10.5px;color:#8a7f6c;margin-left:5px;}\n.bb-read{font-size:12px;color:#5b7aa6;}\n.bb-bars{display:flex;gap:4px;flex-wrap:wrap;margin-top:3px;}\n.bb-b{font-size:9px;color:#8a7f6c;background:#efe6cf;border-radius:4px;padding:1px 5px;}\n.bb-b b{color:#2a2520;}\n.bb-right{display:flex;flex-direction:column;align-items:flex-end;gap:3px;}\n.bb-chip{font-size:10px;letter-spacing:.08em;color:#fff;border-radius:20px;padding:2px 9px;font-family:sans-serif;}\n.bb-core{background:#21406b}.bb-hedge{background:#7a6a3a}.bb-roman{background:#d8472b}.bb-trap{background:#9a9488}\n.bb-dist{font-size:10px;color:#8a7f6c;}.bb-dist b{font-size:15px;font-family:sans-serif;color:#2a2520;}\n.bb-pos b{color:#d8472b}.bb-neg b{color:#5b7aa6}\n.bb-card{cursor:pointer;}\n.bb-card:hover{background:#fff6e4;border-color:#c69a3a;}\n/* \u9078\u624b\u30d7\u30ed\u30d5\u30a1\u30a4\u30eb\u8a73\u7d30\u30d1\u30cd\u30eb */\n#bb-detail{position:absolute;left:16px;right:16px;bottom:14px;z-index:5;display:none;\n  background:#fffaf0;border:1px solid #c69a3a;border-radius:12px;box-shadow:0 8px 28px rgba(0,0,0,.3);padding:14px 16px;}\n#bb-detail.bb-open{display:block;}\n#bb-detail-x{position:absolute;top:8px;right:12px;font-size:20px;color:#8a7f6c;cursor:pointer;line-height:1;}\n.bb-dt-h{font-size:16px;color:#21406b;}.bb-dt-h b{font-size:18px;}\n.bb-dt-h span{display:block;font-size:11px;color:#8a7f6c;margin-top:2px;}\n.bb-dt-s{font-size:11px;letter-spacing:.12em;color:#8a7f6c;margin:12px 0 6px;border-left:3px solid #d8472b;padding-left:7px;}\n.bb-dt-kmrow{display:flex;gap:6px;flex-wrap:wrap;}\n.bb-dt-km{display:flex;flex-direction:column;align-items:center;background:#f7f1e2;border-radius:8px;padding:6px 10px;min-width:58px;}\n.bb-dt-kl{font-size:10px;color:#8a7f6c;}.bb-dt-km b{font-size:18px;font-family:sans-serif;color:#21406b;}.bb-dt-km small{font-size:9px;color:#8a7f6c;}\n.bb-dt-crow{display:flex;gap:6px;flex-wrap:wrap;}\n.bb-dt-cc{display:flex;flex-direction:column;align-items:center;background:#f7f1e2;border-radius:7px;padding:5px 9px;font-size:11px;color:#8a7f6c;}\n.bb-dt-cc b{font-size:15px;font-family:sans-serif;color:#2a2520;}\n.bb-dt-m{font-size:12px;color:#5b5347;margin-top:10px;}\n.bb-dt-note{font-size:12px;color:#8a7f6c;line-height:1.6;}\n.bb-tk{display:flex;flex-direction:column;gap:7px;}\n.bb-ticket{border:1px dashed #c69a3a;background:#fffdf5;border-radius:8px;padding:8px 12px;font-size:12px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;}\n.bb-ticket .bb-ty{font-size:10px;color:#c69a3a;letter-spacing:.06em;min-width:110px;}\n.bb-ticket .bb-cmb{font-family:sans-serif;font-size:16px;color:#2a2520;letter-spacing:.04em;}\n.bb-ticket .bb-od{font-size:11.5px;color:#d8472b;}\n.bb-ticket .bb-alloc{font-size:10.5px;color:#7a6a3a;margin-left:auto;background:#efe6cf;border-radius:5px;padding:1px 7px;}\n/* \u65b0\u30d3\u30e5\u30fc: \u7269\u8a9e\u306e\u898b\u51fa\u3057 \uff0b \u5e02\u5834\u3068\u306e\u6e29\u5ea6\u5dee \uff0b \u5c55\u793a\u30c7\u30fc\u30bf */\n.bb-storypanel{background:#f7f1e2;}\n.bb-story{background:#fffaf0;border:1px solid #d9ccae;border-radius:9px;padding:11px 14px;}\n.bb-story-k{font-size:10px;letter-spacing:.2em;color:#8a7f6c;}\n.bb-story-h{font-size:21px;color:#21406b;letter-spacing:.04em;margin:3px 0 5px;}\n.bb-story-s{font-size:13px;line-height:1.7;color:#5b5347;}\n.bb-are{font-size:11px;font-weight:700;color:#fff;border-radius:20px;padding:1px 9px;margin-left:8px;font-family:sans-serif;letter-spacing:.04em;}\n.bb-are-\u9ad8{background:#d8472b;}.bb-are-\u4e2d{background:#c69a3a;}.bb-are-\u4f4e{background:#5b7aa6;}\n.bb-are-why{font-size:11px;color:#8a7f6c;margin-top:6px;}\n.bb-dt-kpi{display:flex;gap:8px;margin-top:10px;}\n.bb-dt-kpi span{flex:1;display:flex;flex-direction:column;align-items:center;background:#21406b;color:#fff;border-radius:8px;padding:6px 4px;font-size:10px;}\n.bb-dt-kpi b{font-size:17px;font-family:sans-serif;margin-top:1px;}\n.bb-temp-lg{display:flex;justify-content:space-between;font-size:10.5px;color:#8a7f6c;margin:2px 0 8px;}\n.bb-temp{display:flex;flex-direction:column;}\n.bb-trow{padding:9px 0;border-top:1px solid #e7dcc0;}\n.bb-trow-top{display:flex;align-items:center;gap:9px;}\n.bb-tnm{flex:0 0 132px;font-size:14px;color:#2a2520;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;}\n.bb-tnm .bb-g{font-size:10.5px;color:#8a7f6c;margin-left:5px;}\n.bb-bar{position:relative;flex:0 0 200px;height:22px;}\n.bb-bar-c{position:absolute;left:100px;top:0;bottom:0;width:1px;background:#cdbd98;}\n.bb-bar-f{position:absolute;top:5px;height:12px;border-radius:3px;}\n.bb-tval{flex:1;text-align:right;white-space:nowrap;}\n.bb-tval b{font-size:15px;font-family:sans-serif;}\n.bb-tval .bb-chip{margin-left:8px;}\n.bb-tmetrics{display:flex;gap:20px;margin-left:37px;margin-top:6px;align-items:baseline;flex-wrap:wrap;}\n.bb-tmetrics span{display:inline-flex;align-items:baseline;gap:5px;}\n.bb-tmetrics label{font-size:10.5px;color:#8a7f6c;}\n.bb-tmetrics b{font-size:19px;font-family:sans-serif;color:#2a2520;font-weight:700;}\n";var st=document.createElement('style');st.textContent=css;(document.head||document.documentElement).appendChild(st);try{/* BOAT BRAIN ロマンレーダー — content script (all computation is local; no server calls) */
(function () {
  if (window.__bbLoaded) return;
  window.__bbLoaded = true;

  const P = new URLSearchParams(location.search);
  const JCD = P.get("jcd"), RNO = P.get("rno"), HD = P.get("hd");
  if (!JCD || !RNO || !HD) return; // not a race page

  const ORIGIN = location.origin;
  const TAGJP = { core: "軸", hedge: "様子見", roman: "ロマン", trap: "過信注意" };
  const TAGREAD = {
    core: "実力も当日も市場も一致。崩れにくい軸。",
    hedge: "市場と仕上がりが拮抗。強い歪みは無い。",
    roman: "当日の仕上がりは良いのに人気が薄い。歪みの本命＝万舟の種。",
    trap: "人気だが当日の仕上がりが追いつかない。過信は禁物。"
  };

  // ---------- UI shell ----------
  const fab = document.createElement("button");
  fab.id = "bb-fab"; fab.textContent = "ロマンレーダー";
  const root = document.createElement("div");
  root.id = "bb-root";
  root.innerHTML =
    '<div id="bb-head"><div><div class="bb-brand">B O A T  B R A I N</div><h3>ロマンレーダー</h3></div>' +
    '<button id="bb-close" title="閉じる">×</button></div>' +
    '<div id="bb-body">' +
      '<div class="bb-ctl">' +
        '<button class="bb-go" id="bb-go">読む</button>' +
        '<label title="展示STを「平均比の伸び（avg−展示ST）」で主役化して評価。展示フライング艇のSTは中立化（速さとして加点しない）。">' +
          '<input type="checkbox" id="bb-method"> 展示STブースト <span class="bb-exp">実験</span></label>' +
        '<span class="bb-mode" id="bb-mode"></span>' +
        '<span class="bb-logn" id="bb-logn" style="margin-left:auto;font-size:10px;color:#8a7f6c"></span>' +
        '<button class="bb-go" id="bb-export" style="background:#7a6a3a;font-size:11px;padding:6px 10px" title="この端末に貯めた「読み＋買い目＋結果」をJSONで書き出します（自分用データ）。">記録を書き出し</button>' +
      '</div>' +
      '<div id="bb-out"></div>' +
    '</div>';
  const backdrop = document.createElement("div");
  backdrop.id = "bb-backdrop";
  document.body.appendChild(fab);
  document.body.appendChild(backdrop);
  document.body.appendChild(root);
  function setOpen(o) { root.classList.toggle("bb-open", o); backdrop.classList.toggle("bb-open", o); }
  fab.onclick = () => { const willOpen = !root.classList.contains("bb-open"); setOpen(willOpen); if (willOpen && !window.__bbRace) run(); };
  root.querySelector("#bb-close").onclick = () => setOpen(false);
  backdrop.onclick = () => setOpen(false);
  root.querySelector("#bb-go").onclick = run;
  root.querySelector("#bb-method").onchange = rerender;
  root.querySelector("#bb-export").onclick = () => bbLog.exportJSON();

  // ---------- 選手プロファイル（公式3年・同梱 profiles.json を登録番号で参照） ----------
  let BBPROF = null;
  try { fetch(chrome.runtime.getURL("profiles.json")).then(r => r.json()).then(j => { BBPROF = j; if (window.__bbRace) rerender(); }).catch(() => {}); } catch (e) {}
  const detail = document.createElement("div");
  detail.id = "bb-detail";
  detail.innerHTML = '<div id="bb-detail-x" title="閉じる">×</div><div id="bb-detail-c"></div>';
  root.appendChild(detail);
  detail.querySelector("#bb-detail-x").onclick = () => detail.classList.remove("bb-open");
  function showDetail(tb) { detail.querySelector("#bb-detail-c").innerHTML = racerDetailHTML(tb); detail.classList.add("bb-open"); }
  root.querySelector("#bb-out").addEventListener("click", e => {
    const el = e.target.closest("[data-toban]"); if (!el) return;
    const tb = el.getAttribute("data-toban"); if (tb && tb !== "null") showDetail(tb);
  });
  function racerDetailHTML(tb) {
    if (!BBPROF) return `<div class="bb-dt-note">プロファイル未読み込み。profiles.json を同梱して拡張を再読み込みしてください。</div>`;
    const p = BBPROF[String(tb)];
    if (!p) return `<div class="bb-dt-note">この選手の公式プロファイルが見つかりません（登録 ${tb}）。新人など3年集計に未掲載の可能性があります。</div>`;
    const labels = ["逃げ", "まくり", "差し", "まくり差し", "抜き"], w = p.w || 1;
    const km = p.km.map((c, i) => `<span class="bb-dt-km"><span class="bb-dt-kl">${labels[i]}</span><b>${Math.round(c / w * 100)}%</b><small>${c}勝</small></span>`).join("");
    const course = p.cw.map((wp, i) => `<span class="bb-dt-cc">${i + 1}<b>${(p.cn[i] && +p.cn[i] >= 10 && wp !== "") ? wp + "%" : "—"}</b></span>`).join("");
    return `<div class="bb-dt-h"><b>${p.nm}</b><span>登録${tb} ／ ${p.ty || "—"} ／ 通算${p.r}走 ${p.w}勝</span></div>` +
      `<div class="bb-dt-kpi"><span>2連対率<b>${p.r2 != null ? p.r2 + "%" : "—"}</b></span><span>3連対率<b>${p.r3 != null ? p.r3 + "%" : "—"}</b></span><span>平均ST<b>${p.st || "—"}</b></span></div>` +
      `<div class="bb-dt-s">勝ち方の内訳（公式3年）</div><div class="bb-dt-kmrow">${km}</div>` +
      `<div class="bb-dt-s">コース別1着率</div><div class="bb-dt-crow">${course}</div>` +
      `<div class="bb-dt-m">得意コース ${p.bc || "—"}コース</div>`;
  }

  // ---------- fetch (same-origin, user's own session) ----------
  async function getDoc(path) {
    const r = await fetch(`${ORIGIN}/owpc/pc/race/${path}?rno=${RNO}&jcd=${JCD}&hd=${HD}`, { credentials: "same-origin" });
    return new DOMParser().parseFromString(await r.text(), "text/html");
  }

  // ---------- parsers (validated against boatrace.jp) ----------
  function parseRacelist(doc) {
    const boats = [];
    doc.querySelectorAll("tbody.is-fs12").forEach(tb => {
      const c = tb.querySelector('td.is-fs14[class*="is-boatColor"]');
      if (!c) return;
      const boat = +((c.className.match(/is-boatColor(\d)/) || [])[1]);
      if (!(boat >= 1 && boat <= 6)) return;
      const nums = s => (s || "").replace(/\n/g, " ").trim().split(/\s+/).filter(Boolean);
      const lh = [...tb.querySelectorAll("td.is-lineH2")];
      const fl = nums(lh[0] && lh[0].innerText), nat = nums(lh[1] && lh[1].innerText), loc = nums(lh[2] && lh[2].innerText), mot = nums(lh[3] && lh[3].innerText);
      const rd = [...tb.querySelectorAll("div.is-fs11")].find(d => /\d{3,4}/.test(d.textContent));
      // 当節成績: 枠番セル(is-fs14)以外の is-boatColorN の色番号＝着順
      const session = [...tb.querySelectorAll('td[class*="is-boatColor"]:not(.is-fs14)')]
        .map(td => +((td.className.match(/is-boatColor(\d)/) || [])[1])).filter(x => x >= 1 && x <= 6);
      const n = parseFloat;
      boats.push({
        boat,
        reg_no: rd ? +((rd.textContent.match(/\d{3,4}/) || [])[0]) : null,
        grade: rd && rd.querySelector("span") ? rd.querySelector("span").textContent.trim() : "",
        name: ((tb.querySelector(".is-fs18 a") || {}).textContent || "").replace(/　/g, " ").trim(),
        avg_st: n(fl[fl.length - 1]),
        national_win: n(nat[0]), national_3con: n(nat[2]),
        local_win: n(loc[0]),
        motor_2con: n(mot[1]),
        session_results: session
      });
    });
    return boats.sort((a, b) => a.boat - b.boat);
  }

  function parseBefore(doc) {
    const before = {};
    const st = doc.querySelector("table.is-w238");
    if (st) [...st.querySelectorAll("tbody tr")].forEach(tr => {
      const num = tr.querySelector(".table1_boatImage1Number"), tm = tr.querySelector(".table1_boatImage1Time");
      if (num && tm) {
        const b = +num.textContent.trim(), raw = tm.textContent.trim();
        before[b] = before[b] || {};
        before[b].exh_st = parseFloat(raw.replace("F", "").replace(/^\./, "0."));
        before[b].exh_st_f = /F/.test(raw) || /is-fColor/.test(tm.className);
      }
    });
    doc.querySelectorAll('td[class*="is-boatColor"]').forEach(td => {
      const b = +td.textContent.trim(); if (!(b >= 1 && b <= 6)) return;
      const tb = td.closest("tbody"); if (!tb) return;
      const m = (tb.innerText || "").match(/\b([67]\.\d{2})\b/);
      if (m) { before[b] = before[b] || {}; if (before[b].exh_time == null) before[b].exh_time = parseFloat(m[1]); }
    });
    return before;
  }

  function oddsCells(doc) { return [...doc.querySelectorAll("td")].filter(td => /oddsPoint/.test(td.className)).map(td => td.textContent.trim()); }
  function combos2() { const c = []; for (let r = 0; r < 5; r++) for (let f = 1; f <= 6; f++) c.push([f, [1, 2, 3, 4, 5, 6].filter(x => x !== f)[r]]); return c; }
  function combos3() {
    const cp = f => { const p = []; for (let j = 1; j <= 6; j++) { if (j === f) continue; for (let k = 1; k <= 6; k++) { if (k === f || k === j) continue; p.push([j, k]); } } return p; };
    const cols = {}; for (let f = 1; f <= 6; f++) cols[f] = cp(f);
    const c = []; for (let r = 0; r < 20; r++) for (let f = 1; f <= 6; f++) c.push([f, ...cols[f][r]]); return c;
  }
  function parseOdds(d1, d2, d3) {
    const out = { tansho: {}, fukusho: {}, rensho_2t: {}, rensho_2f: {}, rensho_3t: {} };
    const v1 = oddsCells(d1); for (let i = 0; i < 6 && i < v1.length; i++) { const x = parseFloat(v1[i]); if (!isNaN(x) && x > 0) out.tansho[i + 1] = x; }
    const v2 = oddsCells(d2);
    combos2().forEach(([i, j], k) => { if (k < v2.length) { const x = parseFloat(v2[k]); if (!isNaN(x) && x > 0) out.rensho_2t[`${i}-${j}`] = x; } });
    // 2連複: odds2tfページの2連単30点の後ろに15点（三角配置 r=2..6 × c=1..r-1、文書順 1-2,1-3,2-3,...）
    const c2f = []; for (let r = 2; r <= 6; r++) for (let c = 1; c < r; c++) c2f.push([c, r]);
    c2f.forEach(([a, b], k) => { const x = parseFloat(v2[30 + k]); if (!isNaN(x) && x > 0) out.rensho_2f[`${a}-${b}`] = x; });
    const v3 = oddsCells(d3); combos3().forEach(([i, j, k], idx) => { if (idx < v3.length) { const x = parseFloat(v3[idx]); if (!isNaN(x) && x > 0) out.rensho_3t[`${i}-${j}-${k}`] = x; } });
    return out;
  }

  // 結果ページのパース（1-3着の艇番＋決まり手）— ログの自己完結用
  function parseResult(doc) {
    const t = doc.querySelector("table.is-w495"); if (!t) return null;
    const lanes = [...t.querySelectorAll("tbody tr")].map(tr => {
      const bc = tr.querySelector('[class*="is-boatColor"]');
      return bc ? +((bc.className.match(/is-boatColor(\d)/) || [])[1]) : null;
    });
    if (lanes.length < 3 || !lanes[0]) return null;
    const th = [...doc.querySelectorAll("th")].find(e => e.textContent.trim() === "決まり手");
    const tbl = th ? th.closest("table") : null, vc = tbl ? tbl.querySelector("tbody td") : null;
    return { t1: lanes[0], t2: lanes[1], t3: lanes[2], km: vc ? vc.textContent.trim() : null };
  }

  // ---------- 端末内ログ（自前データの堀。サーバー送信なし） ----------
  const bbLog = {
    key: `${JCD}_${HD}_${RNO}`,
    async _all() { try { return (await chrome.storage.local.get("bbLog")).bbLog || {}; } catch (e) { return {}; } },
    async _set(o) { try { await chrome.storage.local.set({ bbLog: o }); } catch (e) {} },
    async record(res, tickets) {
      try {
        const store = await this._all(), ex = store[this.key] || {};
        const boats = res.rows.map(d => ({ b: d.boat, nm: (d.name || "").trim(), g: d.grade, tan: d._tansho,
          exST: d._exhSTn, exT: d._exhTn, dist: +d._dist.toFixed(2), tag: d._tag }));
        const buys = tickets ? tickets.combos.map(c => ({ a: c.a, b: c.b, tier: c.tier, od: c.od ?? null })) : [];
        store[this.key] = { id: this.key, jcd: +JCD, rno: +RNO, hd: HD,
          t: ex.t || Date.now(), updated: Date.now(),
          mode: root.querySelector("#bb-method").checked ? "boost" : "std",
          haveST: !!res.haveST, boats, buys, result: ex.result || null };
        await this._set(store); this.updateChip();
      } catch (e) {}
    },
    async fill(result) {
      try { const store = await this._all(), ex = store[this.key]; if (!ex || ex.result) return;
        ex.result = result; ex.updated = Date.now(); store[this.key] = ex; await this._set(store); this.updateChip(); } catch (e) {}
    },
    async updateChip() {
      const el = root.querySelector("#bb-logn"); if (!el) return;
      const all = await this._all(), n = Object.keys(all).length, done = Object.values(all).filter(x => x.result).length;
      el.textContent = n ? `記録 ${n}（結果${done}）` : "";
    },
    async exportJSON() {
      const all = await this._all();
      const blob = new Blob([JSON.stringify(all, null, 2)], { type: "application/json" });
      const u = URL.createObjectURL(blob), a = document.createElement("a");
      a.href = u; a.download = `boatbrain_log_${new Date().toISOString().slice(0, 10)}.json`;
      document.body.appendChild(a); a.click(); setTimeout(() => { a.remove(); URL.revokeObjectURL(u); }, 3000);
    }
  };

  // ---------- analyze ----------
  function zscores(arr) {
    const v = arr.map(x => (x == null || isNaN(x)) ? null : x), ok = v.filter(x => x != null);
    if (ok.length < 2) return v.map(() => 0);
    const m = ok.reduce((a, b) => a + b, 0) / ok.length, sd = Math.sqrt(ok.reduce((a, b) => a + (b - m) ** 2, 0) / ok.length) || 1;
    return v.map(x => x == null ? 0 : (x - m) / sd);
  }
  function rankOf(a, asc) { const idx = a.map((v, i) => [v, i]).sort((x, y) => asc ? x[0] - y[0] : y[0] - x[0]); const r = []; idx.forEach((p, k) => r[p[1]] = k + 1); return r; }
  function venuePct(x) { return x == null ? "—" : (x * 100).toFixed(1) + "%"; }

  function analyze(boats, odds, before, useMethod) {
    const tansho = (odds && odds.tansho) || {};
    const haveExh = before && Object.values(before).some(b => b && b.exh_time != null);
    const haveST = before && Object.values(before).some(b => b && b.exh_st != null);
    const exhTime = boats.map(b => before && before[b.boat] ? before[b.boat].exh_time : null);
    const exhST = boats.map(b => before && before[b.boat] ? before[b.boat].exh_st : null);
    const exhF = boats.map(b => !!(before && before[b.boat] && before[b.boat].exh_st_f));
    // フライング艇の展示STは“速いST”として仕上がりに加点しない（信号上は無効＝中立。表示は F付きで残す）
    const exhST_sig = exhST.map((v, i) => exhF[i] ? null : v);
    const stDelta = boats.map((b, i) => (b.avg_st != null && exhST_sig[i] != null) ? (b.avg_st - exhST_sig[i]) : null);
    const momentum = boats.map(b => { const s = b.session_results || []; return s.length ? -(s.reduce((a, c) => a + c, 0) / s.length) : null; });
    const zExhT = zscores(exhTime).map(z => -z), zExhAbs = zscores(exhST_sig).map(z => -z), zStD = zscores(stDelta);
    // 実力＝枠(想定コース)での1着率「−」コース平均（公式3年プロファイル）。コース平均を引くことで枠有利の再混入を防ぎ、純粋な“その枠での強さ”を反映。プロファイル無しは0(平均)。読み込み前は全国勝率で代用。
    const BASE_C = { 1: 55, 2: 14, 3: 13, 4: 11, 5: 6, 6: 2 };
    const haveProf = !!BBPROF;
    const ability = boats.map(b => {
      const pr = (BBPROF && b.reg_no) ? BBPROF[String(b.reg_no)] : null;
      if (pr && pr.cw && pr.cn) {
        const idx = b.boat - 1, wp = parseFloat(pr.cw[idx]), nn = +pr.cn[idx];
        if (!isNaN(wp) && nn >= 10) return wp - (BASE_C[b.boat] || 0);
      }
      return haveProf ? 0 : (b.national_win ?? null);
    });
    const zMom = zscores(momentum), zMot = zscores(boats.map(b => b.motor_2con ?? null)), zAbi = zscores(ability), zVen = zscores(boats.map(b => b.local_win ?? null));
    // まくり型: 外枠(3-6)で、勝ち方のまくり率が35%以上の選手（荒れ要因＝まくりの担い手）
    const mkType = boats.map(b => {
      const pr = (BBPROF && b.reg_no) ? BBPROF[String(b.reg_no)] : null;
      const mr = (pr && pr.w) ? pr.km[1] / pr.w : 0;
      return b.boat >= 3 && mr >= 0.35;
    });
    let w, zST;
    if (useMethod) { zST = zStD; w = { exhS: .32, exhT: .16, mom: .20, mot: .12, abi: .12, ven: .08 }; }
    else { zST = zExhAbs; w = { exhS: .18, exhT: .22, mom: .22, mot: .14, abi: .14, ven: .10 }; }
    // 検証結果(287艇/48R): 展示F艇は本番で再フライング0%・本番STは普通(平均並み)。よって"F減点"はせず、展示STの中立化のみで扱う。
    const form = boats.map((_, i) => w.exhS * zST[i] + w.exhT * zExhT[i] + w.mom * zMom[i] + w.mot * zMot[i] + w.abi * zAbi[i] + w.ven * zVen[i]);
    const inv = boats.map(b => { const o = tansho[b.boat]; return (o && o > 0) ? 1 / o : null; });
    const sInv = inv.reduce((a, b) => a + (b || 0), 0) || 1, pop = inv.map(x => x == null ? null : x / sInv);
    const zForm = zscores(form), zPop = zscores(pop), dist = boats.map((_, i) => zForm[i] - zPop[i]);
    const fr = rankOf(form, false), pr = rankOf(pop.map(x => x == null ? -1 : x), false);
    return { haveST, haveExh, rows: boats.map((b, i) => {
      const f = fr[i], p = pr[i];
      // 歪み基準: 歪み大＋人気薄=ロマン、歪みマイナス大＋人気=罠、仕上がり上位＋人気=CORE
      let tag = (dist[i] >= 0.8 && p >= 3) ? "roman" : (dist[i] <= -0.8 && p <= 3) ? "trap" : (f <= 2 && p <= 2) ? "core" : "hedge";
      // 各艇の理由をデータから自動生成
      const _sigz = { "展示ST": zST[i], "展示タイム": zExhT[i], "当節成績": zMom[i], "モーター": zMot[i], "コース実力": zAbi[i], "当地": zVen[i] };
      // 当節成績は「相対的に上位」かつ「絶対的にも平均2.5着以内」のときだけ強みに挙げる（“一番マシ＝好調”の誤表示を防ぐ）
      const strong = Object.entries(_sigz).filter(e => e[1] >= 0.7
        && !(exhF[i] && e[0] === "展示ST")
        && !(e[0] === "当節成績" && !(momentum[i] != null && momentum[i] >= -2.5))
      ).sort((a, b) => b[1] - a[1]).map(e => e[0]).slice(0, 2);
      const weak = Object.entries(_sigz).filter(e => e[1] <= -0.7).sort((a, b) => a[1] - b[1]).map(e => e[0]).slice(0, 2);
      const popP = p === 1 ? "最人気" : `人気${p}番手`;
      const reason = tag === "core" ? `${popP}。${strong.join("・") || "各要素"}が高く、市場と当日がかみ合う堅い軸。`
        : tag === "roman" ? `${popP}と薄いが、${strong.join("・") || "当日要素"}が良い。市場が見落とすロマン。`
        : tag === "trap" ? `${popP}だが、${weak.join("・") || "当日要素"}が弱く、市場の評価に当日の仕上がりが届かない。`
        : `突出した強み・弱みが小さく、市場と概ね一致。`;
      // サプライズ: 枠の常識を破る艇（内枠1-2で仕上がり下位=危険 / 外枠5-6で人気上位=市場が何か見ている）
      const fPct = (boats.length - f) / (boats.length - 1);
      const _surprise = ((b.boat === 1 || b.boat === 2) && fPct <= 0.34) ? "内枠なのに低調"
        : ((b.boat === 5 || b.boat === 6) && p <= 2) ? "外枠なのに人気" : null;
      return { ...b, _reason: reason, _surprise, _formPct: fPct, _popPct: (boats.length - p) / (boats.length - 1),
        _dist: dist[i], _tag: tag, _fr: f, _pr: p, _exF: exhF[i], _tansho: tansho[b.boat] ?? null,
        _mkType: mkType[i], _exhSTn: exhST[i], _exhTn: exhTime[i],
        _sig: { "展示T": exhTime[i], "展示ST": (exhST[i] == null ? null : (exhF[i] ? "F" : "") + exhST[i].toFixed(2)),
          "平均ST": (b.avg_st != null ? b.avg_st.toFixed(2) : null), "当節": ((b.session_results || []).join("・") || "—"),
          "モーター": b.motor_2con, "全国": b.national_win, "当地": (b.local_win != null ? b.local_win : "—") } };
    }).sort((a, b) => b._dist - a._dist) };
  }

  // ---------- render ----------
  function radarSVG(data, tickets) {
    const W = 640, H = 470, L = 66, R = 128, T = 42, B = 58, pw = W - L - R, ph = H - T - B, PAD = .07, q = p => PAD + p * (1 - 2 * PAD);
    const x = p => L + q(p) * pw, y = p => T + (1 - q(p)) * ph, col = t => ({ core: "#21406b", hedge: "#7a6a3a", roman: "#d8472b", trap: "#9a9488" })[t];
    const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
    let s = `<svg viewBox="0 0 ${W} ${H}" role="img">`;
    s += `<defs>` + [["0", "#21406b"], ["1", "#c69a3a"], ["2", "#d8472b"]].map(([id, c]) =>
      `<marker id="bb-ah-${id}" markerWidth="9" markerHeight="9" refX="6.5" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="${c}"/></marker>`).join("") + `</defs>`;
    s += `<polygon points="${L},${T} ${L + pw},${T} ${L},${T + ph}" fill="#d8472b" opacity="0.07"/>`;
    s += `<polygon points="${L + pw},${T} ${L + pw},${T + ph} ${L},${T + ph}" fill="#6b6453" opacity="0.05"/>`;
    for (let i = 0; i <= 4; i++) { const gx = L + pw * i / 4, gy = T + ph * i / 4;
      s += `<line x1="${gx}" y1="${T}" x2="${gx}" y2="${T + ph}" stroke="#e7dcc0"/>`;
      s += `<line x1="${L}" y1="${gy}" x2="${L + pw}" y2="${gy}" stroke="#e7dcc0"/>`; }
    s += `<rect x="${L}" y="${T}" width="${pw}" height="${ph}" fill="none" stroke="#cdbd98" stroke-width="1.5"/>`;
    s += `<line x1="${L}" y1="${T + ph}" x2="${L + pw}" y2="${T}" stroke="#c69a3a" stroke-width="1.5" stroke-dasharray="5 4"/>`;
    s += `<text x="${L + 12}" y="${T + 25}" style="font-size:14px;fill:#d8472b;letter-spacing:.14em">狙い目</text>`;
    s += `<text x="${L + 12}" y="${T + 41}" style="font-size:10px;fill:#b78262">人気以上に走れる</text>`;
    s += `<text x="${L + pw - 12}" y="${T + ph - 14}" style="font-size:12px;fill:#7a7363;text-anchor:end">過信注意</text>`;
    s += `<text x="${L}" y="${H - 22}" style="font-size:12px;fill:#5b7aa6">← 人気薄（穴）</text>`;
    s += `<text x="${L + pw / 2}" y="${H - 22}" style="font-size:11px;fill:#8a7f6c;text-anchor:middle">市場の人気（単勝）</text>`;
    s += `<text x="${L + pw}" y="${H - 22}" style="font-size:12px;fill:#5b7aa6;text-anchor:end">本命（人気）→</text>`;
    s += `<text x="14" y="${T + 9}" style="font-size:11px;fill:#5b7aa6">高</text>`;
    s += `<text x="14" y="${T + ph}" style="font-size:11px;fill:#5b7aa6">低</text>`;
    s += `<text transform="rotate(-90 30 ${T + ph / 2})" x="30" y="${T + ph / 2}" text-anchor="middle" style="font-size:11px;fill:#5b7aa6">仕上がり</text>`;
    const nodes = data.map(d => ({ d, cx: x(d._popPct), cy: y(d._formPct), side: d._popPct <= 0.6 ? 1 : -1, ly: y(d._formPct) }));
    [1, -1].forEach(sv => { const g = nodes.filter(n => n.side === sv).sort((a, b) => a.ly - b.ly);
      for (let i = 1; i < g.length; i++) if (g[i].ly - g[i - 1].ly < 24) g[i].ly = g[i - 1].ly + 24;
      const over = g.length ? g[g.length - 1].ly - (T + ph - 6) : 0; if (over > 0) g.forEach(n => n.ly -= over); });
    nodes.forEach(n => { const lx = n.side === 1 ? n.cx + 24 : n.cx - 24, anc = n.side === 1 ? "start" : "end", tx = lx + (n.side === 1 ? 2 : -2);
      s += `<line x1="${n.cx}" y1="${n.cy}" x2="${lx}" y2="${n.ly}" stroke="#d3c39e" stroke-width="1"/>`;
      s += `<text x="${tx}" y="${n.ly - 2}" style="font-size:12.5px;fill:#2a2520;text-anchor:${anc}">${n.d.boat} ${esc((n.d.name || "").trim())}</text>`;
      s += `<text x="${tx}" y="${n.ly + 12}" style="font-size:9.5px;fill:#8a7f6c;text-anchor:${anc}">${TAGJP[n.d._tag]} ${n.d._dist >= 0 ? "+" : ""}${n.d._dist.toFixed(2)}</text>`; });
    // 推奨3点の着順矢印（実オッズ付き）。矢じりが円に隠れないよう端を円の手前で止める。
    let arrowLabels = "";
    if (tickets && tickets.combos) {
      const pos = {}; nodes.forEach(n => pos[n.d.boat] = { x: n.cx, y: n.cy });
      const rr = 18;
      tickets.combos.forEach((c, idx) => {
        const A = pos[c.a], Bp = pos[c.b]; if (!A || !Bp) return;
        const dx = Bp.x - A.x, dy = Bp.y - A.y, len = Math.hypot(dx, dy) || 1, ux = dx / len, uy = dy / len;
        const x1 = A.x + ux * rr, y1 = A.y + uy * rr, x2 = Bp.x - ux * rr, y2 = Bp.y - uy * rr;
        s += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c.color}" stroke-width="3" opacity="0.9" marker-end="url(#bb-ah-${c.ti})"/>`;
        // ラベルは線の中点から垂直に少しずらし、最前面に描く（円や艇名と重なっても読める）
        const mx = (x1 + x2) / 2 - uy * 13, my = (y1 + y2) / 2 + ux * 13;
        const lab = `${c.tier}${c.od != null ? " ×" + c.od : ""}`, w = lab.length * 7.2 + 12;
        arrowLabels += `<rect x="${mx - w / 2}" y="${my - 9}" width="${w}" height="16" rx="3" fill="#fffdf6" opacity="0.97" stroke="${c.color}" stroke-width="0.7"/>`;
        arrowLabels += `<text x="${mx}" y="${my + 2.5}" style="font-size:11px;font-weight:700;fill:${c.color};text-anchor:middle;font-family:sans-serif">${lab}</text>`;
      });
    }
    nodes.forEach(n => { const c = col(n.d._tag);
      if (n.d._tag === "roman") s += `<circle cx="${n.cx}" cy="${n.cy}" r="21" fill="#d8472b" opacity="0.16"/>`;
      s += `<circle cx="${n.cx}" cy="${n.cy}" r="15" fill="${c}" stroke="${n.d._tag === "roman" ? "#c69a3a" : "#fff"}" stroke-width="${n.d._tag === "roman" ? 3 : 2}" data-toban="${n.d.reg_no}" style="cursor:pointer"/>`;
      s += `<text x="${n.cx}" y="${n.cy + 5}" data-toban="${n.d.reg_no}" style="font-size:15px;fill:#fff;text-anchor:middle;font-family:sans-serif;font-weight:700;cursor:pointer">${n.d.boat}</text>`;
      if (n.d._surprise) s += `<circle cx="${n.cx + 13}" cy="${n.cy - 13}" r="7.5" fill="#c69a3a" stroke="#fff" stroke-width="1.5"/><text x="${n.cx + 13}" y="${n.cy - 9}" style="font-size:11px;fill:#fff;text-anchor:middle;font-weight:700;font-family:sans-serif">!</text>`; });
    s += arrowLabels; // 矢印ラベルを最前面に
    return s + "</svg>";
  }
  function cardHTML(d) {
    const sign = d._dist >= 0 ? "bb-pos" : "bb-neg";
    const bars = Object.entries(d._sig).map(([k, v]) => `<span class="bb-b">${k} <b>${v == null ? "—" : v}</b></span>`).join("");
    return `<div class="bb-card" data-toban="${d.reg_no}" title="クリックで選手の公式プロファイル">` +
      `<div class="bb-lane bb-l${d.boat}">${d.boat}</div>` +
      `<div><div class="bb-nm">${(d.name || "—").trim()}<span class="bb-g">${d.grade || "—"} ／ 単勝 ${d._tansho ?? "—"}</span></div>` +
      `<div class="bb-read">${d._reason}${d._tag === "roman" && d._mkType ? ' <b style="color:#c69a3a">まくり型の穴</b>' : ""}${d._exF ? ' <b style="color:#d8472b">⚠展示F</b>' : ""}${d._surprise ? ` <b style="color:#c69a3a">！${d._surprise}</b>` : ""}</div>` +
      `<div class="bb-bars">${bars}</div></div>` +
      `<div class="bb-right"><span class="bb-chip bb-${d._tag}">${TAGJP[d._tag]}</span>` +
      `<span class="bb-dist ${sign}">ロマン指数 <b>${d._dist >= 0 ? "+" : ""}${d._dist.toFixed(2)}</b></span></div></div>`;
  }
  // 推奨3点を計算（レーダーの矢印・買い目リスト・ログで共有）。ロマン不在なら null。
  function computeTickets(data, odds) {
    const partners = data.filter(d => d._tag === "roman").slice(0, 2);
    if (partners.length === 0) return null;
    const od2 = (odds && odds.rensho_2t) || {};
    const core = data.filter(d => d._tag === "core").sort((a, b) => a._pr - b._pr)[0] || data.slice().sort((a, b) => a._pr - b._pr)[0];
    const byPop = data.slice().sort((a, b) => a._pr - b._pr);
    const ninki = byPop[0], r1 = partners[0];
    const jiku = (core && core._tag === "core") ? core
      : (data.filter(d => d._tag !== "roman" && d._tag !== "trap").sort((a, b) => b._formPct - a._formPct)[0]
        || data.filter(d => d._tag !== "roman").sort((a, b) => b._formPct - a._formPct)[0]
        || ninki);
    const ana = partners[1]
      || data.filter(d => d.boat !== jiku.boat && d.boat !== r1.boat && d.boat !== ninki.boat).sort((a, b) => b._formPct - a._formPct)[0]
      || ninki;
    const kTail = (ninki.boat !== jiku.boat) ? jiku : (byPop[1] || jiku);
    const seen = new Set();
    const combos = [[ninki.boat, kTail.boat], [jiku.boat, r1.boat], [r1.boat, ana.boat]]
      .filter(([a, b]) => a !== b && !seen.has(a + "-" + b) && seen.add(a + "-" + b))
      .map(([a, b]) => ({ a, b, od: od2[`${a}-${b}`] }))
      .sort((x, y) => (x.od ?? 1e9) - (y.od ?? 1e9));
    const tiers = [["堅実", "#21406b"], ["ロマン", "#c69a3a"], ["万舟", "#d8472b"]];
    combos.forEach((c, i) => { const ti = Math.min(i, tiers.length - 1); c.tier = tiers[ti][0]; c.color = tiers[ti][1]; c.ti = ti; });
    return { combos, ninki, jiku, r1 };
  }
  function ticketsHTML(data, odds) {
    const nm = p => `${p.boat} ${(p.name || "").trim()}`;
    const t = computeTickets(data, odds);
    if (!t) {
      const core = data.filter(d => d._tag === "core").sort((a, b) => a._pr - b._pr)[0] || data.slice().sort((a, b) => a._pr - b._pr)[0];
      return `<div class="bb-note">このレースは明確なロマンが見当たりません。市場と仕上がりが概ね一致＝<b style="color:#d8472b">うまみが薄い</b>。無理に広げず、本命で堅く・または見送りが筋です。${core ? ` 強いて狙うなら軸＝<b style="color:#21406b">${nm(core)}</b>。` : ""}</div>`;
    }
    const tk = t.combos.map(c =>
      `<div class="bb-ticket"><span class="bb-ty" style="color:${c.color}">${c.tier}</span><span class="bb-cmb">${c.a}-${c.b}</span><span class="bb-od">${c.od != null ? "×" + c.od : "—"}</span></div>`).join("");
    return `<div class="bb-note" style="margin-top:0">人気=<b>${nm(t.ninki)}</b> ／ 軸=<b style="color:#21406b">${nm(t.jiku)}</b> ／ ロマン=<b style="color:#d8472b">${nm(t.r1)}</b></div>` +
      `<div class="bb-tk" style="margin-top:8px">${tk}</div>` +
      `<div class="bb-note">2連単（頭→2着）。実オッズの安い順に 堅実→ロマン→万舟。3着は出さない。ロマンが無ければ見送り。<b>レーダー上に同じ3点を矢印</b>で表示（向き＝着順、左へ長いほど高配当）。</div>`;
  }

  // ---------- 新ビュー: 物語の見出し ＋ 市場との温度差 ＋ 展示データ ----------
  function storyOf(data) {
    const ninki = data.find(d => d._pr === 1);
    const romans = data.filter(d => d._tag === "roman");
    const core = data.find(d => d._tag === "core");
    const cor = t => `<b style="color:#d8472b">${t}</b>`;
    const nav = t => `<b style="color:#5b7aa6">${t}</b>`;
    const rlist = romans.slice(0, 3).map(r => r.boat).join("・");
    let head, sub;
    if (ninki && ninki._tag === "trap" && romans.length >= 1) {
      head = "主役交代 ― 本命あやうし";
      sub = `人気先頭の${nav(ninki.boat + "号")}（${ninki.grade || "—"}・${ninki._tansho ?? "—"}倍）は仕上がり中位で過信注意。展示で上回る${cor(rlist)}が割って入る波乱含み。`;
    } else if (romans.length >= 1 && romans[0].boat >= 5) {
      head = "外の怪物 ― 外から穴";
      sub = `外枠の${cor(romans[0].boat + "号")}が展示上位。人気は内に偏るが、外から差す一発に妙味。`;
    } else if (core && ninki && core.boat === ninki.boat && romans.length === 0) {
      head = "教科書 ― 本命堅し";
      sub = `${nav(ninki.boat + "号")}（${ninki.grade || "—"}・${ninki._tansho ?? "—"}倍）が実力・展示・人気で一致。波乱の芽は小さい堅い一戦。`;
    } else if (romans.length >= 2) {
      head = "波乱含み ― 横一線";
      sub = `抜けた軸が不在で${cor(rlist)}が拮抗。市場の評価と当日の仕上がりのズレが大きい。`;
    } else if (romans.length === 1) {
      head = "本命＋穴 ― ひと押しの妙味";
      sub = `本命は${ninki ? nav(ninki.boat + "号") : "内枠"}。展示で見直したい穴は${cor(romans[0].boat + "号")}。`;
    } else {
      head = "大きな歪みなし";
      sub = "市場の人気と当日の仕上がりが概ね一致。無理に穴を狙う場面ではない。";
    }
    return { head, sub };
  }
  // 荒れ指数: 本命の堅さ＋外のまくり型ロマンから「荒れやすさ」を推定（検証: 荒れの主因は決まり手）
  function areIndex(data) {
    const ninki = data.find(d => d._pr === 1);
    const romans = data.filter(d => d._tag === "roman");
    const mkR = romans.filter(d => d._mkType);
    let sc = 0;
    if (ninki) sc += (ninki._tag === "trap") ? 2 : (1 - ninki._formPct) * 2;
    sc += Math.min(romans.length, 3) * 0.8 + mkR.length * 1.2;
    const level = sc >= 3.2 ? "高" : sc >= 1.6 ? "中" : "低";
    const why = level === "低" ? "本命が堅く、穴の脅威も小さい"
      : `${ninki && ninki._tag === "trap" ? "本命が過信注意" : "本命の仕上がりに不安"}${mkR.length ? "＋外にまくり型の穴" : (romans.length ? "＋ロマンあり" : "")}`;
    return { level, why };
  }
  function storyPanel(data) {
    const st = storyOf(data), ar = areIndex(data);
    return `<div class="bb-panel bb-storypanel">` +
      `<div class="bb-story"><div class="bb-story-k">きょうの物語<span class="bb-are bb-are-${ar.level}">荒れ度 ${ar.level}</span></div>` +
      `<div class="bb-story-h">${st.head}</div><div class="bb-story-s">${st.sub}</div>` +
      `<div class="bb-are-why">荒れ度の根拠：${ar.why}</div></div></div>`;
  }

  function render(res) {
    const um = root.querySelector("#bb-method").checked;
    root.querySelector("#bb-mode").textContent = (res.haveST ? "直前（展示ST反映）" : res.haveExh ? "直前（展示タイム）" : "事前") + (um ? "・展示STブースト[実験]" : "・標準");
    const data = res.rows;
    const tickets = computeTickets(data, window.__bbRace.odds);
    root.querySelector("#bb-out").innerHTML =
      storyPanel(data) +
      '<div class="bb-panel"><h4>ロマンレーダー（散布図）</h4>' +
      '<div class="bb-legend"><span><i style="background:#21406b"></i>軸＝堅い本命</span><span><i style="background:#d8472b;box-shadow:0 0 0 2px #c69a3a"></i>ロマン＝うまみのある穴</span><span><i style="background:#7a6a3a"></i>様子見＝偏り小さい</span><span><i style="background:#9a9488"></i>過信注意＝人気倒れ</span></div>' +
      radarSVG(data, tickets) +
      '<div class="bb-note">横＝人気（右ほど本命）、縦＝当日の仕上がり。金の点線より上・左ほど狙い目。<b style="color:#c69a3a">！</b>＝枠の常識を破る注目艇。<b>矢印＝推奨3点（実オッズ付き／向き＝着順、左へ長いほど高配当）。</b></div></div>' +
      '<div class="bb-panel"><h4>ロマン指数ランキング</h4>' + data.map(cardHTML).join("") + "</div>" +
      '<div class="bb-panel"><h4>3点圧縮</h4>' + ticketsHTML(data, window.__bbRace.odds) + "</div>";
    bbLog.record(res, tickets);
  }
  function rerender() { if (window.__bbRace) render(analyze(window.__bbRace.boats, window.__bbRace.odds, window.__bbRace.before, root.querySelector("#bb-method").checked)); }

  async function run() {
    const out = root.querySelector("#bb-out");
    out.innerHTML = '<div class="bb-loading">boatrace.jp から読み込み中…（端末内で計算）</div>';
    try {
      const [rl, bf, o1, o2, o3] = await Promise.all([
        getDoc("racelist"), getDoc("beforeinfo"), getDoc("oddstf"), getDoc("odds2tf"), getDoc("odds3t")
      ]);
      const boats = parseRacelist(rl);
      if (!boats.length) { out.innerHTML = '<div class="bb-loading">出走表が読めませんでした。レースページで開いてください。</div>'; return; }
      const before = parseBefore(bf), odds = parseOdds(o1, o2, o3);
      window.__bbRace = { boats, before, odds };
      rerender();
      // 結果が出ていれば端末内ログに追記（自己完結。読み＋買い目＋結果が貯まる）
      getDoc("raceresult").then(rd => { const r = parseResult(rd); if (r) bbLog.fill(r); }).catch(() => {});
    } catch (e) {
      out.innerHTML = '<div class="bb-loading">取得に失敗しました。少し待って再試行してください。</div>';
    }
  }

  bbLog.updateChip();
})();
}catch(e){alert('ロマンレーダー初期化エラー: '+e);}setTimeout(function(){var f=document.getElementById('bb-fab');if(f)f.click();},500);})();