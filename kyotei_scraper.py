"""
BOAT RACE 公式データスクレイパー
=================================
公式サイト (https://www.boatrace.jp) から以下を取得:
  - 開催会場一覧
  - 出走表（選手名・登番・級別・F/L・勝率・モーター・ボート・今節成績）
  - 直前情報（展示ST・展示タイム）
  - 単勝/2連単/3連単オッズ
  - レース結果（着順・払戻金）
"""

import re, time, urllib.request
from datetime import datetime, timedelta
from typing import Optional

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
}

VENUE_CODE = {
    "桐生":1,"戸田":2,"江戸川":3,"平和島":4,"多摩川":5,"浜名湖":6,
    "蒲郡":7,"常滑":8,"津":9,"三国":10,"びわこ":11,"住之江":12,
    "尼崎":13,"鳴門":14,"丸亀":15,"児島":16,"宮島":17,"徳山":18,
    "下関":19,"若松":20,"芦屋":21,"福岡":22,"唐津":23,"大村":24,
}
CODE_VENUE = {v:k for k,v in VENUE_CODE.items()}

BASE = "https://www.boatrace.jp/owpc/pc/race"


# ─────────────────────────────────
# ユーティリティ
# ─────────────────────────────────

def _get(path: str, params: dict, timeout=12) -> str:
    qs = "&".join(f"{k}={v}" for k,v in params.items())
    url = f"{BASE}/{path}?{qs}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")

def _safe_float(s) -> Optional[float]:
    try: return float(str(s).strip())
    except: return None

def _safe_int(s) -> Optional[int]:
    try: return int(str(s).strip())
    except: return None


# ─────────────────────────────────
# 1. 開催会場取得
# ─────────────────────────────────


def fetch_race_info(jcd: int, race_no: int, date_str: str = None) -> dict:
    """締め切り時間・天候・風速・波高を取得"""
    hd = date_str or datetime.now().strftime("%Y%m%d")
    result = {"deadline": None, "weather": None, "wind_spd": None,
              "wind_dir": None, "wave_cm": None}
    try:
        # 締め切り時間は番組表から
        html = _get("racelist", {"rno": race_no, "jcd": f"{jcd:02d}", "hd": hd})
        import re as _re
        # 締切予定時刻の取得
        idx = html.find("締切予定時刻")
        if idx >= 0:
            times = _re.findall(r'(\d{2}:\d{2})', html[idx:idx+300])
            # race_no番目の時刻を取得
            if len(times) >= race_no:
                result["deadline"] = times[race_no - 1]
            elif times:
                result["deadline"] = times[-1]
    except Exception:
        pass

    try:
        # 天候・風速・波高は直前情報から
        html2 = _get("beforeinfo", {"rno": race_no, "jcd": f"{jcd:02d}", "hd": hd})
        import re as _re2
        # 天候
        w = _re2.search(r'weather1_bodyUnitImage is-weather(\d+)', html2)
        if w:
            weather_map = {"1":"晴","2":"曇り","3":"雨","4":"雪","5":"霧"}
            result["weather"] = weather_map.get(w.group(1), "不明")
        # 風速
        spd = _re2.search(r'風速</span>\s*<span[^>]*>([\d.]+)m</span>', html2)
        if spd:
            result["wind_spd"] = float(spd.group(1))
        # 波高
        wave = _re2.search(r'波高</span>\s*<span[^>]*>([\d.]+)cm</span>', html2)
        if wave:
            result["wave_cm"] = float(wave.group(1))
        # 風向
        wd = _re2.search(r'風向</span>\s*<span[^>]*>([^<]+)</span>', html2)
        if wd:
            result["wind_dir"] = wd.group(1).strip()
    except Exception:
        pass

    return result


