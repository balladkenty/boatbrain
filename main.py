"""
BOAT BRAIN - メインアプリケーション
=====================================
FastAPI + Stripe + APScheduler による
完全自走型競艇AI予想サービス

環境変数（Renderで設定）:
  STRIPE_SECRET_KEY      Stripeシークレットキー
  STRIPE_PRICE_ID_STD    スタンダードプランの価格ID
  STRIPE_PRICE_ID_PRE    プレミアムプランの価格ID
  STRIPE_WEBHOOK_SECRET  Webhookシークレット
  JWT_SECRET             JWT署名シークレット（任意の長い文字列）
  ADMIN_EMAIL            管理者メール
"""

import os, json, time, logging, hashlib, secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
import uvicorn

# ── ロガー ──────────────────────────────────────
logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ── 環境変数 ─────────────────────────────────────
STRIPE_SECRET       = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PRICE_STD    = os.getenv("STRIPE_PRICE_ID_STD", "")
STRIPE_PRICE_PRE    = os.getenv("STRIPE_PRICE_ID_PRE", "")
STRIPE_WEBHOOK_SEC  = os.getenv("STRIPE_WEBHOOK_SECRET", "")
JWT_SECRET          = os.getenv("JWT_SECRET", secrets.token_hex(32))
DATA_DIR            = Path(os.getenv("DATA_DIR", "./data"))
MODEL_PATH          = Path(os.getenv("MODEL_PATH", "./kyotei_model_v5.pkl"))

DATA_DIR.mkdir(parents=True, exist_ok=True)
(DATA_DIR / "users").mkdir(exist_ok=True)
(DATA_DIR / "racelist").mkdir(exist_ok=True)
(DATA_DIR / "odds").mkdir(exist_ok=True)
(DATA_DIR / "before").mkdir(exist_ok=True)
(DATA_DIR / "result").mkdir(exist_ok=True)

# ── スクレイパー ──────────────────────────────────
from kyotei_scraper import (
    fetch_venues, fetch_racelist, fetch_beforeinfo,
    fetch_odds, fetch_result, CODE_VENUE, VENUE_CODE
)

# ── モデル ────────────────────────────────────────
import joblib, numpy as np
model_data = None
if MODEL_PATH.exists():
    model_data = joblib.load(MODEL_PATH)
    log.info(f"モデルロード完了: {MODEL_PATH}")
else:
    log.warning(f"モデルファイルなし: {MODEL_PATH} （軽量スコアリングで代替）")

# ── FastAPI ───────────────────────────────────────
app = FastAPI(title="BOAT BRAIN API", version="2.0", docs_url=None)

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ── ユーザーDB（JSONファイル、本番はPostgreSQLに移行） ──
def _users_path(): return DATA_DIR / "users" / "db.json"

def load_users() -> dict:
    p = _users_path()
    return json.loads(p.read_text()) if p.exists() else {}

def save_users(users: dict):
    _users_path().write_text(json.dumps(users, ensure_ascii=False, indent=2))

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

# ── JWT（シンプル実装） ───────────────────────────
import base64, hmac

