"""
競艇データ毎日自動収集スクリプト
=================================
Cron で毎日実行することで、以下を自動蓄積する:
  1. 開催前（前夜）: 出走表（選手名・モーター・勝率・F/L）
  2. 発走30分前:     オッズ（単勝・2連単・3連単）
  3. 発走10分前:     直前情報（展示ST・展示タイム）
  4. レース後:       結果（着順・払戻金）

蓄積先:
  data/
    racelist/  YYYYMMDD_jcd_RR.json   出走表
    odds/      YYYYMMDD_jcd_RR.json   オッズ
    before/    YYYYMMDD_jcd_RR.json   直前情報
    result/    YYYYMMDD_jcd_RR.json   結果
    daily/     YYYYMMDD.csv           日次サマリ CSV

Cron 設定例（crontab -e）:
  # 前夜22時: 翌日の出走表取得
  0 22 * * * python3 /path/to/kyotei_daily_collector.py --mode racelist --date tomorrow

  # 毎時: オッズ更新（発走前のみ有効データが入る）
  0 9-21 * * * python3 /path/to/kyotei_daily_collector.py --mode odds

  # 毎時10分: 直前情報
  10 9-21 * * * python3 /path/to/kyotei_daily_collector.py --mode before

  # 深夜0時: 当日の結果収集
  0 0 * * * python3 /path/to/kyotei_daily_collector.py --mode result --date yesterday
"""

import os, sys, json, time, csv, argparse, logging
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# 自作スクレイパーをインポート
sys.path.insert(0, str(Path(__file__).parent))
from kyotei_scraper import (
    fetch_venues, fetch_racelist, fetch_beforeinfo,
    fetch_odds, fetch_result, CODE_VENUE
)

# ─────────────────────────────────
# 設定
# ─────────────────────────────────

DATA_DIR   = Path("./kyotei_live_data")
LOG_FILE   = DATA_DIR / "collector.log"
MAX_WORKERS = 4          # 並列ワーカー数（公式に負荷かけすぎない）
SLEEP_SEC   = 0.5        # リクエスト間隔（秒）
RETRY_MAX   = 3          # リトライ回数

for subdir in ["racelist","odds","before","result","daily"]:
    (DATA_DIR / subdir).mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ]
)
log = logging.getLogger(__name__)


# ─────────────────────────────────
# ユーティリティ
# ─────────────────────────────────