def fetch_venues(date_str: str = None) -> list[dict]:
    """
    指定日の開催会場を返す。
    Returns: [{"jcd": 1, "name": "桐生", "race_count": 12}, ...]
    """
    hd = date_str or datetime.now().strftime("%Y%m%d")
    html = _get("index", {"hd": hd})

    # jcd が含まれるリンクを抽出
    jcds = re.findall(rf'jcd=(\d+)&(?:amp;)?hd={hd}', html)
    jcds = sorted(set(int(j) for j in jcds))

    venues = []
    for jcd in jcds:
        name = CODE_VENUE.get(jcd, f"会場{jcd}")
        # レース数はリンク数から推定（rno=1〜12）
        race_links = re.findall(rf'rno=(\d+)&(?:amp;)?jcd={jcd:02d}', html)
        race_count = max((int(r) for r in race_links), default=12)
        venues.append({"jcd": jcd, "name": name, "race_count": race_count})

    return venues


# ─────────────────────────────────
# 2. 出走表パース
# ─────────────────────────────────

def fetch_racelist(jcd: int, race_no: int, date_str: str = None) -> list[dict]:
    """
    出走表を取得し、6艇分のデータを返す。

    Returns: [{
        "boat": 1,
        "reg_no": 3467,
        "name": "森 弘行",
        "grade": "B1",
        "branch": "東京/東京",
        "age": 57,
        "weight": 52.0,
        "f_count": 0,
        "l_count": 0,
        "avg_st": 0.17,
        "national_win": 3.97,
        "national_2con": 15.38,
        "national_3con": 35.38,
        "local_win": 3.84,
        "local_2con": 18.75,
        "local_3con": 31.25,
        "motor_no": 50,
        "motor_2con": 33.33,
        "motor_3con": 49.17,
        "boat_no": 63,
        "boat_2con": 19.82,
        "boat_3con": 33.33,
        "session_results": [6],   # 今節成績（着順リスト）
    }, ...]
    """
    hd = date_str or datetime.now().strftime("%Y%m%d")
    html = _get("racelist", {"rno": race_no, "jcd": f"{jcd:02d}", "hd": hd})

    if "データがありません" in html:
        return []

    # 各艇ブロックに分割
    blocks = re.split(r'<td class="is-boatColor\d+ is-fs14"', html)
    if len(blocks) < 7:
        return []

    boats = []
    for i, block in enumerate(blocks[1:7], 1):
        b = {"boat": i}

        # 登録番号・級別
        reg_m = re.search(r'toban=(\d{4})', block)
        b["reg_no"] = int(reg_m.group(1)) if reg_m else None

        grade_m = re.search(r'<span class=" ?(?:is-fc\d+)?">([AB][12])</span>', block)
        b["grade"] = grade_m.group(1) if grade_m else ""

        # 氏名
        name_m = re.search(r'is-fs18 is-fBold">[^<]*<a[^>]*>([^<]+)</a>', block)
        b["name"] = name_m.group(1).replace('\u3000', ' ').strip() if name_m else ""

        # 支部/出身地・年齢/体重
        branch_m = re.search(r'is-fs11">([^<\n]+/[^<\n]+)\s*<br\s*/>', block)
        b["branch"] = branch_m.group(1).strip() if branch_m else ""
        age_m = re.search(r'(\d{2})歳/([\d.]+)kg', block)
        b["age"]    = int(age_m.group(1))    if age_m else None
        b["weight"] = float(age_m.group(2))  if age_m else None

        # F数/L数/平均ST
        fl_m = re.search(r'is-lineH2"[^>]*>F(\d+)\s*<br\s*/>L(\d+)\s*<br\s*/>([\d.]+)', block)
        b["f_count"] = int(fl_m.group(1))    if fl_m else 0
        b["l_count"] = int(fl_m.group(2))    if fl_m else 0
        b["avg_st"]  = float(fl_m.group(3))  if fl_m else None

        # 全国/当地/モーター/ボート の数値ブロック（<br/>区切り）
        # パターン: rowspan="4">数値<br />数値<br />数値
        num_blocks = re.findall(r'rowspan="4">([\d.]+)\s*<br\s*/>([\d.]+)\s*<br\s*/>([\d.]+)', block)
        if len(num_blocks) >= 4:
            b["national_win"],  b["national_2con"],  b["national_3con"]  = [_safe_float(x) for x in num_blocks[0]]
            b["local_win"],     b["local_2con"],     b["local_3con"]     = [_safe_float(x) for x in num_blocks[1]]
            motor_n = re.search(r'is-lineH2" rowspan="4">(\d+)\s*<br\s*/>([\d.]+)\s*<br\s*/>([\d.]+)', block)
            if motor_n:
                b["motor_no"]   = int(motor_n.group(1))
                b["motor_2con"] = float(motor_n.group(2))
                b["motor_3con"] = float(motor_n.group(3))
            else:
                b["motor_no"] = b["motor_2con"] = b["motor_3con"] = None

            # ボートNoは rowspan="4">数字 の4番目
            all_no = re.findall(r'rowspan="4">(\d{2,3})\s*\n?\s*<br\s*/>([\d.]+)\s*<br\s*/>([\d.]+)', block)
            if len(all_no) >= 2:
                b["boat_no"]   = int(all_no[-1][0])
                b["boat_2con"] = float(all_no[-1][1])
                b["boat_3con"] = float(all_no[-1][2])
            else:
                b["boat_no"] = b["boat_2con"] = b["boat_3con"] = None
        else:
            for k in ["national_win","national_2con","national_3con",
                      "local_win","local_2con","local_3con",
                      "motor_no","motor_2con","motor_3con",
                      "boat_no","boat_2con","boat_3con"]:
                b[k] = None

        # 今節成績（着順リスト）
        session = re.findall(r'<td class=" is-boatColor(\d)">', block)
        session += re.findall(r'<td class="is-boatColor(\d) ">', block)
        b["session_results"] = [int(x) for x in session if x.isdigit()]

        boats.append(b)

    return boats