def make_token(email: str, plan: str) -> str:
    payload = json.dumps({"email": email, "plan": plan,
                          "exp": (datetime.utcnow()+timedelta(days=30)).isoformat()})
    sig = hmac.new(JWT_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    token = base64.urlsafe_b64encode(
        (payload + "." + sig).encode()).decode()
    return token

def verify_token(token: str) -> Optional[dict]:
    try:
        decoded = base64.urlsafe_b64decode(token.encode()).decode()
        payload_str, sig = decoded.rsplit(".", 1)
        expected = hmac.new(JWT_SECRET.encode(),
                            payload_str.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        payload = json.loads(payload_str)
        if datetime.fromisoformat(payload["exp"]) < datetime.utcnow():
            return None
        return payload
    except Exception:
        return None

def get_user(authorization: str = Header(None)) -> Optional[dict]:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    return verify_token(authorization[7:])

def require_user(user=Depends(get_user)):
    if not user:
        raise HTTPException(401, "ログインが必要です")
    return user

def require_paid(user=Depends(require_user)):
    if user.get("plan") not in ("standard", "premium"):
        raise HTTPException(403, "有料プランへのアップグレードが必要です")
    return user

# ── レートリミット（無料: 3レース/日） ───────────────
_free_usage: dict[str, list] = {}

def check_free_limit(email: str) -> bool:
    today = datetime.now().strftime("%Y%m%d")
    key = f"{email}:{today}"
    _free_usage.setdefault(key, [])
    return len(_free_usage[key]) < 3

def record_free_usage(email: str):
    today = datetime.now().strftime("%Y%m%d")
    key = f"{email}:{today}"
    _free_usage.setdefault(key, []).append(datetime.now().isoformat())

# ══════════════════════════════════════════════════
# 認証エンドポイント
# ══════════════════════════════════════════════════

class RegisterReq(BaseModel):
    email: str
    password: str

class LoginReq(BaseModel):
    email: str
    password: str

@app.post("/auth/register")
def register(req: RegisterReq):
    users = load_users()
    if req.email in users:
        raise HTTPException(400, "このメールアドレスは登録済みです")
    users[req.email] = {
        "email":      req.email,
        "pw_hash":    hash_pw(req.password),
        "plan":       "free",
        "created_at": datetime.now().isoformat(),
        "stripe_customer_id": "",
        "stripe_subscription_id": "",
    }
    save_users(users)
    token = make_token(req.email, "free")
    return {"token": token, "plan": "free", "email": req.email}

@app.post("/auth/login")
def login(req: LoginReq):
    users = load_users()
    u = users.get(req.email)
    if not u or u["pw_hash"] != hash_pw(req.password):
        raise HTTPException(401, "メールアドレスまたはパスワードが違います")
    token = make_token(req.email, u["plan"])
    return {"token": token, "plan": u["plan"], "email": req.email}

@app.get("/auth/me")
def me(user=Depends(require_user)):
    users = load_users()
    u = users.get(user["email"], {})
    return {"email": user["email"], "plan": u.get("plan","free")}

# ══════════════════════════════════════════════════
# Stripe 決済エンドポイント
# ══════════════════════════════════════════════════

@app.post("/billing/checkout")
def create_checkout(plan: str, user=Depends(require_user)):
    """Stripeのチェックアウトセッションを作成"""
    if not STRIPE_SECRET:
        raise HTTPException(503, "決済システム未設定")
    import stripe
    stripe.api_key = STRIPE_SECRET
    price_id = STRIPE_PRICE_STD if plan == "standard" else STRIPE_PRICE_PRE

    users = load_users()
    u = users.get(user["email"], {})

    # 既存顧客またはゲスト
    customer_id = u.get("stripe_customer_id") or None
    if not customer_id:
        c = stripe.Customer.create(email=user["email"])
        customer_id = c.id
        u["stripe_customer_id"] = customer_id
        users[user["email"]] = u
        save_users(users)

    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url="https://your-domain.com/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://your-domain.com/pricing",
        metadata={"email": user["email"], "plan": plan},
    )
    return {"checkout_url": session.url}

@app.post("/billing/portal")
def customer_portal(user=Depends(require_user)):
    """Stripeカスタマーポータル（プラン変更・解約）"""
    if not STRIPE_SECRET:
        raise HTTPException(503, "決済システム未設定")
    import stripe
    stripe.api_key = STRIPE_SECRET
    users = load_users()
    u = users.get(user["email"], {})
    cid = u.get("stripe_customer_id")
    if not cid:
        raise HTTPException(400, "サブスクリプションが見つかりません")
    portal = stripe.billing_portal.Session.create(
        customer=cid,
        return_url="https://your-domain.com/mypage",
    )
    return {"portal_url": portal.url}

@app.post("/billing/webhook")
async def stripe_webhook(request: Request):
    """Stripeからの自動通知を受け取りプランを更新"""
    if not STRIPE_SECRET:
        return {"ok": True}
    import stripe
    stripe.api_key = STRIPE_SECRET
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig, STRIPE_WEBHOOK_SEC)
    except Exception as e:
        raise HTTPException(400, str(e))

    users = load_users()

    if event["type"] == "checkout.session.completed":
        meta  = event["data"]["object"].get("metadata", {})
        email = meta.get("email")
        plan  = meta.get("plan", "standard")
        sub_id = event["data"]["object"].get("subscription")
        if email and email in users:
            users[email]["plan"] = plan
            users[email]["stripe_subscription_id"] = sub_id or ""
            save_users(users)
            log.info(f"プランアップグレード: {email} → {plan}")

    elif event["type"] in ("customer.subscription.deleted",
                            "customer.subscription.paused"):
        sub = event["data"]["object"]
        cid = sub.get("customer")
        for email, u in users.items():
            if u.get("stripe_customer_id") == cid:
                users[email]["plan"] = "free"
                save_users(users)
                log.info(f"プランダウングレード（解約）: {email}")
                break

    return {"ok": True}