def to_hd(date_str: str = "today") -> str:
    if date_str == "today":
        return datetime.now().strftime("%Y%m%d")
    if date_str == "yesterday":
        return (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    if date_str == "tomorrow":
        return (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
    return date_str  # YYYYMMDD 形式をそのまま返す


def save_json(data: dict, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def retry(func, *args, max_retry=RETRY_MAX, sleep=SLEEP_SEC, **kwargs):
    for attempt in range(max_retry):
        try:
            result = func(*args, **kwargs)
            time.sleep(sleep)
            return result
        except Exception as e:
            if attempt < max_retry - 1:
                log.warning(f"リトライ {attempt+1}/{max_retry}: {func.__name__} {e}")
                time.sleep(sleep * (attempt + 2))
            else:
                log.error(f"失敗: {func.__name__} args={args} {e}")
                return None
    return None


# ─────────────────────────────────
# 収集モード
# ─────────────────────────────────

def collect_racelist(hd: str):
    """出走表を全会場・全レース取得して保存"""
    log.info(f"[出走表] {hd} 開始")
    venues = retry(fetch_venues, hd) or []
    log.info(f"  開催会場: {[v['name'] for v in venues]}")

    total = ok = ng = 0
    for venue in venues:
        jcd = venue["jcd"]
        name = venue["name"]
        race_count = min(venue["race_count"], 12)

        for rno in range(1, race_count + 1):
            total += 1
            save_path = DATA_DIR / "racelist" / f"{hd}_{jcd:02d}_R{rno:02d}.json"
            if save_path.exists():
                log.debug(f"  スキップ(既存): {name} {rno}R")
                ok += 1
                continue

            boats = retry(fetch_racelist, jcd, rno, hd)
            if boats:
                save_json({
                    "venue": name, "jcd": jcd, "race_no": rno, "date": hd,
                    "boats": boats, "fetched_at": datetime.now().isoformat()
                }, save_path)
                log.info(f"  ✓ {name} {rno}R: {len(boats)}艇")
                ok += 1
            else:
                log.warning(f"  ✗ {name} {rno}R: データなし")
                ng += 1

    log.info(f"[出走表] 完了 OK={ok} NG={ng} / {total}件")
    return ok, ng


def collect_odds(hd: str):
    """全会場・全レースのオッズを取得（発走前のみ有効値）"""
    log.info(f"[オッズ] {hd} 開始")
    venues = retry(fetch_venues, hd) or []

    # 出走表が既存のものだけ対象
    existing = list((DATA_DIR / "racelist").glob(f"{hd}_*.json"))
    log.info(f"  対象: {len(existing)}レース")

    ok = ng = 0
    for path in existing:
        meta = load_json(path)
        jcd  = meta.get("jcd")
        rno  = meta.get("race_no")
        name = meta.get("venue")
        if not jcd or not rno:
            continue

        save_path = DATA_DIR / "odds" / f"{hd}_{jcd:02d}_R{rno:02d}.json"

        odds = retry(fetch_odds, jcd, rno, hd)
        if odds and any(odds.get("tansho", {}).values()):
            # 0.0 以外の有効オッズがある場合のみ保存
            valid = {k: v for k,v in odds.get("tansho",{}).items() if v and v > 0}
            if valid:
                save_json({
                    "venue": name, "jcd": jcd, "race_no": rno, "date": hd,
                    "odds": odds, "fetched_at": datetime.now().isoformat()
                }, save_path)
                log.info(f"  ✓ {name} {rno}R 単勝: {valid}")
                ok += 1
            else:
                log.debug(f"  スキップ(未確定): {name} {rno}R")
        else:
            ng += 1

    log.info(f"[オッズ] 完了 OK={ok} NG={ng}")
    return ok, ng


def collect_before(hd: str):
    """直前情報（展示ST・展示タイム）を取得"""
    log.info(f"[直前情報] {hd} 開始")
    existing = list((DATA_DIR / "racelist").glob(f"{hd}_*.json"))

    ok = ng = 0
    for path in existing:
        meta = load_json(path)
        jcd  = meta.get("jcd")
        rno  = meta.get("race_no")
        name = meta.get("venue")
        if not jcd or not rno:
            continue

        save_path = DATA_DIR / "before" / f"{hd}_{jcd:02d}_R{rno:02d}.json"
        if save_path.exists():
            continue  # 既取得

        bi = retry(fetch_beforeinfo, jcd, rno, hd)
        if bi and any(v.get("exh_time") for v in bi.values()):
            save_json({
                "venue": name, "jcd": jcd, "race_no": rno, "date": hd,
                "before": bi, "fetched_at": datetime.now().isoformat()
            }, save_path)
            log.info(f"  ✓ {name} {rno}R 展示: {[(k, v.get('exh_time')) for k,v in bi.items()]}")
            ok += 1
        else:
            ng += 1

    log.info(f"[直前情報] 完了 OK={ok} NG={ng}")
    return ok, ng


def collect_result(hd: str):
    """レース結果を全件取得してCSVにまとめる"""
    log.info(f"[結果] {hd} 開始")
    existing = list((DATA_DIR / "racelist").glob(f"{hd}_*.json"))

    csv_path = DATA_DIR / "daily" / f"{hd}.csv"
    csv_rows = []
    ok = ng = 0

    for path in sorted(existing):
        meta = load_json(path)
        jcd  = meta.get("jcd")
        rno  = meta.get("race_no")
        name = meta.get("venue")
        boats = meta.get("boats", [])
        if not jcd or not rno:
            continue

        save_path = DATA_DIR / "result" / f"{hd}_{jcd:02d}_R{rno:02d}.json"

        res = retry(fetch_result, jcd, rno, hd)
        if res and res.get("finishes"):
            save_json({
                "venue": name, "jcd": jcd, "race_no": rno, "date": hd,
                "result": res, "fetched_at": datetime.now().isoformat()
            }, save_path)
            log.info(f"  ✓ {name} {rno}R 着順: {res['finishes']}")
            ok += 1

            # オッズ・直前情報・出走表を結合してCSV行を生成
            odds_data = load_json(DATA_DIR / "odds"   / f"{hd}_{jcd:02d}_R{rno:02d}.json")
            bi_data   = load_json(DATA_DIR / "before" / f"{hd}_{jcd:02d}_R{rno:02d}.json")
            tansho    = odds_data.get("odds", {}).get("tansho", {})
            bi_boats  = bi_data.get("before", {})

            finish_order = res["finishes"]
            for boat_info in boats:
                boat_no = boat_info["boat"]
                finish  = (finish_order.index(boat_no) + 1
                           if boat_no in finish_order else None)
                bi      = bi_boats.get(str(boat_no), {}) or bi_boats.get(boat_no, {})

                row = {
                    "date":         hd,
                    "venue":        name,
                    "jcd":          jcd,
                    "race_no":      rno,
                    "boat":         boat_no,
                    "reg_no":       boat_info.get("reg_no"),
                    "name":         boat_info.get("name"),
                    "grade":        boat_info.get("grade"),
                    "f_count":      boat_info.get("f_count",0),
                    "l_count":      boat_info.get("l_count",0),
                    "avg_st":       boat_info.get("avg_st"),
                    "national_win": boat_info.get("national_win"),
                    "national_2con":boat_info.get("national_2con"),
                    "local_win":    boat_info.get("local_win"),
                    "motor_no":     boat_info.get("motor_no"),
                    "motor_2con":   boat_info.get("motor_2con"),
                    "boat_no":      boat_info.get("boat_no"),
                    "boat_2con":    boat_info.get("boat_2con"),
                    "exh_st":       bi.get("exh_st"),
                    "exh_st_f":     bi.get("exh_st_f"),
                    "exh_time":     bi.get("exh_time"),
                    "tansho_odds":  tansho.get(boat_no) or tansho.get(str(boat_no)),
                    "finish":       finish,
                    "finish_1st":   int(finish == 1) if finish else 0,
                }
                csv_rows.append(row)
        else:
            log.warning(f"  ✗ {name} {rno}R: 結果なし")
            ng += 1

    # CSV 書き出し
    if csv_rows:
        fieldnames = list(csv_rows[0].keys())
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_rows)
        log.info(f"  CSV保存: {csv_path} ({len(csv_rows)}行)")

    log.info(f"[結果] 完了 OK={ok} NG={ng}")
    return ok, ng


def collect_all(hd: str):
    """全モードを順番に実行（当日の完全収集）"""
    collect_racelist(hd)
    collect_odds(hd)
    collect_before(hd)
    collect_result(hd)


# ─────────────────────────────────
# メイン
# ─────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="競艇データ自動収集")
    parser.add_argument(
        "--mode",
        choices=["racelist","odds","before","result","all"],
        default="all",
        help="収集モード"
    )
    parser.add_argument(
        "--date",
        default="today",
        help="対象日 (today/yesterday/tomorrow/YYYYMMDD)"
    )
    args = parser.parse_args()
    hd = to_hd(args.date)

    log.info(f"=== 競艇データ収集 mode={args.mode} date={hd} ===")

    if   args.mode == "racelist": collect_racelist(hd)
    elif args.mode == "odds":     collect_odds(hd)
    elif args.mode == "before":   collect_before(hd)
    elif args.mode == "result":   collect_result(hd)
    else:                         collect_all(hd)

    log.info("=== 完了 ===")