# ─────────────────────────────────
# 3. 直前情報（展示ST・展示タイム）
# ─────────────────────────────────

def fetch_beforeinfo(jcd: int, race_no: int, date_str: str = None) -> dict:
    """
    直前情報（展示ST・展示タイム・進入コース）を取得。

    Returns: {
        1: {"entry_course": 1, "exh_st": 0.13, "exh_time": 6.89},
        2: {"entry_course": 2, "exh_st": 0.14, "exh_time": 6.92},
        ...
    }  ← key は枠番
    """
    hd = date_str or datetime.now().strftime("%Y%m%d")
    try:
        html = _get("beforeinfo", {"rno": race_no, "jcd": f"{jcd:02d}", "hd": hd})
    except Exception:
        return {}

    if "データがありません" in html:
        return {}

    result = {}

    # 展示情報テーブル: 枠番・選手名・進入・ST・展示タイム
    # <td class="is-boatColor1 is-fs14">１</td> ... ST ... 展示T
    boat_sections = re.split(r'<td class="is-boatColor(\d)', html)

    for idx in range(1, len(boat_sections), 2):
        try:
            boat_no = int(boat_sections[idx])
            section = boat_sections[idx+1] if idx+1 < len(boat_sections) else ""

            # 展示ST（F表示の場合も）
            st_m = re.search(r'(?:F\.)?([\d.]{3,5})</td>', section[:500])
            # 展示タイム
            time_m = re.search(r'(6\.\d{2}|7\.\d{2})</td>', section[:500])

            is_f = bool(re.search(r'F\.', section[:300]))

            result[boat_no] = {
                "exh_st":   (_safe_float(st_m.group(1)) if st_m and not is_f else None),
                "exh_st_f": is_f,
                "exh_time": _safe_float(time_m.group(1)) if time_m else None,
            }
        except (IndexError, ValueError):
            continue

    # 進入順（並び順テーブル）
    entry_m = re.findall(r'is-boatColor(\d).*?進入.*?(\d)', html, re.DOTALL)

    return result


# ─────────────────────────────────
# 4. オッズ取得
# ─────────────────────────────────