# ══════════════════════════════════════════════════
# レースデータ API
# ══════════════════════════════════════════════════

def today_str(): return datetime.now().strftime("%Y%m%d")

def _cached(category, jcd, rno, hd):
    p = DATA_DIR / category / f"{hd}_{jcd:02d}_R{rno:02d}.json"
    return json.loads(p.read_text()) if p.exists() else None

@app.get("/api/venues")
def api_venues(date: str = None, user=Depends(require_user)):
    hd = date or today_str()
    try:
        return {"date": hd, "venues": fetch_venues(hd)}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/racelist")
def api_racelist(jcd: int, rno: int, date: str = None,
                 user=Depends(require_user)):
    hd = date or today_str()
    # 無料プランは3レース/日まで
    if user.get("plan") == "free":
        if not check_free_limit(user["email"]):
            raise HTTPException(429, "無料プランは1日3レースまでです。アップグレードしてください。")
        record_free_usage(user["email"])

    cached = _cached("racelist", jcd, rno, hd)
    if cached: return cached
    try:
        boats = fetch_racelist(jcd, rno, hd)
        result = {"venue": CODE_VENUE.get(jcd), "jcd": jcd,
                  "race_no": rno, "date": hd, "boats": boats}
        p = DATA_DIR/"racelist"/f"{hd}_{jcd:02d}_R{rno:02d}.json"
        p.write_text(json.dumps(result, ensure_ascii=False))
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/odds")
def api_odds(jcd: int, rno: int, date: str = None,
             user=Depends(require_user)):
    hd = date or today_str()
    # オッズはプレミアムのみリアルタイム取得
    # スタンダードはキャッシュのみ
    if user.get("plan") == "free":
        return {"tansho":{}, "rensho_2t":{}, "rensho_3t":{},
                "msg": "オッズはスタンダード以上のプランで利用できます"}
    cached = _cached("odds", jcd, rno, hd)
    if cached and user.get("plan") == "standard":
        return cached.get("odds", {})
    try:
        odds = fetch_odds(jcd, rno, hd)
        result = {"venue": CODE_VENUE.get(jcd), "jcd": jcd,
                  "race_no": rno, "date": hd, "odds": odds}
        if any(v > 0 for v in odds.get("tansho", {}).values()):
            p = DATA_DIR/"odds"/f"{hd}_{jcd:02d}_R{rno:02d}.json"
            p.write_text(json.dumps(result, ensure_ascii=False))
        return odds
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/before")
def api_before(jcd: int, rno: int, date: str = None,
               user=Depends(require_user)):
    hd = date or today_str()
    cached = _cached("before", jcd, rno, hd)
    if cached: return cached
    try:
        bi = fetch_beforeinfo(jcd, rno, hd)
        result = {"venue": CODE_VENUE.get(jcd), "jcd": jcd,
                  "race_no": rno, "date": hd, "before": bi}
        if any(v and v.get("exh_time") for v in bi.values()):
            p = DATA_DIR/"before"/f"{hd}_{jcd:02d}_R{rno:02d}.json"
            p.write_text(json.dumps(result, ensure_ascii=False))
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/result")
def api_result(jcd: int, rno: int, date: str = None,
               user=Depends(require_user)):
    hd = date or today_str()
    cached = _cached("result", jcd, rno, hd)
    if cached: return cached
    try:
        res = fetch_result(jcd, rno, hd)
        result = {"venue": CODE_VENUE.get(jcd), "jcd": jcd,
                  "race_no": rno, "date": hd, "result": res}
        if res.get("finishes"):
            p = DATA_DIR/"result"/f"{hd}_{jcd:02d}_R{rno:02d}.json"
            p.write_text(json.dumps(result, ensure_ascii=False))
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# ══════════════════════════════════════════════════
# AI 予測エンドポイント
# ══════════════════════════════════════════════════

VENUE_IN_ADV = {
    "大村":0.671,"住之江":0.598,"尼崎":0.590,"徳山":0.582,"下関":0.578,
    "常滑":0.573,"蒲郡":0.571,"唐津":0.570,"芦屋":0.565,"若松":0.562,
    "福岡":0.559,"宮島":0.554,"多摩川":0.549,"桐生":0.545,"鳴門":0.540,
    "丸亀":0.538,"平和島":0.535,"浜名湖":0.530,"三国":0.528,"児島":0.525,
    "津":0.520,"びわこ":0.515,"戸田":0.480,"江戸川":0.455,
}
GRADE_SCORE = {"A1":4,"A2":3,"B1":2,"B2":1}

