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
    fetch_odds, fetch_result, CODE_VENUE
)

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
        result = {"venue": CODE_VENUE.get(jcd), "jcd": jcd,
                  "race_no": rno, "date": hd, "boats": boats}
        save(result, "racelist", jcd, rno, hd)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/odds")
def api_odds(jcd: int, rno: int, date: str = None):
    hd = date or today()
    try:
        odds = fetch_odds(jcd, rno, hd)
        result = {"venue": CODE_VENUE.get(jcd), "jcd": jcd,
                  "race_no": rno, "date": hd, "odds": odds}
        if any(v and float(v) > 0 for v in odds.get("tansho", {}).values()):
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

@app.get("/", response_class=HTMLResponse)
def index():
    p = Path("index.html")
    if p.exists():
        return HTMLResponse(p.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>BOAT BRAIN</h1><p>起動中...</p>")

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