def fetch_odds(jcd: int, race_no: int, date_str: str = None) -> dict:
    """
    単勝・複勝・2連単・3連単オッズを取得。

    Returns: {
        "tansho":    {1: 1.5, 2: 17.2, ...},
        "fukusho":   {1: "1.0-1.1", ...},
        "rensho_2t": {(1,2): 7.7, ...},
        "rensho_3t": {(1,2,3): 5.3, ...},
    }
    """
    hd = date_str or datetime.now().strftime("%Y%m%d")
    params = {"rno": race_no, "jcd": f"{jcd:02d}", "hd": hd}
    out = {"tansho":{}, "fukusho":{}, "rensho_2t":{}, "rensho_3t":{}}

    # 単勝・複勝
    try:
        html = _get("oddstf", params)
        vals = re.findall(r'<td class="oddsPoint [^"]*">([\d.\-]+)</td>', html)
        if len(vals) >= 6:
            out["tansho"]  = {i+1: float(vals[i])   for i in range(6)}
            out["fukusho"] = {i+1: vals[i+6]         for i in range(6) if i+6<len(vals)}
    except Exception as e:
        pass

    # 2連単
    try:
        html2 = _get("odds2tf", params)
        vals2 = re.findall(r'<td class="oddsPoint [^"]*">([\d.]+)</td>', html2)
        combos2 = [(i,j) for i in range(1,7) for j in range(1,7) if i!=j]
        for k,(i,j) in enumerate(combos2):
            if k < len(vals2):
                try: out["rensho_2t"][(i,j)] = float(vals2[k])
                except: pass
    except Exception:
        pass

    # 3連単
    try:
        html3 = _get("odds3t", params)
        vals3 = re.findall(r'<td class="oddsPoint [^"]*">([\d.]+)</td>', html3)
        combos3 = [(i,j,k) for i in range(1,7) for j in range(1,7)
                   for k in range(1,7) if len({i,j,k})==3]
        for idx,(i,j,k) in enumerate(combos3):
            if idx < len(vals3):
                try: out["rensho_3t"][(i,j,k)] = float(vals3[idx])
                except: pass
    except Exception:
        pass

    return out


# ─────────────────────────────────
# 5. レース結果取得
# ─────────────────────────────────

def fetch_result(jcd: int, race_no: int, date_str: str = None) -> dict:
    """
    レース結果（着順・払戻金）を取得。

    Returns: {
        "finishes": [1,3,2,4,5,6],   # 着順（艇番）
        "tansho_payout": {1: 150},
        "rensho_2t_payout": {(1,3): 770},
        "rensho_3t_payout": {(1,3,2): 5300},
    }
    """
    hd = date_str or datetime.now().strftime("%Y%m%d")
    try:
        html = _get("raceresult", {"rno": race_no, "jcd": f"{jcd:02d}", "hd": hd})
    except Exception:
        return {}

    if "データがありません" in html:
        return {}

    out = {"finishes":[], "tansho_payout":{}, "rensho_2t_payout":{}, "rensho_3t_payout":{}}

    # 着順テーブル: 1着〜6着の艇番
    # <td class="is-fs14">１</td> <td>艇番</td>
    finish_m = re.findall(
        r'<td[^>]*>([１２３４５６])</td>\s*<td[^>]*>([1-6])</td>',
        html
    )
    zen_to_han = {'１':1,'２':2,'３':3,'４':4,'５':5,'６':6}
    if finish_m:
        finishes = sorted(finish_m, key=lambda x: zen_to_han.get(x[0],9))
        out["finishes"] = [int(x[1]) for x in finishes]

    # 払戻テーブル
    # 単勝: 艇番と金額
    tansho_m = re.findall(
        r'単勝.*?<td[^>]*>([1-6])</td>\s*<td[^>]*>([\d,]+)円',
        html, re.DOTALL
    )
    for boat, amount in tansho_m:
        out["tansho_payout"][int(boat)] = int(amount.replace(',',''))

    # 3連単
    san_m = re.findall(
        r'<td[^>]*>([1-6])-([1-6])-([1-6])</td>\s*<td[^>]*>([\d,]+)円',
        html
    )
    for a,b,c,amt in san_m:
        out["rensho_3t_payout"][(int(a),int(b),int(c))] = int(amt.replace(',',''))

    # 2連単
    ni_m = re.findall(
        r'<td[^>]*>([1-6])-([1-6])</td>\s*<td[^>]*>([\d,]+)円',
        html
    )
    for a,b,amt in ni_m:
        out["rensho_2t_payout"][(int(a),int(b))] = int(amt.replace(',',''))

    return out