def _compute_probs(boats, before, odds_data, venue_name):
    in_adv  = VENUE_IN_ADV.get(venue_name, 0.54)
    tansho  = odds_data.get("tansho", {}) if odds_data else {}
    raw_impl = {int(b): 1/(o*0.75) for b,o in tansho.items() if o and float(o)>0}
    impl_tot = sum(raw_impl.values()) or 1
    impl = {b: raw_impl.get(b,0)/impl_tot if raw_impl else 1/6
            for b in [bt["boat"] for bt in boats]}

    exh_times = [
        (before.get(b["boat"]) or before.get(str(b["boat"])) or {}).get("exh_time")
        for b in boats
    ]
    valid_exh = [t for t in exh_times if t]
    exh_mean  = sum(valid_exh)/len(valid_exh) if valid_exh else 6.85

    scores = []
    for i, b in enumerate(boats):
        c   = b["boat"]
        g   = GRADE_SCORE.get(b.get("grade","B1"), 2)
        wr  = b.get("national_win") or 5.0
        mtr = (b.get("motor_2con") or 35) / 100
        bi  = before.get(c) or before.get(str(c)) or {}
        is_f= (b.get("f_count") or 0) > 0
        st  = (bi.get("exh_st") or b.get("avg_st") or 0.16)
        if is_f: st += 0.07
        exh_t = bi.get("exh_time") or exh_mean
        sess  = b.get("session_results") or []
        sess_wr = sess.count(1)/len(sess) if sess else 0.17
        imp   = impl.get(c, 1/6)

        score = (
            in_adv*(7-c)*(wr*0.35 + g*0.25 + imp*3*0.2 + sess_wr*2*0.1 + mtr*0.1)
            - st*5
            + (exh_mean - exh_t)*2
            + imp*2.5
        )
        scores.append(score)

    max_s = max(scores)
    exps  = [np.exp(s-max_s) for s in scores]
    tot   = sum(exps)
    return [e/tot for e in exps]

