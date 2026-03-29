import streamlit as st
import requests
import json
import hashlib
import pandas as pd
from datetime import datetime, date

st.set_page_config(
    page_title="The Caller · AI Recruitment",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════
#  GLOBAL STYLES  — light, clean, professional
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stAppViewBlockContainer"],
.main, .block-container {
    background: #f1f5f9 !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
    color: #0f172a !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="collapsedControl"] { display: none !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] * { color: #0f172a !important; }
[data-testid="stSidebar"] .stButton > button {
    background: #2563eb !important;
    color: #fff !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea textarea,
.stNumberInput input {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 12px !important;
    transition: border-color .15s, box-shadow .15s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,.1) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea textarea::placeholder { color: #94a3b8 !important; }

/* Labels */
.stTextInput label, .stTextArea label,
.stSelectbox label, .stNumberInput label,
.stDateInput label, .stMultiSelect label {
    color: #475569 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    margin-bottom: 4px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    transition: background .15s, box-shadow .15s !important;
    cursor: pointer !important;
    width: 100%;
}
.stButton > button:hover {
    background: #1d4ed8 !important;
    box-shadow: 0 4px 12px rgba(37,99,235,.25) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #64748b !important;
    padding: 10px 18px !important;
    border-radius: 0 !important;
    border: none !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #2563eb !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #2563eb !important;
    background: transparent !important;
}
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #e2e8f0 !important;
    gap: 0 !important;
    padding: 0 !important;
}
[data-testid="stTabsContent"] { padding-top: 20px !important; }

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
    font-size: 14px !important;
}
[data-baseweb="menu"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,.08) !important;
}
[data-baseweb="option"] { color: #0f172a !important; font-size: 14px !important; }
[data-baseweb="option"]:hover { background: #f1f5f9 !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}
details summary {
    color: #0f172a !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* ── Date input ── */
.stDateInput input {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
    font-size: 14px !important;
}

/* ── Checkbox ── */
.stCheckbox label p { color: #475569 !important; font-size: 14px !important; }

/* ── Alerts ── */
[data-testid="stAlert"] { border-radius: 8px !important; font-size: 14px !important; }

/* ── Form ── */
[data-testid="stForm"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* ── Multiselect ── */
[data-baseweb="tag"] {
    background: #dbeafe !important;
    color: #1e40af !important;
    border-radius: 4px !important;
}

/* ── Divider ── */
hr { border-color: #e2e8f0 !important; margin: 16px 0 !important; }

/* Spinner */
.stSpinner > div { border-top-color: #2563eb !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════
for k, v in {
    "page": "landing", "user": None, "candidates": None,
    "selected_id": None, "active_calls": {}, "show_add": False,
    "sb_url": "", "sb_key": "", "bland_key": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════
#  UTILITIES
# ═══════════════════════════════════════════════════════════════
def get_sb():
    try:
        from supabase import create_client
        url = st.session_state.sb_url or st.secrets.get("SUPABASE_URL", "")
        key = st.session_state.sb_key or st.secrets.get("SUPABASE_KEY", "")
        if url and key:
            return create_client(url, key)
    except Exception:
        pass
    return None

def hp(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

STATUS_LIST = ["New", "Called", "Follow-Up", "Closed", "Placed"]

# Light-theme status badge colors
STATUS_CFG = {
    "New":       ("#dbeafe", "#1e40af", "#bfdbfe"),
    "Called":    ("#dcfce7", "#15803d", "#bbf7d0"),
    "Follow-Up": ("#fef9c3", "#854d0e", "#fef08a"),
    "Closed":    ("#fee2e2", "#b91c1c", "#fecaca"),
    "Placed":    ("#d1fae5", "#065f46", "#a7f3d0"),
}

def badge(status):
    bg, txt, bdr = STATUS_CFG.get(status, ("#f1f5f9", "#475569", "#e2e8f0"))
    return f'<span style="display:inline-block;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;letter-spacing:.2px;background:{bg};color:{txt};border:1px solid {bdr}">{status}</span>'

def sc_color(s):
    if s is None: return "#94a3b8"
    if s >= 75:   return "#16a34a"
    if s >= 50:   return "#d97706"
    return "#dc2626"

def sc_bg(s):
    if s is None: return "#f1f5f9"
    if s >= 75:   return "#dcfce7"
    if s >= 50:   return "#fef9c3"
    return "#fee2e2"

DEMO_CANDIDATES = [
    {"id":1,"user_id":1,"name":"Aditya Sharma","phone":"+91-98765-43210","email":"aditya@email.com","role":"Senior Backend Engineer","experience":6,"skills":"Python, Django, AWS, PostgreSQL","status":"New","ai_score":None,"transcript":None,"followup_date":None,"notes":"","bland_call_id":None},
    {"id":2,"user_id":1,"name":"Priya Menon","phone":"+91-87654-32109","email":"priya@email.com","role":"Product Manager","experience":5,"skills":"Roadmapping, Agile, Data Analysis","status":"Called","ai_score":82,"transcript":"Agent: Hi Priya, I'm Alex from TalentBridge. Good time to talk?\nPriya: Yes, go ahead.\nAgent: We have a Senior PM role at a SaaS company. Walk me through a product you've shipped?\nPriya: I led a 0-to-1 analytics dashboard — 10k DAUs in 3 months.\nAgent: CTC expectations?\nPriya: Currently 24 LPA, expecting 32–35.\nAgent: Notice period?\nPriya: 45 days, negotiable.\nAgent: Perfect. I'll share the JD and schedule next steps.","followup_date":"2025-04-05","notes":"Strong candidate. Interested, CTC aligned."},
    {"id":3,"user_id":1,"name":"Rajan Verma","phone":"+91-76543-21098","email":"rajan@email.com","role":"DevOps Engineer","experience":4,"skills":"Kubernetes, Terraform, CI/CD, AWS","status":"Follow-Up","ai_score":67,"transcript":"Agent: Hi Rajan, calling about a DevOps role at a fintech startup.\nRajan: Bit busy right now.\nAgent: Remote role, 25-30 LPA, strong K8s match.\nRajan: Email me details first?\nAgent: Absolutely. Tuesday to reconnect?\nRajan: Tuesday works.","followup_date":"2025-04-08","notes":"Sent JD. Call back Tuesday."},
    {"id":4,"user_id":1,"name":"Sneha Kulkarni","phone":"+91-65432-10987","email":"sneha@email.com","role":"Data Scientist","experience":3,"skills":"Python, ML, SQL, Tableau, TensorFlow","status":"Placed","ai_score":91,"transcript":"Strong call. Very enthusiastic. Offer negotiated and accepted.","followup_date":None,"notes":"Joining April 15."},
    {"id":5,"user_id":1,"name":"Karan Patel","phone":"+91-54321-09876","email":"karan@email.com","role":"Frontend Engineer","experience":2,"skills":"React, TypeScript, Tailwind CSS","status":"Closed","ai_score":41,"transcript":"Not interested in switching at this time.","followup_date":None,"notes":"Revisit in 6 months."},
]

def load_candidates(sb, user_id=None):
    if sb:
        try:
            q = sb.table("candidates").select("*").order("created_at", desc=True)
            if user_id:
                q = q.eq("user_id", user_id)
            return q.execute().data or []
        except Exception as e:
            st.toast(f"DB error: {e}", icon="⚠️")
    return DEMO_CANDIDATES

def save_candidate(sb, c):
    if sb:
        try:
            sb.table("candidates").upsert(c).execute()
        except Exception as e:
            st.error(f"Save error: {e}")

def login_user(sb, email, pw):
    if email == "admin@thecaller.ai" and pw == "admin123":
        return {"id": 0, "name": "Admin", "email": email, "role": "admin"}, None
    if not sb:
        return None, "No database connected. Use admin@thecaller.ai / admin123 for demo."
    try:
        r = sb.table("users").select("*").eq("email", email).eq("password_hash", hp(pw)).execute()
        if r.data:
            return r.data[0], None
        return None, "Invalid email or password."
    except Exception as e:
        return None, str(e)

def signup_user(sb, name, email, pw):
    if not sb:
        return None, "No database connected."
    try:
        ex = sb.table("users").select("id").eq("email", email).execute()
        if ex.data:
            return None, "Email already registered."
        r = sb.table("users").insert({
            "name": name, "email": email,
            "password_hash": hp(pw), "role": "user"
        }).execute()
        return r.data[0] if r.data else None, None
    except Exception as e:
        return None, str(e)

def call_bland(api_key, candidate, jd, custom=""):
    task = f"""You are Alex, a professional recruitment consultant at TalentBridge.
You are calling {candidate['name']} about a {candidate['role']} position.
JD: {jd}
Goals: 1) Warm intro 2) Pitch role 3) Ask current/expected CTC 4) Notice period 5) Gauge interest 6) Handle objections 7) Agree next steps.
Candidate: {candidate.get('experience','?')}y exp, Skills: {candidate.get('skills','')}
{('Context: ' + custom) if custom else ''}
Be warm, professional, consultative."""
    try:
        r = requests.post("https://api.bland.ai/v1/calls",
            json={"phone_number": candidate["phone"], "task": task, "voice": "june",
                  "reduce_latency": True, "record": True, "max_duration": 10,
                  "wait_for_greeting": True, "language": "en"},
            headers={"authorization": api_key, "Content-Type": "application/json"}, timeout=15)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def fetch_call(api_key, call_id):
    try:
        r = requests.get(f"https://api.bland.ai/v1/calls/{call_id}",
                         headers={"authorization": api_key}, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def score_ai(candidate, jd, transcript):
    try:
        r = requests.post("https://api.anthropic.com/v1/messages",
            json={"model": "claude-sonnet-4-20250514", "max_tokens": 1000,
                  "messages": [{"role": "user", "content":
                    f"Evaluate candidate vs JD.\nJD: {jd}\nCandidate: {candidate['name']}, {candidate.get('experience','?')}y, Skills: {candidate.get('skills','')}\nTranscript:\n{transcript}\nReturn ONLY JSON (no markdown):\n{{\"score\":<0-100>,\"summary\":\"<2-3 sentences>\",\"strengths\":[],\"concerns\":[],\"recommendation\":\"Proceed|Follow-Up|Reject\",\"suggested_ctc\":\"<range>\",\"next_step\":\"<action>\"}}"}]},
            headers={"Content-Type": "application/json"}, timeout=30)
        txt = r.json()["content"][0]["text"].strip().strip("```json").strip("```").strip()
        return json.loads(txt)
    except Exception as e:
        return {"score": 0, "summary": str(e), "strengths": [], "concerns": [],
                "recommendation": "Follow-Up", "suggested_ctc": "N/A", "next_step": "Manual review"}

# ═══════════════════════════════════════════════════════════════
#  SHARED COMPONENTS
# ═══════════════════════════════════════════════════════════════
def nav_bar(active="app"):
    user = st.session_state.user
    if not user: return
    is_admin = user.get("role") == "admin"

    st.markdown("""
    <div style="background:#ffffff;border-bottom:1px solid #e2e8f0;padding:0 8px;margin-bottom:0;
                position:sticky;top:0;z-index:999">
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 5, 3])
    with c1:
        st.markdown('<div style="display:flex;align-items:center;gap:8px;padding:10px 0"><div style="width:32px;height:32px;background:#2563eb;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px">📞</div><span style="font-weight:700;font-size:16px;color:#0f172a;letter-spacing:-.3px">The Caller</span></div>', unsafe_allow_html=True)
    with c2:
        n1, n2, n3 = st.columns([1, 1, 4])
        with n1:
            if st.button("Pipeline", key="nav_pipeline"):
                st.session_state.page = "app"; st.rerun()
        with n2:
            if is_admin and st.button("Admin", key="nav_admin"):
                st.session_state.page = "admin"; st.rerun()
    with c3:
        nc1, nc2 = st.columns([3, 1])
        with nc1:
            role_badge = '<span style="background:#dbeafe;color:#1e40af;border-radius:4px;padding:2px 7px;font-size:11px;font-weight:600;margin-left:6px">Admin</span>' if is_admin else ""
            st.markdown(f'<div style="text-align:right;padding:10px 0;font-size:13px;color:#64748b;font-weight:500">{user.get("name","")}{role_badge}</div>', unsafe_allow_html=True)
        with nc2:
            if st.button("Sign out", key="nav_out"):
                for k in ["user","candidates","selected_id","show_add"]:
                    st.session_state[k] = None if k != "show_add" else False
                st.session_state.active_calls = {}
                st.session_state.page = "landing"
                st.rerun()

    st.markdown('<div style="border-bottom:1px solid #e2e8f0;margin-bottom:24px"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  PAGE: LANDING
# ═══════════════════════════════════════════════════════════════
def page_landing():
    st.markdown("""
    <style>
    .land { max-width:880px; margin:0 auto; padding:64px 24px 60px; }

    /* Nav bar at top */
    .top-nav {
      display:flex; justify-content:space-between; align-items:center;
      margin-bottom:80px;
    }
    .logo { display:flex;align-items:center;gap:10px; }
    .logo-box { width:36px;height:36px;background:#2563eb;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:18px; }
    .logo-name { font-weight:700;font-size:17px;color:#0f172a; }

    /* Hero */
    .eyebrow { display:inline-flex;align-items:center;gap:6px;background:#dbeafe;border:1px solid #bfdbfe;border-radius:20px;padding:4px 12px;font-size:12px;font-weight:600;color:#1e40af;letter-spacing:.3px;margin-bottom:20px; }
    .hero-h { font-size:clamp(32px,5vw,52px);font-weight:800;line-height:1.12;color:#0f172a;letter-spacing:-1px;margin-bottom:16px; }
    .hero-h em { font-style:normal;color:#2563eb; }
    .hero-sub { font-size:16px;color:#64748b;line-height:1.65;max-width:520px;margin-bottom:32px; }

    /* Pipeline badge */
    .pipe { display:flex;align-items:center;background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:6px;width:fit-content;margin-bottom:56px; }
    .pipe-s { padding:9px 20px;border-radius:8px;font-size:13px;font-weight:600;color:#94a3b8; }
    .pipe-s.on { background:#2563eb;color:#fff; }
    .pipe-a { padding:0 6px;color:#cbd5e1;font-size:14px; }

    /* Features */
    .feat-grid { display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-bottom:56px; }
    .feat { background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:22px;transition:border-color .2s,box-shadow .2s; }
    .feat:hover { border-color:#bfdbfe;box-shadow:0 4px 16px rgba(37,99,235,.08); }
    .feat-ico { width:40px;height:40px;background:#eff6ff;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:12px; }
    .feat-t { font-size:14px;font-weight:700;color:#0f172a;margin-bottom:5px; }
    .feat-d { font-size:13px;color:#64748b;line-height:1.55; }

    /* Stats */
    .stats { display:flex;gap:0;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;margin-bottom:48px;background:#ffffff; }
    .stat { flex:1;text-align:center;padding:24px 16px;border-right:1px solid #e2e8f0; }
    .stat:last-child { border-right:none; }
    .stat-n { font-size:32px;font-weight:800;color:#2563eb; }
    .stat-l { font-size:12px;color:#94a3b8;margin-top:3px;font-weight:500; }

    /* Footer */
    .foot { text-align:center;font-size:12px;color:#94a3b8;border-top:1px solid #e2e8f0;padding-top:24px; }
    </style>

    <div class="land">
      <div class="top-nav">
        <div class="logo">
          <div class="logo-box">📞</div>
          <span class="logo-name">The Caller</span>
        </div>
      </div>

      <div class="eyebrow">🤖 AI Recruitment Agent</div>
      <h1 class="hero-h">Your recruiter,<br><em>fully automated.</em></h1>
      <p class="hero-sub">The Caller is an AI calling agent that connects with candidates, evaluates fit against your JD, negotiates offers, and keeps your pipeline moving — completely hands-free.</p>

      <div class="pipe">
        <div class="pipe-s">🔍 Sourcer</div>
        <div class="pipe-a">→</div>
        <div class="pipe-s on">📞 The Caller</div>
        <div class="pipe-a">→</div>
        <div class="pipe-s">✅ Validator</div>
      </div>

      <div class="feat-grid">
        <div class="feat"><div class="feat-ico">📞</div><div class="feat-t">AI Phone Calls</div><div class="feat-d">Calls candidates via Bland.ai with a natural, human-like voice and a structured conversation flow.</div></div>
        <div class="feat"><div class="feat-ico">🧠</div><div class="feat-t">Smart Scoring</div><div class="feat-d">Claude AI scores each candidate against your JD with detailed strengths, concerns and CTC insight.</div></div>
        <div class="feat"><div class="feat-ico">💬</div><div class="feat-t">Negotiate & Close</div><div class="feat-d">Handles CTC negotiation, notice periods and objections professionally on your behalf.</div></div>
        <div class="feat"><div class="feat-ico">🔔</div><div class="feat-t">Follow-Up Tracking</div><div class="feat-d">Schedules follow-ups and keeps your pipeline moving without any manual effort.</div></div>
        <div class="feat"><div class="feat-ico">🗄️</div><div class="feat-t">Supabase Sync</div><div class="feat-d">Shares data seamlessly across your Sourcer and Validator apps through one database.</div></div>
        <div class="feat"><div class="feat-ico">📊</div><div class="feat-t">Admin Analytics</div><div class="feat-d">Full dashboard with placement rates, AI scores, pipeline status and team performance.</div></div>
      </div>

      <div class="stats">
        <div class="stat"><div class="stat-n">10×</div><div class="stat-l">Faster outreach</div></div>
        <div class="stat"><div class="stat-n">3</div><div class="stat-l">Apps, one pipeline</div></div>
        <div class="stat"><div class="stat-n">0</div><div class="stat-l">Manual calls needed</div></div>
        <div class="stat"><div class="stat-n">100%</div><div class="stat-l">Free to deploy</div></div>
      </div>

      <div class="foot">Built on Streamlit · Bland.ai · Claude AI · Supabase</div>
    </div>
    """, unsafe_allow_html=True)

    # CTA buttons
    _, bc1, bc2, _ = st.columns([2, 2, 2, 4])
    with bc1:
        if st.button("Get Started →", key="land_cta"):
            st.session_state.page = "signup"; st.rerun()
    with bc2:
        if st.button("Sign In", key="land_login"):
            st.session_state.page = "login"; st.rerun()

# ═══════════════════════════════════════════════════════════════
#  PAGE: LOGIN
# ═══════════════════════════════════════════════════════════════
def page_login():
    sb = get_sb()

    st.markdown("""
    <style>
    .auth-page { min-height:100vh; display:flex; align-items:flex-start; justify-content:center; padding:48px 16px; }
    .auth-wrap { width:100%; max-width:400px; }
    .auth-logo { text-align:center; margin-bottom:32px; }
    .auth-logo-box { width:52px;height:52px;background:#2563eb;border-radius:14px;display:inline-flex;align-items:center;justify-content:center;font-size:24px;margin-bottom:10px; }
    .auth-logo-name { font-size:20px;font-weight:700;color:#0f172a; }
    .auth-logo-sub { font-size:13px;color:#94a3b8;margin-top:2px; }
    .auth-card { background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;padding:32px;box-shadow:0 1px 3px rgba(0,0,0,.06); }
    .auth-card-title { font-size:20px;font-weight:700;color:#0f172a;margin-bottom:4px; }
    .auth-card-sub { font-size:13px;color:#94a3b8;margin-bottom:24px; }
    .demo-hint { background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:10px 14px;font-size:12px;color:#1e40af;font-family:monospace;margin-bottom:20px;line-height:1.7; }
    .auth-footer { text-align:center;margin-top:18px;font-size:13px;color:#94a3b8; }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="auth-logo">
          <div class="auth-logo-box">📞</div>
          <div class="auth-logo-name">The Caller</div>
          <div class="auth-logo-sub">AI Recruitment Agent</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("← Home", key="login_back"):
            st.session_state.page = "landing"; st.rerun()

        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<div class="auth-card-title">Welcome back</div><div class="auth-card-sub">Sign in to your account</div>', unsafe_allow_html=True)

        if not sb:
            st.markdown("""
            <div class="demo-hint">
              <strong>Demo credentials</strong><br>
              admin@thecaller.ai<br>
              admin123
            </div>
            """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="you@example.com")
            pw    = st.text_input("Password", type="password", placeholder="Your password")
            sub   = st.form_submit_button("Sign In →", use_container_width=True)
            if sub:
                if not email or not pw:
                    st.error("Please enter both email and password.")
                else:
                    with st.spinner("Signing in..."):
                        user, err = login_user(sb, email, pw)
                    if user:
                        st.session_state.user = user
                        st.session_state.candidates = None
                        st.session_state.page = "admin" if user.get("role") == "admin" else "app"
                        st.rerun()
                    else:
                        st.error(err)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-footer">Don\'t have an account?</div>', unsafe_allow_html=True)
        if st.button("Create Account", key="to_signup", use_container_width=True):
            st.session_state.page = "signup"; st.rerun()

# ═══════════════════════════════════════════════════════════════
#  PAGE: SIGNUP
# ═══════════════════════════════════════════════════════════════
def page_signup():
    sb = get_sb()

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style="text-align:center;margin-bottom:32px">
          <div style="width:52px;height:52px;background:#2563eb;border-radius:14px;display:inline-flex;align-items:center;justify-content:center;font-size:24px;margin-bottom:10px">📞</div>
          <div style="font-size:20px;font-weight:700;color:#0f172a">The Caller</div>
          <div style="font-size:13px;color:#94a3b8;margin-top:2px">AI Recruitment Agent</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("← Home", key="signup_back"):
            st.session_state.page = "landing"; st.rerun()

        if not sb:
            st.warning("No database connected. Connect Supabase to enable registration.")
            st.info("For demo access, use Sign In with admin@thecaller.ai / admin123")
            if st.button("Go to Sign In", key="to_login_ns"):
                st.session_state.page = "login"; st.rerun()
            return

        st.markdown('<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;padding:32px;box-shadow:0 1px 3px rgba(0,0,0,.06)">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:20px;font-weight:700;color:#0f172a;margin-bottom:4px">Create account</div><div style="font-size:13px;color:#94a3b8;margin-bottom:24px">Start automating your recruitment</div>', unsafe_allow_html=True)

        with st.form("signup_form"):
            name    = st.text_input("Full Name", placeholder="Your name")
            email   = st.text_input("Email", placeholder="you@example.com")
            pw      = st.text_input("Password", type="password", placeholder="Min. 8 characters")
            confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
            agree   = st.checkbox("I agree to the terms of service")
            sub     = st.form_submit_button("Create Account →", use_container_width=True)
            if sub:
                if not all([name, email, pw, confirm]):
                    st.error("Please fill in all fields.")
                elif pw != confirm:
                    st.error("Passwords do not match.")
                elif len(pw) < 8:
                    st.error("Password must be at least 8 characters.")
                elif not agree:
                    st.error("Please accept the terms of service.")
                else:
                    with st.spinner("Creating your account..."):
                        user, err = signup_user(sb, name, email, pw)
                    if user:
                        st.session_state.user = user
                        st.session_state.page = "app"
                        st.rerun()
                    else:
                        st.error(err)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;margin-top:18px;font-size:13px;color:#94a3b8">Already have an account?</div>', unsafe_allow_html=True)
        if st.button("Sign In", key="to_login2", use_container_width=True):
            st.session_state.page = "login"; st.rerun()

# ═══════════════════════════════════════════════════════════════
#  PAGE: MAIN APP
# ═══════════════════════════════════════════════════════════════
def page_app():
    if not st.session_state.user:
        st.session_state.page = "login"; st.rerun()

    user = st.session_state.user
    sb   = get_sb()

    if st.session_state.candidates is None:
        uid = None if user.get("role") == "admin" else user.get("id")
        st.session_state.candidates = load_candidates(sb, uid)

    candidates = st.session_state.candidates

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        with st.expander("🗄️ Supabase"):
            u = st.text_input("URL", value=st.session_state.sb_url, placeholder="https://xxx.supabase.co", key="sb_u")
            k = st.text_input("Key", value=st.session_state.sb_key, type="password", key="sb_k")
            if st.button("Connect", key="sb_conn"):
                st.session_state.sb_url = u; st.session_state.sb_key = k
                st.session_state.candidates = None; st.rerun()
        with st.expander("📞 Bland.ai"):
            bk = st.text_input("API Key", value=st.session_state.bland_key, type="password", key="bk_inp")
            if st.button("Save Key", key="bk_save"):
                st.session_state.bland_key = bk; st.success("Saved!")
        st.markdown("---")
        st.markdown("### 🔍 Filter")
        sf = st.multiselect("Status", STATUS_LIST, default=["New","Called","Follow-Up"], key="sf")
        sq = st.text_input("Search", placeholder="Name, role, skills…", key="sq")
        if st.button("🔄 Refresh", use_container_width=True, key="refresh"):
            st.session_state.candidates = None; st.rerun()

    nav_bar("app")

    # Filter candidates
    filtered = [
        c for c in candidates
        if (not sf or c["status"] in sf)
        and (not sq or any(sq.lower() in str(c.get(f,"")).lower() for f in ["name","role","skills","email"]))
    ]

    # KPI row
    total  = len(candidates)
    new_c  = sum(1 for c in candidates if c["status"] == "New")
    active = sum(1 for c in candidates if c["status"] in ["Called","Follow-Up"])
    placed = sum(1 for c in candidates if c["status"] == "Placed")
    scores = [c["ai_score"] for c in candidates if c.get("ai_score")]
    avg_sc = int(sum(scores)/len(scores)) if scores else None
    today  = str(date.today())
    ov     = sum(1 for c in candidates if c.get("followup_date") and c["followup_date"] < today)

    kpi_html = f"""
    <style>
    .kpi-row {{ display:flex;gap:10px;margin-bottom:24px;flex-wrap:wrap; }}
    .kpi {{ flex:1;min-width:100px;background:#ffffff;border:1px solid #e2e8f0;
             border-radius:10px;padding:14px 16px;box-shadow:0 1px 2px rgba(0,0,0,.04); }}
    .kpi-v {{ font-size:24px;font-weight:800;color:#0f172a;line-height:1; }}
    .kpi-l {{ font-size:11px;color:#94a3b8;margin-top:4px;text-transform:uppercase;
               letter-spacing:.6px;font-weight:500; }}
    </style>
    <div class="kpi-row">
      <div class="kpi"><div class="kpi-v">{total}</div><div class="kpi-l">Pipeline</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#2563eb">{new_c}</div><div class="kpi-l">Pending</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#d97706">{active}</div><div class="kpi-l">In Progress</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#16a34a">{placed}</div><div class="kpi-l">Placed</div></div>
      <div class="kpi"><div class="kpi-v" style="color:{sc_color(avg_sc)}">{avg_sc if avg_sc else '—'}</div><div class="kpi-l">Avg Score</div></div>
      <div class="kpi"><div class="kpi-v" style="color:{'#dc2626' if ov else '#16a34a'}">{ov}</div><div class="kpi-l">Overdue</div></div>
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)

    left, right = st.columns([5, 7], gap="large")

    # ── LEFT: candidate list ──────────────────────────────────
    with left:
        h1, h2 = st.columns([4, 1])
        with h1:
            st.markdown(f'<div style="font-size:15px;font-weight:700;color:#0f172a;margin-bottom:10px">Candidates <span style="color:#94a3b8;font-weight:400;font-size:13px">({len(filtered)})</span></div>', unsafe_allow_html=True)
        with h2:
            if st.button("+ Add", key="add_tog"):
                st.session_state.show_add = not st.session_state.show_add

        if st.session_state.show_add:
            st.markdown('<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:20px;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,.06)">', unsafe_allow_html=True)
            with st.form("add_form"):
                st.markdown('<div style="font-weight:600;font-size:14px;color:#0f172a;margin-bottom:12px">Add Candidate</div>', unsafe_allow_html=True)
                a1, a2 = st.columns(2)
                with a1:
                    n  = st.text_input("Name *", key="add_n")
                    ph = st.text_input("Phone *", placeholder="+91-XXXXX-XXXXX", key="add_ph")
                    ro = st.text_input("Role *", key="add_ro")
                with a2:
                    em = st.text_input("Email", key="add_em")
                    ex = st.number_input("Experience (yrs)", 0, 40, 2, key="add_ex")
                    sk = st.text_input("Skills", key="add_sk")
                if st.form_submit_button("Add to Pipeline", use_container_width=True):
                    if n and ph and ro:
                        nid = max([c["id"] for c in candidates], default=0) + 1
                        obj = {"id": nid, "user_id": user.get("id",1),
                               "name":n,"phone":ph,"email":em,"role":ro,
                               "experience":ex,"skills":sk,"status":"New",
                               "ai_score":None,"transcript":None,
                               "followup_date":None,"notes":"","bland_call_id":None}
                        st.session_state.candidates.append(obj)
                        save_candidate(sb, obj)
                        st.session_state.show_add = False; st.rerun()
                    else:
                        st.error("Name, phone and role are required.")
            st.markdown('</div>', unsafe_allow_html=True)

        if not filtered:
            st.markdown('<div style="text-align:center;padding:40px;color:#94a3b8;background:#ffffff;border:1px solid #e2e8f0;border-radius:12px"><div style="font-size:28px;margin-bottom:10px">🔍</div><div style="font-weight:600;color:#64748b">No candidates</div><div style="font-size:13px;margin-top:4px">Adjust filters or add a candidate</div></div>', unsafe_allow_html=True)

        for c in filtered:
            is_sel  = st.session_state.selected_id == c["id"]
            is_live = c["id"] in st.session_state.active_calls
            sc      = c.get("ai_score")
            sc_html = f'<div style="background:{sc_bg(sc)};color:{sc_color(sc)};border-radius:8px;padding:4px 10px;font-size:13px;font-weight:700;text-align:center">{sc}</div>' if sc else ""
            live_dot = '<span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#dc2626;margin-left:6px;vertical-align:middle"></span>' if is_live else ""
            bdr = "2px solid #2563eb" if is_sel else "1px solid #e2e8f0"
            shadow = "box-shadow:0 0 0 3px rgba(37,99,235,.1);" if is_sel else "box-shadow:0 1px 2px rgba(0,0,0,.04);"

            st.markdown(f"""
            <div style="background:#ffffff;border:{bdr};border-radius:10px;padding:12px 14px;
                        margin-bottom:6px;{shadow}transition:all .15s">
              <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div style="flex:1;min-width:0">
                  <div style="font-size:14px;font-weight:600;color:#0f172a">{c['name']}{live_dot}</div>
                  <div style="font-size:12px;color:#94a3b8;margin-top:2px">{c['role']} · {c.get('experience','?')}y exp</div>
                  <div style="margin-top:8px">{badge(c['status'])}</div>
                </div>
                <div style="flex-shrink:0;margin-left:12px">{sc_html}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open →", key=f"sel_{c['id']}", use_container_width=True):
                st.session_state.selected_id = c["id"]; st.rerun()

    # ── RIGHT: detail panel ───────────────────────────────────
    with right:
        sel_id = st.session_state.selected_id
        sel    = next((c for c in candidates if c["id"] == sel_id), None)

        if not sel:
            st.markdown("""
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                        height:380px;background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;
                        text-align:center;box-shadow:0 1px 2px rgba(0,0,0,.04)">
              <div style="font-size:40px;margin-bottom:12px">📋</div>
              <div style="font-size:15px;font-weight:700;color:#0f172a">No candidate selected</div>
              <div style="font-size:13px;margin-top:4px;color:#94a3b8">Click a candidate on the left to view details</div>
            </div>
            """, unsafe_allow_html=True)
            return

        sc = sel.get("ai_score")
        sc_block = f'<div style="background:{sc_bg(sc)};border:1.5px solid {sc_color(sc)}33;border-radius:12px;padding:12px 16px;text-align:center;flex-shrink:0"><div style="font-size:24px;font-weight:800;color:{sc_color(sc)}">{sc}</div><div style="font-size:10px;color:#94a3b8;margin-top:2px;font-weight:600;text-transform:uppercase;letter-spacing:.5px">AI Score</div></div>' if sc else ""

        st.markdown(f"""
        <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;
                    padding:18px 22px;margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,.06)">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px">
            <div style="flex:1">
              <div style="font-size:19px;font-weight:700;color:#0f172a">{sel['name']}</div>
              <div style="font-size:13px;color:#94a3b8;margin-top:3px">{sel['role']} · {sel.get('experience','?')} yrs experience</div>
              <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap;align-items:center">
                {badge(sel['status'])}
                <span style="font-size:12px;color:#94a3b8">{sel.get('phone','')}</span>
                <span style="font-size:12px;color:#94a3b8">{sel.get('email','')}</span>
              </div>
            </div>
            {sc_block}
          </div>
        </div>
        """, unsafe_allow_html=True)

        t1, t2, t3, t4 = st.tabs(["Profile", "📞 Call", "🧠 Evaluation", "🔔 Follow-Ups"])

        # Profile tab
        with t1:
            st.markdown(f'<div style="font-size:12px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px">Skills</div><div style="font-size:13px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px 12px;margin-bottom:16px;color:#0f172a;font-family:monospace">{sel.get("skills","—")}</div>', unsafe_allow_html=True)
            new_notes  = st.text_area("Notes & Activity", value=sel.get("notes","") or "", height=110, key="notes_ta")
            sa, sb_col = st.columns(2)
            with sa:
                new_status = st.selectbox("Update Status", STATUS_LIST, index=STATUS_LIST.index(sel.get("status","New")), key="status_sel")
            with sb_col:
                st.markdown('<div style="height:26px"></div>', unsafe_allow_html=True)
                if st.button("💾 Save Changes", use_container_width=True, key="save_profile"):
                    for i, c in enumerate(st.session_state.candidates):
                        if c["id"] == sel["id"]:
                            st.session_state.candidates[i]["notes"]  = new_notes
                            st.session_state.candidates[i]["status"] = new_status
                            save_candidate(sb, st.session_state.candidates[i])
                    st.success("Saved!"); st.rerun()

        # Call tab
        with t2:
            jd = st.text_area("Job Description *",
                placeholder="Paste the full JD or a summary. The AI agent uses this to pitch the role and evaluate the candidate.",
                height=100, key="jd_call")
            ci = st.text_area("Agent Instructions (optional)",
                placeholder="e.g. Be warm. Mention remote culture. Budget is 28–35 LPA. Emphasise growth opportunities.",
                height=65, key="ci_call")
            bk = st.session_state.bland_key
            ca, cb = st.columns(2)
            with ca:
                if not bk:
                    st.info("💡 Add your Bland.ai API key in the sidebar Settings to enable calls.")
                elif st.button("📞 Start AI Call", use_container_width=True, key="start_call"):
                    if not jd.strip():
                        st.error("Please paste the Job Description first.")
                    else:
                        with st.spinner(f"Connecting to {sel['name']}..."):
                            res = call_bland(bk, sel, jd, ci)
                        cid = res.get("call_id") or res.get("id")
                        if cid:
                            st.session_state.active_calls[sel["id"]] = cid
                            for i, c in enumerate(st.session_state.candidates):
                                if c["id"] == sel["id"]:
                                    st.session_state.candidates[i]["status"] = "Called"
                                    st.session_state.candidates[i]["bland_call_id"] = cid
                                    save_candidate(sb, st.session_state.candidates[i])
                            st.success(f"✓ Call started · ID: `{cid}`")
                        else:
                            st.error(f"Call failed: {res.get('error', res)}")
            with cb:
                acid = st.session_state.active_calls.get(sel["id"]) or sel.get("bland_call_id")
                if acid and st.button("🔄 Fetch Transcript", use_container_width=True, key="fetch_tx"):
                    with st.spinner("Fetching transcript..."):
                        data = fetch_call(bk, acid)
                    tx = data.get("transcript","") or "\n".join(
                        [f"{t.get('user','?')}: {t.get('text','')}" for t in data.get("transcripts",[])])
                    if tx:
                        for i, c in enumerate(st.session_state.candidates):
                            if c["id"] == sel["id"]:
                                st.session_state.candidates[i]["transcript"] = tx
                                save_candidate(sb, st.session_state.candidates[i])
                        st.success("Transcript fetched!"); st.rerun()
                    else:
                        st.info(f"Status: {data.get('status','pending')} — try again in a moment.")

            st.markdown('<div style="border-top:1px solid #e2e8f0;margin:16px 0"></div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:12px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">Transcript</div>', unsafe_allow_html=True)
            mtx = st.text_area("", value=sel.get("transcript","") or "", height=170,
                               label_visibility="collapsed", key="mtx",
                               placeholder="Transcript appears here after a call, or paste it manually.")
            if st.button("💾 Save Transcript", use_container_width=True, key="save_tx"):
                for i, c in enumerate(st.session_state.candidates):
                    if c["id"] == sel["id"]:
                        st.session_state.candidates[i]["transcript"] = mtx
                        save_candidate(sb, st.session_state.candidates[i])
                st.success("Transcript saved!")

        # Evaluation tab
        with t3:
            if not sel.get("transcript"):
                st.markdown("""
                <div style="text-align:center;padding:48px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px">
                  <div style="font-size:36px;margin-bottom:12px">📞</div>
                  <div style="font-size:15px;font-weight:700;color:#0f172a">Complete a call first</div>
                  <div style="font-size:13px;margin-top:6px;color:#94a3b8">Save the transcript in the Call tab, then run AI evaluation here.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                jde = st.text_area("Job Description for Scoring",
                    placeholder="Paste the JD to score this candidate against…", height=90, key="jd_eval")
                if st.button("⚡ Run AI Evaluation", use_container_width=True, key="run_eval"):
                    if not jde.strip():
                        st.error("Please paste the JD first.")
                    else:
                        with st.spinner("Claude is evaluating the candidate..."):
                            res = score_ai(sel, jde, sel["transcript"])
                        score = res.get("score", 0)
                        for i, c in enumerate(st.session_state.candidates):
                            if c["id"] == sel["id"]:
                                st.session_state.candidates[i]["ai_score"] = score
                                note = f"\n[AI Eval {datetime.now().strftime('%d %b %H:%M')}] {res.get('summary','')}"
                                st.session_state.candidates[i]["notes"] = (c.get("notes","") or "") + note
                                save_candidate(sb, st.session_state.candidates[i])

                        rec   = res.get("recommendation","—")
                        rc    = {"Proceed":"#16a34a","Follow-Up":"#d97706","Reject":"#dc2626"}.get(rec,"#64748b")
                        rcbg  = {"Proceed":"#dcfce7","Follow-Up":"#fef9c3","Reject":"#fee2e2"}.get(rec,"#f1f5f9")

                        st.markdown(f"""
                        <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:20px;margin:12px 0;box-shadow:0 1px 3px rgba(0,0,0,.06)">
                          <div style="display:flex;gap:16px;align-items:center;margin-bottom:14px">
                            <div style="width:64px;height:64px;border-radius:50%;background:{sc_bg(score)};
                                        border:2px solid {sc_color(score)}66;display:flex;align-items:center;
                                        justify-content:center;font-size:22px;font-weight:800;
                                        color:{sc_color(score)};flex-shrink:0">{score}</div>
                            <div>
                              <div style="font-size:16px;font-weight:700;color:#0f172a">{sel['name']}</div>
                              <div style="margin-top:6px;display:flex;align-items:center;gap:8px;flex-wrap:wrap">
                                <span style="background:{rcbg};color:{rc};border-radius:6px;padding:3px 10px;font-size:12px;font-weight:600">{rec}</span>
                                <span style="font-size:13px;color:#94a3b8">{res.get('suggested_ctc','')}</span>
                              </div>
                            </div>
                          </div>
                          <p style="font-size:13px;color:#64748b;line-height:1.65;margin:0">{res.get('summary','')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        ea, eb = st.columns(2)
                        with ea:
                            st.markdown('<div style="font-size:12px;font-weight:700;color:#16a34a;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px">✓ Strengths</div>', unsafe_allow_html=True)
                            for s in res.get("strengths",[]):
                                st.markdown(f'<div style="font-size:13px;color:#374151;padding:5px 0;border-bottom:1px solid #f1f5f9">· {s}</div>', unsafe_allow_html=True)
                        with eb:
                            st.markdown('<div style="font-size:12px;font-weight:700;color:#dc2626;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px">⚠ Concerns</div>', unsafe_allow_html=True)
                            for s in res.get("concerns",[]):
                                st.markdown(f'<div style="font-size:13px;color:#374151;padding:5px 0;border-bottom:1px solid #f1f5f9">· {s}</div>', unsafe_allow_html=True)

                        if res.get("next_step"):
                            st.markdown(f'<div style="margin-top:12px;background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:10px 14px;font-size:13px;color:#1e40af;font-weight:500">💡 Next step: {res["next_step"]}</div>', unsafe_allow_html=True)
                        st.rerun()

                if sel.get("ai_score"):
                    st.markdown(f'<div style="display:inline-flex;align-items:center;gap:8px;padding:8px 14px;background:{sc_bg(sel["ai_score"])};border-radius:8px;margin-top:8px"><span style="font-size:13px;color:#64748b">Stored score:</span><span style="font-size:20px;font-weight:800;color:{sc_color(sel["ai_score"])}">{sel["ai_score"]}/100</span></div>', unsafe_allow_html=True)

        # Follow-Ups tab
        with t4:
            fa, fb = st.columns(2)
            with fa:
                fud = st.date_input("Schedule Date", value=date.today(), key="fud")
            fun = st.text_area("Reminder Note", height=70, key="fun",
                placeholder="e.g. Send updated offer. Call at 11 AM. Confirm notice period.")
            if st.button("📅 Schedule Follow-Up", use_container_width=True, key="save_fu"):
                for i, c in enumerate(st.session_state.candidates):
                    if c["id"] == sel["id"]:
                        entry = f"\n[Follow-Up: {fud}] {fun}"
                        st.session_state.candidates[i]["followup_date"] = str(fud)
                        st.session_state.candidates[i]["status"]        = "Follow-Up"
                        st.session_state.candidates[i]["notes"]         = (c.get("notes","") or "") + entry
                        save_candidate(sb, st.session_state.candidates[i])
                st.success(f"Follow-up scheduled for {fud}!"); st.rerun()

            st.markdown('<div style="border-top:1px solid #e2e8f0;margin:16px 0"></div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:10px">All Upcoming Follow-Ups</div>', unsafe_allow_html=True)

            fu_list = sorted([(c["name"],c["followup_date"],c["role"],c["id"]) for c in candidates if c.get("followup_date")], key=lambda x: x[1])
            today_s = str(date.today())

            if not fu_list:
                st.markdown('<div style="font-size:13px;color:#94a3b8">None scheduled yet.</div>', unsafe_allow_html=True)
            for nm, fd, rl, cid in fu_list:
                is_ov   = fd < today_s
                is_tod  = fd == today_s
                dc      = "#dc2626" if is_ov else ("#d97706" if is_tod else "#16a34a")
                dcbg    = "#fee2e2" if is_ov else ("#fef9c3" if is_tod else "#dcfce7")
                lbl     = f"Overdue · {fd}" if is_ov else ("Today" if is_tod else fd)
                hl      = "border-left:3px solid #2563eb;" if cid == sel_id else ""
                st.markdown(f'<div style="display:flex;align-items:center;gap:10px;padding:10px 14px;background:#ffffff;border:1px solid #e2e8f0;border-radius:8px;margin-bottom:5px;{hl}box-shadow:0 1px 2px rgba(0,0,0,.04)"><div style="width:8px;height:8px;border-radius:50%;background:{dc};flex-shrink:0"></div><div style="flex:1"><div style="font-size:13px;font-weight:600;color:#0f172a">{nm}</div><div style="font-size:12px;color:#94a3b8">{rl}</div></div><div style="background:{dcbg};color:{dc};border-radius:6px;padding:2px 10px;font-size:12px;font-weight:600">{lbl}</div></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE: ADMIN
# ═══════════════════════════════════════════════════════════════
def page_admin():
    user = st.session_state.get("user")
    if not user: st.session_state.page = "login"; st.rerun()
    if user.get("role") != "admin": st.session_state.page = "app"; st.rerun()

    sb = get_sb()
    nav_bar("admin")

    all_c = load_candidates(sb)
    all_u = []
    if sb:
        try: all_u = sb.table("users").select("id,name,email,role,created_at").execute().data or []
        except: pass
    if not all_u:
        all_u = [
            {"id":0,"name":"Admin (Demo)","email":"admin@thecaller.ai","role":"admin","created_at":"2025-01-01"},
            {"id":1,"name":"Recruiter One","email":"recruiter1@example.com","role":"user","created_at":"2025-01-15"},
        ]

    total_c = len(all_c); total_u = len(all_u)
    placed  = sum(1 for c in all_c if c.get("status")=="Placed")
    called  = sum(1 for c in all_c if c.get("status") in ["Called","Follow-Up","Placed","Closed"])
    scores  = [c["ai_score"] for c in all_c if c.get("ai_score")]
    avg_sc  = int(sum(scores)/len(scores)) if scores else None
    pr      = int((placed/total_c)*100) if total_c else 0
    today   = str(date.today())
    ov      = sum(1 for c in all_c if c.get("followup_date") and c["followup_date"] < today)

    st.markdown(f"""
    <style>
    .adkpi {{ display:flex;gap:10px;margin-bottom:24px;flex-wrap:wrap; }}
    .adk {{ flex:1;min-width:100px;background:#ffffff;border:1px solid #e2e8f0;border-radius:10px;
             padding:14px 16px;box-shadow:0 1px 2px rgba(0,0,0,.04); }}
    .adk-v {{ font-size:24px;font-weight:800;color:#0f172a;line-height:1; }}
    .adk-l {{ font-size:11px;color:#94a3b8;margin-top:4px;text-transform:uppercase;letter-spacing:.6px;font-weight:500; }}
    .admt {{ width:100%;border-collapse:collapse;font-size:13px; }}
    .admt th {{ text-align:left;padding:9px 14px;background:#f8fafc;color:#94a3b8;font-size:11px;text-transform:uppercase;letter-spacing:.6px;font-weight:600;border-bottom:1px solid #e2e8f0; }}
    .admt td {{ padding:10px 14px;border-bottom:1px solid #f1f5f9;vertical-align:middle;color:#374151; }}
    .admt tr:hover td {{ background:#f8fafc; }}
    .admc {{ background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;margin-bottom:18px;box-shadow:0 1px 3px rgba(0,0,0,.04); }}
    .admch {{ padding:12px 18px;border-bottom:1px solid #e2e8f0;font-size:14px;font-weight:700;color:#0f172a; }}
    </style>

    <div style="margin-bottom:20px">
      <div style="font-size:20px;font-weight:700;color:#0f172a">Admin Dashboard</div>
      <div style="font-size:13px;color:#94a3b8;margin-top:3px">Full platform overview · All users · All data</div>
    </div>

    <div class="adkpi">
      <div class="adk"><div class="adk-v">{total_u}</div><div class="adk-l">Users</div></div>
      <div class="adk"><div class="adk-v">{total_c}</div><div class="adk-l">Candidates</div></div>
      <div class="adk"><div class="adk-v" style="color:#16a34a">{placed}</div><div class="adk-l">Placed</div></div>
      <div class="adk"><div class="adk-v" style="color:#2563eb">{called}</div><div class="adk-l">Calls Made</div></div>
      <div class="adk"><div class="adk-v" style="color:{sc_color(avg_sc)}">{avg_sc or '—'}</div><div class="adk-l">Avg Score</div></div>
      <div class="adk"><div class="adk-v" style="color:#16a34a">{pr}%</div><div class="adk-l">Placement Rate</div></div>
      <div class="adk"><div class="adk-v" style="color:{'#dc2626' if ov else '#16a34a'}">{ov}</div><div class="adk-l">Overdue</div></div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["👥 Users", "📋 Candidates", "📊 Analytics", "⚙️ Settings"])

    with tab1:
        rows = ""
        for u in all_u:
            rb = f'<span style="background:{"#dbeafe" if u.get("role")=="admin" else "#f1f5f9"};color:{"#1e40af" if u.get("role")=="admin" else "#64748b"};border-radius:5px;padding:2px 8px;font-size:11px;font-weight:600">{"Admin" if u.get("role")=="admin" else "User"}</span>'
            uc = [c for c in all_c if c.get("user_id")==u["id"]]
            rows += f'<tr><td style="font-weight:600;color:#0f172a">{u.get("name","")}</td><td>{u.get("email","")}</td><td>{rb}</td><td style="text-align:center;font-weight:600">{len(uc)}</td><td style="text-align:center;font-weight:600;color:#16a34a">{sum(1 for c in uc if c.get("status")=="Placed")}</td><td style="color:#94a3b8">{str(u.get("created_at",""))[:10]}</td></tr>'
        st.markdown(f'<div class="admc"><div class="admch">Registered Users ({len(all_u)})</div><table class="admt"><thead><tr><th>Name</th><th>Email</th><th>Role</th><th style="text-align:center">Candidates</th><th style="text-align:center">Placed</th><th>Joined</th></tr></thead><tbody>{rows}</tbody></table></div>', unsafe_allow_html=True)
        st.markdown("**Update User Role**")
        m1, m2, m3 = st.columns([3,2,1])
        with m1: te = st.selectbox("User", [u["email"] for u in all_u], key="role_email")
        with m2: nr = st.selectbox("Role", ["user","admin"], key="role_new")
        with m3:
            st.markdown('<div style="height:26px"></div>', unsafe_allow_html=True)
            if st.button("Update", key="role_upd"):
                if sb:
                    try: sb.table("users").update({"role":nr}).eq("email",te).execute(); st.success("Updated!"); st.rerun()
                    except Exception as e: st.error(str(e))
                else: st.info("Demo mode — connect Supabase to manage users")

    with tab2:
        f1, f2 = st.columns([2,3])
        with f1: fs = st.multiselect("Status", STATUS_LIST, key="adm_sf")
        with f2: fq = st.text_input("Search", key="adm_sq", placeholder="Name, role, email…")
        fc = [c for c in all_c if (not fs or c.get("status") in fs) and (not fq or any(fq.lower() in str(c.get(f,"")).lower() for f in ["name","role","email","skills"]))]
        rows = "".join(f'<tr><td style="font-weight:600;color:#0f172a">{c.get("name","")}</td><td style="color:#64748b">{c.get("role","")}</td><td>{badge(c.get("status","New"))}</td><td style="text-align:center;font-weight:700;color:{sc_color(c.get("ai_score"))}">{c.get("ai_score","") or "—"}</td><td style="color:#94a3b8">{c.get("followup_date","") or "—"}</td></tr>' for c in fc)
        st.markdown(f'<div class="admc"><div class="admch">All Candidates ({len(fc)})</div><table class="admt"><thead><tr><th>Name</th><th>Role</th><th>Status</th><th style="text-align:center">Score</th><th>Follow-Up</th></tr></thead><tbody>{rows or "<tr><td colspan=5 style=padding:20px;text-align:center;color:#94a3b8>No results</td></tr>"}</tbody></table></div>', unsafe_allow_html=True)
        if fc and st.button("⬇️ Export CSV", key="exp_csv"):
            st.download_button("Download CSV", pd.DataFrame(fc).to_csv(index=False), "candidates.csv", "text/csv")

    with tab3:
        sc_counts = {s: sum(1 for c in all_c if c.get("status")==s) for s in STATUS_LIST}
        sc_cols   = {"New":"#2563eb","Called":"#16a34a","Follow-Up":"#d97706","Closed":"#dc2626","Placed":"#059669"}
        sc_bgs    = {"New":"#dbeafe","Called":"#dcfce7","Follow-Up":"#fef9c3","Closed":"#fee2e2","Placed":"#d1fae5"}
        maxv = max(sc_counts.values()) if sc_counts else 1
        bars = "".join(f'<div style="margin-bottom:12px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px"><span style="font-size:13px;color:#374151;font-weight:500">{s}</span><span style="background:{sc_bgs[s]};color:{sc_cols[s]};border-radius:5px;padding:1px 8px;font-size:12px;font-weight:700">{v}</span></div><div style="height:6px;background:#f1f5f9;border-radius:3px"><div style="height:6px;width:{int((v/maxv)*100)}%;background:{sc_cols[s]};border-radius:3px"></div></div></div>' for s,v in sc_counts.items())

        bands = {"≥75 Strong":0,"50–74 Medium":0,"<50 Weak":0,"Unscored":0}
        for c in all_c:
            s = c.get("ai_score")
            if not s: bands["Unscored"]+=1
            elif s>=75: bands["≥75 Strong"]+=1
            elif s>=50: bands["50–74 Medium"]+=1
            else: bands["<50 Weak"]+=1
        bc  = {"≥75 Strong":"#16a34a","50–74 Medium":"#d97706","<50 Weak":"#dc2626","Unscored":"#94a3b8"}
        bcbg= {"≥75 Strong":"#dcfce7","50–74 Medium":"#fef9c3","<50 Weak":"#fee2e2","Unscored":"#f1f5f9"}
        tot = sum(bands.values()) or 1
        dist = "".join(f'<div style="display:flex;align-items:center;justify-content:space-between;padding:9px 0;border-bottom:1px solid #f1f5f9"><div style="display:flex;align-items:center;gap:8px"><div style="width:10px;height:10px;border-radius:50%;background:{bc[b]}"></div><span style="font-size:13px;color:#374151;font-weight:500">{b}</span></div><div style="display:flex;align-items:center;gap:8px"><span style="font-size:15px;font-weight:800;color:{bc[b]}">{v}</span><span style="background:{bcbg[b]};color:{bc[b]};border-radius:5px;padding:1px 8px;font-size:11px;font-weight:600">{int((v/tot)*100)}%</span></div></div>' for b,v in bands.items())

        ga, gb = st.columns(2)
        with ga: st.markdown(f'<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:12px">Pipeline by Status</div><div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.04)">{bars}</div>', unsafe_allow_html=True)
        with gb: st.markdown(f'<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:12px">Score Distribution</div><div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.04)">{dist}</div>', unsafe_allow_html=True)

    with tab4:
        s1, s2 = st.columns(2)
        with s1:
            with st.expander("🗄️ Supabase", expanded=True):
                su = st.text_input("URL", value=st.session_state.sb_url, key="adm_su")
                sk = st.text_input("Key", value=st.session_state.sb_key, type="password", key="adm_sk")
                if st.button("Update", key="adm_sb_save"):
                    st.session_state.sb_url=su; st.session_state.sb_key=sk
                    st.session_state.candidates=None; st.success("Saved!")
        with s2:
            with st.expander("📞 Bland.ai", expanded=True):
                bki = st.text_input("API Key", value=st.session_state.bland_key, type="password", key="adm_bk")
                if st.button("Update Key", key="adm_bk_save"):
                    st.session_state.bland_key=bki; st.success("Saved!")

        st.markdown("---")
        if sb: st.success("✓ Connected to Supabase")
        else: st.warning("⚠ Not connected to Supabase — running in demo mode")

        st.markdown("""
        <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:20px;margin-top:16px;box-shadow:0 1px 3px rgba(0,0,0,.04)">
          <div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:14px">Three-App Pipeline</div>
          <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
            <div style="background:#dbeafe;border:1px solid #bfdbfe;border-radius:8px;padding:8px 16px;color:#1e40af;font-weight:600;font-size:13px">🔍 Sourcer</div>
            <div style="color:#cbd5e1;font-size:18px;font-weight:300">→</div>
            <div style="background:#2563eb;border-radius:8px;padding:8px 16px;color:#fff;font-weight:600;font-size:13px">📞 The Caller</div>
            <div style="color:#cbd5e1;font-size:18px;font-weight:300">→</div>
            <div style="background:#dbeafe;border:1px solid #bfdbfe;border-radius:8px;padding:8px 16px;color:#1e40af;font-weight:600;font-size:13px">✅ Validator</div>
          </div>
          <div style="margin-top:12px;font-size:12px;color:#94a3b8">Sourcer writes <code style="background:#f1f5f9;padding:1px 5px;border-radius:4px;color:#374151">status = New</code> · Validator reads <code style="background:#f1f5f9;padding:1px 5px;border-radius:4px;color:#374151">Called</code> / <code style="background:#f1f5f9;padding:1px 5px;border-radius:4px;color:#374151">Placed</code></div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  ROUTER
# ═══════════════════════════════════════════════════════════════
page = st.session_state.page
if   page == "landing": page_landing()
elif page == "login":   page_login()
elif page == "signup":  page_signup()
elif page == "app":     page_app()
elif page == "admin":   page_admin()
else:
    st.session_state.page = "landing"; st.rerun()