# ─────────────────────────────────
# 6. 1レース分の全データを一括取得
# ─────────────────────────────────

def fetch_race_all(jcd: int, race_no: int, date_str: str = None,
                   include_odds: bool = True,
                   include_result: bool = False) -> dict:
    """
    1レース分の全データを取得して辞書で返す。

    Returns: {
        "venue": "桐生",
        "jcd": 1,
        "race_no": 1,
        "date": "20260615",
        "boats": [...],          # fetch_racelist の結果
        "beforeinfo": {...},     # fetch_beforeinfo の結果
        "odds": {...},           # fetch_odds の結果
        "result": {...},         # fetch_result の結果（include_result=True時）
    }
    """
    hd = date_str or datetime.now().strftime("%Y%m%d")
    out = {
        "venue":    CODE_VENUE.get(jcd, f"会場{jcd}"),
        "jcd":      jcd,
        "race_no":  race_no,
        "date":     hd,
        "boats":    [],
        "beforeinfo": {},
        "odds":     {},
        "result":   {},
    }

    # 出走表
    out["boats"] = fetch_racelist(jcd, race_no, hd)
    time.sleep(0.3)

    # 直前情報
    out["beforeinfo"] = fetch_beforeinfo(jcd, race_no, hd)
    time.sleep(0.3)

    # オッズ
    if include_odds:
        out["odds"] = fetch_odds(jcd, race_no, hd)
        time.sleep(0.3)

    # 結果
    if include_result:
        out["result"] = fetch_result(jcd, race_no, hd)

    return out


# ─────────────────────────────────
# エクスポート
# ─────────────────────────────────

__all__ = [
    "fetch_venues", "fetch_racelist", "fetch_beforeinfo",
    "fetch_odds", "fetch_result", "fetch_race_all",
    "VENUE_CODE", "CODE_VENUE",
]


if __name__ == "__main__":
    # 動作確認
    print("=== BOAT RACE スクレイパー 動作確認 ===\n")

    hd = datetime.now().strftime("%Y%m%d")

    print(f"[1] 本日({hd})の開催会場:")
    venues = fetch_venues(hd)
    for v in venues:
        print(f"    {v['name']} (jcd={v['jcd']:02d}) 最大{v['race_count']}R")

    if venues:
        jcd  = venues[0]["jcd"]
        name = venues[0]["name"]
        print(f"\n[2] {name} 1R 出走表:")
        boats = fetch_racelist(jcd, 1, hd)
        for b in boats:
            print(f"    {b['boat']}号艇 {b['name']:12s} {b['grade']} "
                  f"全国勝率={b['national_win']} F={b['f_count']} "
                  f"モーターNo={b['motor_no']} モーター2連={b['motor_2con']}")

        print(f"\n[3] {name} 1R オッズ:")
        odds = fetch_odds(jcd, 1, hd)
        print("    単勝:", odds.get("tansho"))
        print("    2連単(上位5):", list(odds.get("rensho_2t",{}).items())[:5])

        print(f"\n[4] {name} 1R 直前情報:")
        bi = fetch_beforeinfo(jcd, 1, hd)
        for boat, info in bi.items():
            print(f"    {boat}号艇: 展示ST={info.get('exh_st')} "
                  f"展示T={info.get('exh_time')} F={info.get('exh_st_f')}")
