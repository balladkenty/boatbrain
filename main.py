import os, json, logging
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
for d in ["racelist","odds","before","result"]:
    (DATA_DIR/d).mkdir(exist_ok=True)

from kyotei_scraper import (
    fetch_venues, fetch_racelist, fetch_beforeinfo,
    fetch_odds, fetch_result, fetch_race_info, CODE_VENUE
)

# 当地適性データを読み込み
import json as _json
_VENUE_STATS = {}
_venue_stats_path = Path("venue_stats.json")
if _venue_stats_path.exists():
    try:
        _VENUE_STATS = _json.loads(_venue_stats_path.read_text(encoding="utf-8"))
        log.info(f"当地適性データ読み込み: {len(_VENUE_STATS)}選手")
    except Exception as e:
        log.warning(f"venue_stats.json読み込み失敗: {e}")

def add_venue_stats(boats: list, venue: str) -> list:
    """boatsリストに当地適性を付与"""
    for b in boats:
        reg = str(b.get("reg_no", ""))
        vstats = _VENUE_STATS.get(reg, {}).get(venue, {})
        b["venue_win_rate"] = vstats.get("rate", 0.167)
        b["venue_n"] = vstats.get("n", 0)
    return boats

app = FastAPI(title="BOAT BRAIN API")
app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def today():
    return datetime.now().strftime("%Y%m%d")

def cached(cat, jcd, rno, hd):
    p = DATA_DIR/cat/f"{hd}_{jcd:02d}_R{rno:02d}.json"
    if p.exists():
        return json.loads(p.read_text())
    return None

def save(data, cat, jcd, rno, hd):
    p = DATA_DIR/cat/f"{hd}_{jcd:02d}_R{rno:02d}.json"
    p.write_text(json.dumps(data, ensure_ascii=False))

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now().isoformat(), "model": False}

@app.get("/api/venues")
def api_venues(date: str = None):
    hd = date or today()
    try:
        venues = fetch_venues(hd)
        return {"date": hd, "venues": venues}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/racelist")
def api_racelist(jcd: int, rno: int, date: str = None):
    hd = date or today()
    c = cached("racelist", jcd, rno, hd)
    if c:
        return c
    try:
        boats = fetch_racelist(jcd, rno, hd)
        venue_name = CODE_VENUE.get(jcd, "")
        boats = add_venue_stats(boats, venue_name)
        result = {"venue": venue_name, "jcd": jcd,
                  "race_no": rno, "date": hd, "boats": boats}
        save(result, "racelist", jcd, rno, hd)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

def json_safe(obj):
    if isinstance(obj, dict):
        return {
            "-".join(map(str, k)) if isinstance(k, tuple) else str(k): json_safe(v)
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [json_safe(v) for v in obj]
    return obj

@app.get("/api/odds")
def api_odds(jcd: int, rno: int, date: str = None):
    hd = date or today()
    try:
        odds = fetch_odds(jcd, rno, hd)
        safe_odds = json_safe(odds)
        result = {"venue": CODE_VENUE.get(jcd), "jcd": jcd,
                  "race_no": rno, "date": hd, "odds": safe_odds}
        if any(
            float(v) > 0
            for v in safe_odds.get("tansho", {}).values()
            if v is not None
        ):
            save(result, "odds", jcd, rno, hd)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/before")
def api_before(jcd: int, rno: int, date: str = None):
    hd = date or today()
    c = cached("before", jcd, rno, hd)
    if c:
        return c
    try:
        bi = fetch_beforeinfo(jcd, rno, hd)
        result = {"venue": CODE_VENUE.get(jcd), "jcd": jcd,
                  "race_no": rno, "date": hd, "before": bi}
        if any(v and v.get("exh_time") for v in bi.values()):
            save(result, "before", jcd, rno, hd)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/raceinfo")
def api_raceinfo(jcd: int, rno: int, date: str = None):
    hd = date or today()
    try:
        info = fetch_race_info(jcd, rno, hd)
        return {"venue": CODE_VENUE.get(jcd), "jcd": jcd,
                "race_no": rno, "date": hd, **info}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/result")
def api_result(jcd: int, rno: int, date: str = None):
    hd = date or today()
    c = cached("result", jcd, rno, hd)
    if c:
        return c
    try:
        res = fetch_result(jcd, rno, hd)
        result = {"venue": CODE_VENUE.get(jcd), "jcd": jcd,
                  "race_no": rno, "date": hd, "result": res}
        if res.get("finishes"):
            save(result, "result", jcd, rno, hd)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

HTML_CONTENT = open(Path(__file__).parent / "index.html", encoding="utf-8").read() if (Path(__file__).parent / "index.html").exists() else "<h1>BOAT BRAIN</h1><p>index.html not found</p>"

@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(HTML_CONTENT)

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from kyotei_daily_collector import (
        collect_racelist, collect_odds, collect_before, collect_result, to_hd
    )
    scheduler = BackgroundScheduler(timezone="Asia/Tokyo")
    scheduler.add_job(lambda: collect_racelist(to_hd("tomorrow")), "cron", hour=22, minute=0)
    scheduler.add_job(lambda: collect_odds(to_hd("today")), "cron", hour="9-21", minute=0)
    scheduler.add_job(lambda: collect_before(to_hd("today")), "cron", hour="9-21", minute=15)
    scheduler.add_job(lambda: collect_result(to_hd("yesterday")), "cron", hour=0, minute=30)

    @app.on_event("startup")
    def startup():
        scheduler.start()
        log.info("scheduler started")

    @app.on_event("shutdown")
    def shutdown():
        scheduler.shutdown()
except Exception as e:
    log.warning(f"scheduler error: {e}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