@app.get("/api/predict")
def api_predict(jcd: int, rno: int, date: str = None,
                bankroll: int = 10000,
                user=Depends(require_user)):
    hd = date or today_str()

    # 無料プラン制限
    if user.get("plan") == "free":
        if not check_free_limit(user["email"]):
            raise HTTPException(429, "無料プランは1日3レースまでです")
        record_free_usage(user["email"])

    venue_name = CODE_VENUE.get(jcd, "大村")

    # データ取得
    rl = _cached("racelist", jcd, rno, hd)
    boats = rl["boats"] if rl else fetch_racelist(jcd, rno, hd)

    bi_data = _cached("before", jcd, rno, hd)
    before  = bi_data.get("before",{}) if bi_data else {}
    if not before:
        try: before = fetch_beforeinfo(jcd, rno, hd)
        except: pass

    # オッズは有料のみ
    odds_data = {}
    if user.get("plan") in ("standard","premium"):
        od = _cached("odds", jcd, rno, hd)
        odds_data = od.get("odds",{}) if od else {}
        if not odds_data:
            try: odds_data = fetch_odds(jcd, rno, hd)
            except: pass

    if not boats:
        raise HTTPException(404, "出走表データがありません")

    probs = _compute_probs(boats, before, odds_data, venue_name)

    TANSHO_TAX = 0.75; RENSHO_TAX = 0.725; KELLY = 0.25; MIN_EV = 1.05
    tansho  = odds_data.get("tansho", {})
    r2t     = odds_data.get("rensho_2t", {})
    r3t     = odds_data.get("rensho_3t", {})
    has_odds = any(v and float(v)>0 for v in tansho.values())

    pmap = {b["boat"]: probs[i] for i,b in enumerate(boats)}

    # 期待値計算
    bets = []
    if has_odds and user.get("plan") in ("standard","premium"):
        # 単勝
        for b,p in pmap.items():
            o = tansho.get(b) or tansho.get(str(b))
            if not o or float(o)<=0: continue
            o=float(o)
            ev=p*o*TANSHO_TAX
            if ev<MIN_EV: continue
            k=max(0,(p*o-1)/(o-1))*KELLY
            amt=max(100,int(bankroll*k/100)*100)
            bets.append({"type":"単勝","combo":[b],"label":f"{b}号艇",
                         "odds":o,"ev":round(ev,3),"amount":amt})

        # 上位3艇の2連単・3連単
        top3 = sorted(pmap.keys(), key=lambda x:-pmap[x])[:3]
        for a in top3:
            for b_ in top3:
                if a==b_: continue
                o=r2t.get((a,b_)) or r2t.get(f"{a},{b_}") or r2t.get(str((a,b_)))
                if not o: continue
                o=float(o)
                pa,pb=pmap[a],pmap[b_]
                p2=pa*(pb/(1-pa+1e-9))
                ev=p2*o*RENSHO_TAX
                if ev<MIN_EV: continue
                k=max(0,(p2*o-1)/(o-1))*KELLY
                amt=max(100,int(bankroll*k/100)*100)
                bets.append({"type":"2連単","combo":[a,b_],"label":f"{a}-{b_}",
                             "odds":o,"ev":round(ev,3),"amount":amt})

        from itertools import permutations
        for perm in permutations(top3,3):
            a,b_,c=perm
            o=r3t.get(perm) or r3t.get(f"{a},{b_},{c}")
            if not o: continue
            o=float(o)
            pa,pb,pc=pmap[a],pmap[b_],pmap[c]
            p3=pa*(pb/(1-pa+1e-9))*(pc/(1-pa-pb+1e-9))
            ev=p3*o*RENSHO_TAX
            if ev<MIN_EV: continue
            k=max(0,(p3*o-1)/(o-1))*KELLY
            amt=max(100,int(bankroll*k/100)*100)
            bets.append({"type":"3連単","combo":list(perm),"label":f"{a}-{b_}-{c}",
                         "odds":o,"ev":round(ev,3),"amount":amt})

    bets.sort(key=lambda x:-x["ev"])
    top3_boats = sorted(pmap.keys(), key=lambda x:-pmap[x])[:3]

    result_boats = [{
        **b,
        "win_prob": round(probs[i],4),
        "tansho_odds": float(tansho.get(b["boat"],0) or tansho.get(str(b["boat"]),0)),
    } for i,b in enumerate(boats)]
    result_boats.sort(key=lambda x:-x["win_prob"])

    return {
        "venue":      venue_name,
        "jcd":        jcd,
        "race_no":    rno,
        "date":       hd,
        "boats":      result_boats,
        "top3":       top3_boats,
        "bets":       bets[:8],
        "has_odds":   has_odds,
        "has_before": bool(before and any(v and v.get("exh_time") for v in before.values())),
        "verdict":    "go" if (bets and bets[0]["ev"]>=MIN_EV) else "stop",
        "plan":       user.get("plan","free"),
    }

# ══════════════════════════════════════════════════
# 自動スケジューラー（Cron代替）
# ══════════════════════════════════════════════════

from apscheduler.schedulers.background import BackgroundScheduler
from kyotei_daily_collector import (
    collect_racelist, collect_odds, collect_before, collect_result, to_hd
)

scheduler = BackgroundScheduler(timezone="Asia/Tokyo")

def job_racelist():
    """前夜22時: 翌日の出走表を取得"""
    log.info("[Cron] 出走表取得開始")
    collect_racelist(to_hd("tomorrow"))

def job_odds():
    """9〜21時の毎時0分: オッズ更新"""
    log.info("[Cron] オッズ更新")
    collect_odds(to_hd("today"))

def job_before():
    """9〜21時の毎時15分: 直前情報"""
    log.info("[Cron] 直前情報取得")
    collect_before(to_hd("today"))

def job_result():
    """深夜0時30分: 当日結果収集"""
    log.info("[Cron] 結果収集")
    collect_result(to_hd("yesterday"))

# Cronスケジュール登録
scheduler.add_job(job_racelist, "cron", hour=22, minute=0)
scheduler.add_job(job_odds,     "cron", hour="9-21", minute=0)
scheduler.add_job(job_before,   "cron", hour="9-21", minute=15)
scheduler.add_job(job_result,   "cron", hour=0,  minute=30)

@app.on_event("startup")
def startup():
    scheduler.start()
    log.info("スケジューラー起動完了")

@app.on_event("shutdown")
def shutdown():
    scheduler.shutdown()

# ══════════════════════════════════════════════════
# フロントエンド配信
# ══════════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
def index():
    p = Path("index.html")
    if p.exists():
        return HTMLResponse(p.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>BOAT BRAIN</h1><p>index.html not found</p>")

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now().isoformat(),
            "model": MODEL_PATH.exists()}

# ── 起動 ─────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
