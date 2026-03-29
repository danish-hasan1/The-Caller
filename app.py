import streamlit as st
import requests
import json
import hashlib
import pandas as pd
from datetime import datetime, date

st.set_page_config(
    page_title="The Caller · AI Recruitment Agent",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════
#  GLOBAL STYLES
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:        #0d1117;
  --surface:   #161b22;
  --surface2:  #1c2330;
  --surface3:  #21262d;
  --border:    #30363d;
  --border2:   #3d444d;
  --accent:    #2563eb;
  --accent-h:  #1d4ed8;
  --green:     #16a34a;
  --amber:     #d97706;
  --red:       #dc2626;
  --text:      #e6edf3;
  --text2:     #8b949e;
  --text3:     #656d76;
  --r:         10px;
  --rl:        16px;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMain"],
section[data-testid="stSidebar"] + div { 
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="collapsedControl"],
[data-testid="stDecoration"] { display: none !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

/* Inputs */
.stTextInput > div > div > input,
.stTextArea textarea,
.stNumberInput input {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
  color: var(--text) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(37,99,235,.15) !important;
  outline: none !important;
}

/* Labels */
.stTextInput label, .stTextArea label,
.stSelectbox label, .stNumberInput label, .stDateInput label {
  color: var(--text2) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
}

/* Buttons — primary */
.stButton > button {
  background: var(--accent) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--r) !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  padding: 9px 18px !important;
  transition: background .15s !important;
  width: 100%;
}
.stButton > button:hover { background: var(--accent-h) !important; }

/* Tabs */
[data-testid="stTabs"] [role="tab"] {
  font-family: 'Inter', sans-serif !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  color: var(--text2) !important;
  padding: 8px 16px !important;
  border-radius: 0 !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  color: var(--accent) !important;
  border-bottom: 2px solid var(--accent) !important;
  background: transparent !important;
}
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
}
[data-testid="stTabsContent"] { padding-top: 16px !important; }

/* Selectbox */
[data-baseweb="select"] > div {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
  color: var(--text) !important;
}
[data-baseweb="menu"] {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
}
[data-baseweb="option"] { background: var(--surface2) !important; color: var(--text) !important; }
[data-baseweb="option"]:hover { background: var(--surface3) !important; }

/* Expander */
[data-testid="stExpander"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
}
details summary { color: var(--text) !important; font-size: 14px !important; }

/* Date input */
.stDateInput input {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: var(--r) !important;
}

/* Alerts */
[data-testid="stAlert"] { border-radius: var(--r) !important; }

/* Checkbox */
.stCheckbox label p { color: var(--text) !important; font-size: 14px !important; }

/* Multiselect */
[data-baseweb="tag"] { background: var(--surface3) !important; }

/* Form */
[data-testid="stForm"] {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
}

hr { border-color: var(--border) !important; margin: 16px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════════
for k, v in {
    "page": "landing", "user": None, "candidates": None,
    "selected_id": None, "active_calls": {}, "show_add": False,
    "sb_url": "", "sb_key": "", "bland_key": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════════
#  UTILITIES
# ═══════════════════════════════════════════════════════════════════
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

STATUS_CFG = {
    "New":       ("#1e3a5f", "#60a5fa", "#3b82f6"),
    "Called":    ("#14532d", "#4ade80", "#16a34a"),
    "Follow-Up": ("#451a03", "#fbbf24", "#d97706"),
    "Closed":    ("#450a0a", "#f87171", "#dc2626"),
    "Placed":    ("#052e16", "#34d399", "#059669"),
}

def badge(status):
    bg, txt, bdr = STATUS_CFG.get(status, ("#1c2330", "#8b949e", "#30363d"))
    return f'<span style="display:inline-block;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:600;letter-spacing:.3px;background:{bg};color:{txt};border:1px solid {bdr}">{status}</span>'

def sc_color(s):
    if s is None: return "#8b949e"
    if s >= 75:   return "#4ade80"
    if s >= 50:   return "#fbbf24"
    return "#f87171"

def card(content, padding="20px 24px", mb="12px", border_color="#30363d"):
    st.markdown(f'<div style="background:#161b22;border:1px solid {border_color};border-radius:12px;padding:{padding};margin-bottom:{mb}">{content}</div>', unsafe_allow_html=True)

DEMO_CANDIDATES = [
    {"id":1,"user_id":1,"name":"Aditya Sharma","phone":"+91-98765-43210","email":"aditya@email.com","role":"Senior Backend Engineer","experience":6,"skills":"Python, Django, AWS, PostgreSQL","status":"New","ai_score":None,"transcript":None,"followup_date":None,"notes":"","bland_call_id":None},
    {"id":2,"user_id":1,"name":"Priya Menon","phone":"+91-87654-32109","email":"priya@email.com","role":"Product Manager","experience":5,"skills":"Roadmapping, Agile, Data Analysis","status":"Called","ai_score":82,"transcript":"Agent: Hi Priya, I'm Alex calling from TalentBridge. Good time to talk?\nPriya: Yes, please go ahead.\nAgent: We have a Senior PM role at a SaaS company. Walk me through a product you've shipped recently?\nPriya: I led a 0-to-1 analytics dashboard — grew to 10k DAUs in 3 months.\nAgent: Impressive! CTC expectations?\nPriya: Currently 24 LPA, expecting 32–35.\nAgent: Notice period?\nPriya: 45 days, negotiable.\nAgent: Perfect. I'll share details and schedule next steps.","followup_date":"2025-04-05","notes":"Strong candidate. Interested, CTC aligned."},
    {"id":3,"user_id":1,"name":"Rajan Verma","phone":"+91-76543-21098","email":"rajan@email.com","role":"DevOps Engineer","experience":4,"skills":"Kubernetes, Terraform, CI/CD, AWS","status":"Follow-Up","ai_score":67,"transcript":"Agent: Hi Rajan, calling about a DevOps role at a fintech startup.\nRajan: Bit busy right now.\nAgent: Quick pitch — remote role, 25-30 LPA, strong K8s fit.\nRajan: Can you email details first?\nAgent: Absolutely. Reconnect Tuesday?\nRajan: Yes, Tuesday works.","followup_date":"2025-04-08","notes":"Requested JD on email. Call back Tuesday."},
    {"id":4,"user_id":1,"name":"Sneha Kulkarni","phone":"+91-65432-10987","email":"sneha@email.com","role":"Data Scientist","experience":3,"skills":"Python, ML, SQL, Tableau, TensorFlow","status":"Placed","ai_score":91,"transcript":"Strong call. Candidate very enthusiastic. Negotiated offer successfully.","followup_date":None,"notes":"Offer accepted. Joining April 15."},
    {"id":5,"user_id":1,"name":"Karan Patel","phone":"+91-54321-09876","email":"karan@email.com","role":"Frontend Engineer","experience":2,"skills":"React, TypeScript, Tailwind CSS","status":"Closed","ai_score":41,"transcript":"Candidate not interested in switching at this time.","followup_date":None,"notes":"Not interested. Revisit in 6 months."},
]

def load_candidates(sb, user_id=None):
    if sb:
        try:
            q = sb.table("candidates").select("*").order("created_at", desc=True)
            if user_id:
                q = q.eq("user_id", user_id)
            return q.execute().data or []
        except Exception as e:
            st.toast(f"DB: {e}", icon="⚠️")
    return DEMO_CANDIDATES

def load_all_candidates(sb):
    return load_candidates(sb)

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
        return None, "No database connected. Use admin@thecaller.ai / admin123"
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
Job Description: {jd}
Your goals: 1) Warm intro, confirm good time 2) Pitch the role 3) Ask current/expected CTC 4) Ask notice period 5) Gauge interest 6) Handle objections 7) Agree next steps or thank professionally.
Candidate: {candidate.get('experience','?')}y exp, Skills: {candidate.get('skills','')}
{('Extra context: ' + custom) if custom else ''}
Be conversational, warm, and consultative."""
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
                    f"Evaluate this candidate against the JD.\nJD: {jd}\nCandidate: {candidate['name']}, {candidate.get('experience','?')}y, Skills: {candidate.get('skills','')}\nTranscript:\n{transcript}\nRespond ONLY in JSON (no markdown):\n{{\"score\":<0-100>,\"summary\":\"<2-3 sentences>\",\"strengths\":[\"...\"],\"concerns\":[\"...\"],\"recommendation\":\"Proceed|Follow-Up|Reject\",\"suggested_ctc\":\"<range>\",\"next_step\":\"<action>\"}}"}]},
            headers={"Content-Type": "application/json"}, timeout=30)
        txt = r.json()["content"][0]["text"].strip().strip("```json").strip("```").strip()
        return json.loads(txt)
    except Exception as e:
        return {"score": 0, "summary": str(e), "strengths": [], "concerns": [], "recommendation": "Follow-Up", "suggested_ctc": "N/A", "next_step": "Manual review"}

# ═══════════════════════════════════════════════════════════════════
#  NAV BAR
# ═══════════════════════════════════════════════════════════════════
def nav_bar(active="app"):
    user = st.session_state.user
    if not user: return
    is_admin = user.get("role") == "admin"

    c1, c2, c3 = st.columns([2, 5, 3])
    with c1:
        st.markdown('<div style="display:flex;align-items:center;gap:10px;padding:10px 0"><span style="font-size:20px">📞</span><span style="font-weight:700;font-size:16px;color:#e6edf3;letter-spacing:-.3px">The Caller</span></div>', unsafe_allow_html=True)
    with c2:
        nb1, nb2, nb3 = st.columns([1, 1, 4])
        with nb1:
            if st.button("Pipeline", key="nav_pipeline"):
                st.session_state.page = "app"; st.rerun()
        with nb2:
            if is_admin:
                if st.button("Admin ⚙️", key="nav_admin"):
                    st.session_state.page = "admin"; st.rerun()
    with c3:
        nc1, nc2 = st.columns([3, 1])
        with nc1:
            role_tag = ' <span style="background:#1e3a5f;color:#60a5fa;border-radius:4px;padding:1px 7px;font-size:11px;font-weight:600">Admin</span>' if is_admin else ""
            st.markdown(f'<div style="text-align:right;padding:10px 0;font-size:13px;color:#8b949e">{user.get("name","")}{role_tag}</div>', unsafe_allow_html=True)
        with nc2:
            if st.button("Out", key="nav_out"):
                for k in ["user","candidates","selected_id","active_calls","show_add"]:
                    st.session_state[k] = None if k in ["user","candidates","selected_id"] else ([] if k == "active_calls" else False)
                st.session_state.active_calls = {}
                st.session_state.page = "landing"
                st.rerun()

    st.markdown('<hr style="margin:0 0 20px">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  PAGE: LANDING
# ═══════════════════════════════════════════════════════════════════
def page_landing():
    st.markdown("""
    <style>
    .land { max-width:860px; margin:0 auto; padding:70px 24px 60px; }
    .eyebrow { display:inline-flex;align-items:center;gap:8px;background:#1e3a5f;border:1px solid #3b82f6;border-radius:20px;padding:4px 14px;font-size:12px;font-weight:600;color:#60a5fa;letter-spacing:.5px;text-transform:uppercase;margin-bottom:24px; }
    .h1 { font-size:clamp(34px,6vw,58px);font-weight:800;line-height:1.1;color:#e6edf3;letter-spacing:-1.5px;margin-bottom:18px; }
    .h1 em { font-style:normal;color:#2563eb; }
    .sub { font-size:17px;color:#8b949e;line-height:1.65;max-width:560px;margin-bottom:36px; }
    .pipe-row { display:flex;align-items:center;background:#161b22;border:1px solid #30363d;border-radius:12px;padding:5px;width:fit-content;margin-bottom:60px; }
    .pipe-step { padding:10px 22px;border-radius:8px;font-size:14px;font-weight:600;color:#8b949e; }
    .pipe-step.on { background:#1e3a5f;color:#60a5fa;border:1px solid #3b82f6; }
    .pipe-arr { padding:0 6px;color:#3d444d;font-size:16px; }
    .feat-grid { display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-bottom:60px; }
    .feat { background:#161b22;border:1px solid #30363d;border-radius:12px;padding:22px;transition:border-color .2s; }
    .feat:hover { border-color:#3b82f6; }
    .feat-ico { width:38px;height:38px;background:#1e3a5f;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:18px;margin-bottom:12px; }
    .feat-t { font-size:14px;font-weight:700;color:#e6edf3;margin-bottom:5px; }
    .feat-d { font-size:13px;color:#8b949e;line-height:1.55; }
    .stats { display:flex;gap:40px;flex-wrap:wrap;border-top:1px solid #30363d;border-bottom:1px solid #30363d;padding:28px 0;margin-bottom:50px; }
    .stat { flex:1;min-width:100px;text-align:center; }
    .stat-n { font-size:34px;font-weight:800;color:#2563eb; }
    .stat-l { font-size:12px;color:#8b949e;margin-top:3px; }
    .foot { text-align:center;font-size:12px;color:#656d76;border-top:1px solid #30363d;padding-top:28px; }
    </style>

    <div class="land">
      <div class="eyebrow">🤖 AI-Powered Recruitment</div>
      <h1 class="h1">Your recruiter,<br><em>fully automated.</em></h1>
      <p class="sub">The Caller is an AI calling agent that connects with candidates, evaluates fit, negotiates offers, and keeps your pipeline moving — hands-free.</p>

      <div class="pipe-row">
        <div class="pipe-step">🔍 Sourcer</div>
        <div class="pipe-arr">→</div>
        <div class="pipe-step on">📞 The Caller</div>
        <div class="pipe-arr">→</div>
        <div class="pipe-step">✅ Validator</div>
      </div>

      <div class="feat-grid">
        <div class="feat"><div class="feat-ico">📞</div><div class="feat-t">AI Phone Calls</div><div class="feat-d">Calls candidates via Bland.ai with a natural, human-like voice and structured conversation.</div></div>
        <div class="feat"><div class="feat-ico">🧠</div><div class="feat-t">Smart Evaluation</div><div class="feat-d">Claude AI scores each candidate against your JD after every call with detailed insights.</div></div>
        <div class="feat"><div class="feat-ico">💬</div><div class="feat-t">Negotiation & Closing</div><div class="feat-d">Handles CTC negotiation, notice periods, and candidate objections professionally.</div></div>
        <div class="feat"><div class="feat-ico">🔔</div><div class="feat-t">Follow-Up Tracking</div><div class="feat-d">Tracks follow-up dates and keeps your pipeline moving without manual effort.</div></div>
        <div class="feat"><div class="feat-ico">🗄️</div><div class="feat-t">Supabase Sync</div><div class="feat-d">Shares candidate data seamlessly with your Sourcer and Validator apps.</div></div>
        <div class="feat"><div class="feat-ico">📊</div><div class="feat-t">Admin Analytics</div><div class="feat-d">Real-time dashboard with placement rates, AI scores, and team performance.</div></div>
      </div>

      <div class="stats">
        <div class="stat"><div class="stat-n">10×</div><div class="stat-l">Faster outreach</div></div>
        <div class="stat"><div class="stat-n">3</div><div class="stat-l">Apps. One pipeline.</div></div>
        <div class="stat"><div class="stat-n">0</div><div class="stat-l">Manual calls</div></div>
        <div class="stat"><div class="stat-n">100%</div><div class="stat-l">Free to deploy</div></div>
      </div>

      <div class="foot">Built on Streamlit · Bland.ai · Claude AI · Supabase</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="max-width:860px;margin:0 auto;padding:0 24px 60px">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 2, 6])
    with c1:
        if st.button("Get Started →", key="land_signup"):
            st.session_state.page = "signup"; st.rerun()
    with c2:
        if st.button("Sign In", key="land_login"):
            st.session_state.page = "login"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  PAGE: LOGIN
# ═══════════════════════════════════════════════════════════════════
def page_login():
    sb = get_sb()
    st.markdown("""
    <style>
    .auth-outer { display:flex;justify-content:center;padding:48px 16px 0; }
    .auth-logo { text-align:center;margin-bottom:28px; }
    .auth-ico { width:50px;height:50px;background:#1e3a5f;border:1px solid #3b82f6;border-radius:13px;display:inline-flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:10px; }
    .auth-name { font-size:20px;font-weight:700;color:#e6edf3; }
    .auth-sub2 { font-size:13px;color:#8b949e;margin-top:2px; }
    .auth-card { background:#161b22;border:1px solid #30363d;border-radius:16px;padding:30px; }
    .auth-h { font-size:21px;font-weight:700;color:#e6edf3;margin-bottom:4px; }
    .auth-sh { font-size:13px;color:#8b949e;margin-bottom:22px; }
    .demo-box { background:#0d1f36;border:1px solid #1e3a5f;border-radius:8px;padding:10px 14px;font-size:12px;color:#60a5fa;font-family:'JetBrains Mono',monospace;margin-bottom:18px; }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="auth-logo">
          <div class="auth-ico">📞</div>
          <div class="auth-name">The Caller</div>
          <div class="auth-sub2">AI Recruitment Agent</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("← Back to home", key="login_back"):
            st.session_state.page = "landing"; st.rerun()

        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<div class="auth-h">Welcome back</div><div class="auth-sh">Sign in to your account</div>', unsafe_allow_html=True)

        if not sb:
            st.markdown('<div class="demo-box">Demo mode — no DB connected<br>admin@thecaller.ai &nbsp;/&nbsp; admin123</div>', unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Email address", placeholder="you@example.com")
            pw    = st.text_input("Password", type="password", placeholder="••••••••")
            sub   = st.form_submit_button("Sign In", use_container_width=True)
            if sub:
                if not email or not pw:
                    st.error("Please fill in all fields.")
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
        st.markdown('<div style="text-align:center;margin-top:16px;font-size:13px;color:#8b949e">Don\'t have an account?</div>', unsafe_allow_html=True)
        if st.button("Create Account", key="to_signup", use_container_width=True):
            st.session_state.page = "signup"; st.rerun()

# ═══════════════════════════════════════════════════════════════════
#  PAGE: SIGNUP
# ═══════════════════════════════════════════════════════════════════
def page_signup():
    sb = get_sb()

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style="text-align:center;margin-bottom:28px">
          <div style="width:50px;height:50px;background:#1e3a5f;border:1px solid #3b82f6;border-radius:13px;display:inline-flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:10px">📞</div>
          <div style="font-size:20px;font-weight:700;color:#e6edf3">The Caller</div>
          <div style="font-size:13px;color:#8b949e;margin-top:2px">AI Recruitment Agent</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("← Back to home", key="signup_back"):
            st.session_state.page = "landing"; st.rerun()

        if not sb:
            st.warning("⚠️ No database connected. Configure Supabase to enable registration.")
            st.info("For demo access → Sign In with admin@thecaller.ai / admin123")
            if st.button("Go to Sign In", key="to_login"):
                st.session_state.page = "login"; st.rerun()
            return

        st.markdown('<div style="background:#161b22;border:1px solid #30363d;border-radius:16px;padding:30px">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:21px;font-weight:700;color:#e6edf3;margin-bottom:4px">Create account</div><div style="font-size:13px;color:#8b949e;margin-bottom:22px">Start automating your recruitment calls</div>', unsafe_allow_html=True)

        with st.form("signup_form"):
            name    = st.text_input("Full Name", placeholder="Your name")
            email   = st.text_input("Email address", placeholder="you@example.com")
            pw      = st.text_input("Password", type="password", placeholder="Min. 8 characters")
            confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
            agree   = st.checkbox("I agree to the terms of service")
            sub     = st.form_submit_button("Create Account", use_container_width=True)
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
                    with st.spinner("Creating account..."):
                        user, err = signup_user(sb, name, email, pw)
                    if user:
                        st.session_state.user = user
                        st.session_state.page = "app"
                        st.rerun()
                    else:
                        st.error(err)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;margin-top:16px;font-size:13px;color:#8b949e">Already have an account?</div>', unsafe_allow_html=True)
        if st.button("Sign In", key="to_login2", use_container_width=True):
            st.session_state.page = "login"; st.rerun()

# ═══════════════════════════════════════════════════════════════════
#  PAGE: MAIN APP
# ═══════════════════════════════════════════════════════════════════
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
            if st.button("Save", key="bk_save"):
                st.session_state.bland_key = bk; st.success("Saved!")
        st.markdown("---")
        st.markdown("### 🔍 Filters")
        sf = st.multiselect("Status", STATUS_LIST, default=["New","Called","Follow-Up"], key="sf")
        sq = st.text_input("Search", placeholder="Name, role, skills…", key="sq")
        if st.button("🔄 Refresh", use_container_width=True, key="refresh"):
            st.session_state.candidates = None; st.rerun()

    nav_bar("app")

    # Filter
    filtered = [
        c for c in candidates
        if (not sf or c["status"] in sf)
        and (not sq or any(sq.lower() in str(c.get(f,"")).lower() for f in ["name","role","skills","email"]))
    ]

    # KPIs
    total  = len(candidates)
    new_c  = sum(1 for c in candidates if c["status"] == "New")
    active = sum(1 for c in candidates if c["status"] in ["Called","Follow-Up"])
    placed = sum(1 for c in candidates if c["status"] == "Placed")
    scores = [c["ai_score"] for c in candidates if c.get("ai_score")]
    avg_sc = int(sum(scores)/len(scores)) if scores else None
    today  = str(date.today())
    ov     = sum(1 for c in candidates if c.get("followup_date") and c["followup_date"] < today)

    sc_c = sc_color(avg_sc)
    ov_c = "#f87171" if ov > 0 else "#4ade80"

    st.markdown(f"""
    <style>
    .kpi-row {{ display:flex;gap:10px;margin-bottom:24px;flex-wrap:wrap; }}
    .kpi {{ flex:1;min-width:110px;background:#161b22;border:1px solid #30363d;border-radius:10px;padding:14px 18px; }}
    .kpi-v {{ font-size:26px;font-weight:800;color:#e6edf3;line-height:1; }}
    .kpi-l {{ font-size:10px;color:#8b949e;margin-top:4px;text-transform:uppercase;letter-spacing:.8px; }}
    </style>
    <div class="kpi-row">
      <div class="kpi"><div class="kpi-v">{total}</div><div class="kpi-l">Pipeline</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#60a5fa">{new_c}</div><div class="kpi-l">Pending</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#fbbf24">{active}</div><div class="kpi-l">In Progress</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#4ade80">{placed}</div><div class="kpi-l">Placed</div></div>
      <div class="kpi"><div class="kpi-v" style="color:{sc_c}">{avg_sc if avg_sc else '—'}</div><div class="kpi-l">Avg Score</div></div>
      <div class="kpi"><div class="kpi-v" style="color:{ov_c}">{ov}</div><div class="kpi-l">Overdue</div></div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([5, 7], gap="large")

    # ── LEFT: List ────────────────────────────────────────────────────────────
    with left:
        h1, h2 = st.columns([4, 1])
        with h1:
            st.markdown(f'<div style="font-size:15px;font-weight:600;color:#e6edf3;margin-bottom:10px">Candidates <span style="color:#8b949e;font-weight:400;font-size:13px">({len(filtered)})</span></div>', unsafe_allow_html=True)
        with h2:
            if st.button("+ Add", key="add_toggle"):
                st.session_state.show_add = not st.session_state.show_add

        if st.session_state.show_add:
            with st.form("add_form"):
                st.markdown('<div style="font-weight:600;font-size:14px;margin-bottom:10px">New Candidate</div>', unsafe_allow_html=True)
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
                        obj = {"id": nid, "user_id": user.get("id", 1),
                               "name": n, "phone": ph, "email": em, "role": ro,
                               "experience": ex, "skills": sk, "status": "New",
                               "ai_score": None, "transcript": None,
                               "followup_date": None, "notes": "", "bland_call_id": None}
                        st.session_state.candidates.append(obj)
                        save_candidate(sb, obj)
                        st.session_state.show_add = False
                        st.rerun()
                    else:
                        st.error("Name, phone and role are required.")

        if not filtered:
            st.markdown('<div style="text-align:center;padding:40px;color:#8b949e"><div style="font-size:28px;margin-bottom:10px">🔍</div><div>No candidates match your filters</div></div>', unsafe_allow_html=True)

        for c in filtered:
            is_sel  = st.session_state.selected_id == c["id"]
            is_live = c["id"] in st.session_state.active_calls
            sc      = c.get("ai_score")
            sc_html = f'<span style="font-size:13px;font-weight:700;color:{sc_color(sc)}">{sc}</span>' if sc else ""
            live_dot = '<span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#f87171;margin-left:6px;vertical-align:middle"></span>' if is_live else ""
            bdr = "#3b82f6" if is_sel else "#30363d"

            st.markdown(f"""
            <div style="background:#161b22;border:1px solid {bdr};border-radius:10px;padding:12px 14px;margin-bottom:6px">
              <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div style="flex:1;min-width:0">
                  <div style="font-size:14px;font-weight:600;color:#e6edf3">{c['name']}{live_dot}</div>
                  <div style="font-size:12px;color:#8b949e;margin-top:2px">{c['role']} · {c.get('experience','?')}y</div>
                  <div style="margin-top:7px">{badge(c['status'])}</div>
                </div>
                <div style="text-align:right;flex-shrink:0;margin-left:12px">
                  {sc_html}{'<div style="font-size:10px;color:#656d76;margin-top:2px">score</div>' if sc else ''}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open →", key=f"sel_{c['id']}", use_container_width=True):
                st.session_state.selected_id = c["id"]; st.rerun()

    # ── RIGHT: Detail ─────────────────────────────────────────────────────────
    with right:
        sel_id = st.session_state.selected_id
        sel    = next((c for c in candidates if c["id"] == sel_id), None)

        if not sel:
            st.markdown("""
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                        height:380px;background:#161b22;border:1px solid #30363d;border-radius:12px;
                        color:#656d76;text-align:center">
              <div style="font-size:36px;margin-bottom:12px">📋</div>
              <div style="font-size:15px;font-weight:600;color:#8b949e">Select a candidate</div>
              <div style="font-size:13px;margin-top:4px">Click any candidate on the left</div>
            </div>
            """, unsafe_allow_html=True)
            return

        sc = sel.get("ai_score")
        sc_badge = f'<div style="text-align:center;background:#0d1117;border:2px solid {sc_color(sc)};border-radius:50%;width:60px;height:60px;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;color:{sc_color(sc)};flex-shrink:0">{sc}</div>' if sc else ""

        st.markdown(f"""
        <div style="background:#161b22;border:1px solid #30363d;border-radius:12px;padding:18px 22px;margin-bottom:14px">
          <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
              <div style="font-size:19px;font-weight:700;color:#e6edf3">{sel['name']}</div>
              <div style="font-size:13px;color:#8b949e;margin-top:3px">{sel['role']} · {sel.get('experience','?')} yrs</div>
              <div style="margin-top:9px;display:flex;gap:8px;flex-wrap:wrap;align-items:center">
                {badge(sel['status'])}
                <span style="font-size:12px;color:#8b949e">{sel.get('phone','')}</span>
              </div>
            </div>
            {sc_badge}
          </div>
        </div>
        """, unsafe_allow_html=True)

        t1, t2, t3, t4 = st.tabs(["Profile", "📞 Call", "🧠 Evaluation", "🔔 Follow-Ups"])

        # Profile
        with t1:
            st.markdown(f'<div style="font-size:12px;color:#8b949e;margin-bottom:4px">Skills</div><div style="font-size:13px;font-family:JetBrains Mono,monospace;background:#1c2330;border:1px solid #30363d;border-radius:8px;padding:8px 12px;margin-bottom:14px;color:#e6edf3">{sel.get("skills","—")}</div>', unsafe_allow_html=True)
            new_notes  = st.text_area("Notes", value=sel.get("notes","") or "", height=110, key="notes_ta")
            sa, sb_col = st.columns(2)
            with sa:
                new_status = st.selectbox("Status", STATUS_LIST, index=STATUS_LIST.index(sel.get("status","New")), key="status_sel")
            with sb_col:
                st.markdown('<div style="height:26px"></div>', unsafe_allow_html=True)
                if st.button("💾 Save", use_container_width=True, key="save_profile"):
                    for i, c in enumerate(st.session_state.candidates):
                        if c["id"] == sel["id"]:
                            st.session_state.candidates[i]["notes"]  = new_notes
                            st.session_state.candidates[i]["status"] = new_status
                            save_candidate(sb, st.session_state.candidates[i])
                    st.success("Saved!"); st.rerun()

        # Call
        with t2:
            jd = st.text_area("Job Description *", placeholder="Paste the full JD or a summary. The AI agent uses this to pitch and evaluate.", height=100, key="jd_call")
            ci = st.text_area("Agent Instructions (optional)", placeholder="e.g. Be warm. Mention remote culture. Budget 28–35 LPA.", height=60, key="ci_call")
            bk = st.session_state.bland_key
            ca, cb = st.columns(2)
            with ca:
                if not bk:
                    st.warning("Add Bland.ai key in sidebar Settings.")
                elif st.button("📞 Start AI Call", use_container_width=True, key="start_call"):
                    if not jd.strip():
                        st.error("Paste the JD first.")
                    else:
                        with st.spinner(f"Calling {sel['name']}..."):
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
                            st.error(f"Failed: {res.get('error', res)}")
            with cb:
                acid = st.session_state.active_calls.get(sel["id"]) or sel.get("bland_call_id")
                if acid and st.button("🔄 Fetch Transcript", use_container_width=True, key="fetch_tx"):
                    with st.spinner("Fetching..."):
                        data = fetch_call(bk, acid)
                    tx = data.get("transcript","") or "\n".join(
                        [f"{t.get('user','?')}: {t.get('text','')}" for t in data.get("transcripts",[])])
                    if tx:
                        for i, c in enumerate(st.session_state.candidates):
                            if c["id"] == sel["id"]:
                                st.session_state.candidates[i]["transcript"] = tx
                                save_candidate(sb, st.session_state.candidates[i])
                        st.success("Fetched!"); st.rerun()
                    else:
                        st.info(f"Status: {data.get('status','pending')} — try again shortly.")

            st.markdown("---")
            st.markdown('<div style="font-size:13px;color:#8b949e;margin-bottom:6px">Transcript</div>', unsafe_allow_html=True)
            mtx = st.text_area("", value=sel.get("transcript","") or "", height=170,
                               label_visibility="collapsed", key="mtx",
                               placeholder="Transcript appears here after a call, or paste manually.")
            if st.button("💾 Save Transcript", use_container_width=True, key="save_tx"):
                for i, c in enumerate(st.session_state.candidates):
                    if c["id"] == sel["id"]:
                        st.session_state.candidates[i]["transcript"] = mtx
                        save_candidate(sb, st.session_state.candidates[i])
                st.success("Saved!")

        # Evaluation
        with t3:
            if not sel.get("transcript"):
                st.markdown('<div style="text-align:center;padding:48px;color:#8b949e"><div style="font-size:32px;margin-bottom:12px">📞</div><div style="font-size:15px;font-weight:600;color:#e6edf3">Complete a call first</div><div style="font-size:13px;margin-top:4px">Save the transcript in the Call tab, then run evaluation.</div></div>', unsafe_allow_html=True)
            else:
                jde = st.text_area("Job Description", placeholder="Paste JD to score against…", height=90, key="jd_eval")
                if st.button("⚡ Run AI Evaluation", use_container_width=True, key="run_eval"):
                    if not jde.strip():
                        st.error("Paste the JD first.")
                    else:
                        with st.spinner("Claude is evaluating..."):
                            res = score_ai(sel, jde, sel["transcript"])
                        score = res.get("score", 0)
                        for i, c in enumerate(st.session_state.candidates):
                            if c["id"] == sel["id"]:
                                st.session_state.candidates[i]["ai_score"] = score
                                note = f"\n[AI Eval {datetime.now().strftime('%d %b %H:%M')}] {res.get('summary','')}"
                                st.session_state.candidates[i]["notes"] = (c.get("notes","") or "") + note
                                save_candidate(sb, st.session_state.candidates[i])
                        col   = sc_color(score)
                        rec   = res.get("recommendation","—")
                        rc    = {"Proceed":"#4ade80","Follow-Up":"#fbbf24","Reject":"#f87171"}.get(rec,"#8b949e")
                        st.markdown(f"""
                        <div style="background:#161b22;border:1px solid #30363d;border-radius:12px;padding:18px;margin:10px 0">
                          <div style="display:flex;gap:16px;align-items:center;margin-bottom:14px">
                            <div style="width:62px;height:62px;border-radius:50%;border:2px solid {col};display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;color:{col};flex-shrink:0">{score}</div>
                            <div>
                              <div style="font-size:16px;font-weight:700;color:#e6edf3">{sel['name']}</div>
                              <div style="margin-top:5px"><span style="background:#1c2330;border:1px solid {rc};color:{rc};border-radius:6px;padding:2px 10px;font-size:12px;font-weight:600">{rec}</span>
                              <span style="font-size:13px;color:#8b949e;margin-left:8px">{res.get('suggested_ctc','')}</span></div>
                            </div>
                          </div>
                          <p style="font-size:13px;color:#8b949e;line-height:1.6;margin-bottom:14px">{res.get('summary','')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        ea, eb = st.columns(2)
                        with ea:
                            st.markdown('<div style="font-size:13px;font-weight:600;color:#4ade80;margin-bottom:6px">✓ Strengths</div>', unsafe_allow_html=True)
                            for s in res.get("strengths",[]): st.markdown(f'<div style="font-size:13px;color:#8b949e;padding:3px 0;border-bottom:1px solid #21262d">· {s}</div>', unsafe_allow_html=True)
                        with eb:
                            st.markdown('<div style="font-size:13px;font-weight:600;color:#f87171;margin-bottom:6px">⚠ Concerns</div>', unsafe_allow_html=True)
                            for s in res.get("concerns",[]): st.markdown(f'<div style="font-size:13px;color:#8b949e;padding:3px 0;border-bottom:1px solid #21262d">· {s}</div>', unsafe_allow_html=True)
                        if res.get("next_step"):
                            st.markdown(f'<div style="margin-top:10px;background:#1e3a5f;border:1px solid #3b82f6;border-radius:8px;padding:10px 14px;font-size:13px;color:#60a5fa">💡 {res["next_step"]}</div>', unsafe_allow_html=True)
                        st.rerun()

                if sel.get("ai_score"):
                    st.markdown(f'<div style="margin-top:8px;font-size:13px;color:#8b949e">Stored score: <span style="color:{sc_color(sel["ai_score"])};font-weight:700;font-size:18px">{sel["ai_score"]}/100</span></div>', unsafe_allow_html=True)

        # Follow-Ups
        with t4:
            fa, fb = st.columns(2)
            with fa:
                fud = st.date_input("Schedule Date", value=date.today(), key="fud")
            fun = st.text_area("Reminder Note", height=70, key="fun", placeholder="e.g. Send offer letter. Call at 11 AM.")
            if st.button("📅 Schedule Follow-Up", use_container_width=True, key="save_fu"):
                for i, c in enumerate(st.session_state.candidates):
                    if c["id"] == sel["id"]:
                        entry = f"\n[Follow-Up: {fud}] {fun}"
                        st.session_state.candidates[i]["followup_date"] = str(fud)
                        st.session_state.candidates[i]["status"]        = "Follow-Up"
                        st.session_state.candidates[i]["notes"]         = (c.get("notes","") or "") + entry
                        save_candidate(sb, st.session_state.candidates[i])
                st.success(f"Scheduled for {fud}!"); st.rerun()

            st.markdown("---")
            st.markdown('<div style="font-size:14px;font-weight:600;color:#e6edf3;margin-bottom:10px">All Follow-Ups</div>', unsafe_allow_html=True)
            fu_list = sorted([(c["name"],c["followup_date"],c["role"],c["id"]) for c in candidates if c.get("followup_date")], key=lambda x: x[1])
            today_s = str(date.today())
            if not fu_list:
                st.markdown('<div style="font-size:13px;color:#656d76">None scheduled yet.</div>', unsafe_allow_html=True)
            for nm, fd, rl, cid in fu_list:
                overdue = fd < today_s; is_today = fd == today_s
                dc = "#f87171" if overdue else ("#fbbf24" if is_today else "#4ade80")
                lbl = f"OVERDUE · {fd}" if overdue else ("TODAY" if is_today else fd)
                hl = "border-left:3px solid #3b82f6;" if cid == sel_id else ""
                st.markdown(f'<div style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:#161b22;border:1px solid #30363d;border-radius:8px;margin-bottom:5px;{hl}"><div style="width:7px;height:7px;border-radius:50%;background:{dc};flex-shrink:0"></div><div style="flex:1"><div style="font-size:13px;font-weight:600;color:#e6edf3">{nm}</div><div style="font-size:12px;color:#8b949e">{rl}</div></div><div style="font-size:12px;color:{dc};font-family:JetBrains Mono,monospace">{lbl}</div></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  PAGE: ADMIN
# ═══════════════════════════════════════════════════════════════════
def page_admin():
    user = st.session_state.get("user")
    if not user: st.session_state.page = "login"; st.rerun()
    if user.get("role") != "admin": st.session_state.page = "app"; st.rerun()

    sb = get_sb()
    nav_bar("admin")

    # Load data
    all_c = load_all_candidates(sb)
    all_u = []
    if sb:
        try:
            all_u = sb.table("users").select("id,name,email,role,created_at").execute().data or []
        except: pass
    if not all_u:
        all_u = [
            {"id":0,"name":"Admin (Demo)","email":"admin@thecaller.ai","role":"admin","created_at":"2025-01-01"},
            {"id":1,"name":"Recruiter One","email":"recruiter1@example.com","role":"user","created_at":"2025-01-15"},
        ]

    # KPIs
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
    .adk {{ flex:1;min-width:110px;background:#161b22;border:1px solid #30363d;border-radius:10px;padding:14px 18px; }}
    .adk-v {{ font-size:26px;font-weight:800;color:#e6edf3;line-height:1; }}
    .adk-l {{ font-size:10px;color:#8b949e;margin-top:4px;text-transform:uppercase;letter-spacing:.8px; }}
    .adm-table {{ width:100%;border-collapse:collapse;font-size:13px;color:#e6edf3; }}
    .adm-table th {{ text-align:left;padding:9px 14px;background:#1c2330;color:#8b949e;font-size:11px;text-transform:uppercase;letter-spacing:.8px;font-weight:600;border-bottom:1px solid #30363d; }}
    .adm-table td {{ padding:9px 14px;border-bottom:1px solid #21262d;vertical-align:middle; }}
    .adm-table tr:hover td {{ background:#1c2330; }}
    .adm-card {{ background:#161b22;border:1px solid #30363d;border-radius:12px;overflow:hidden;margin-bottom:18px; }}
    .adm-ch {{ padding:12px 18px;border-bottom:1px solid #30363d;font-size:14px;font-weight:600;color:#e6edf3; }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="adkpi">
      <div class="adk"><div class="adk-v">{total_u}</div><div class="adk-l">Users</div></div>
      <div class="adk"><div class="adk-v">{total_c}</div><div class="adk-l">Candidates</div></div>
      <div class="adk"><div class="adk-v" style="color:#4ade80">{placed}</div><div class="adk-l">Placed</div></div>
      <div class="adk"><div class="adk-v" style="color:#60a5fa">{called}</div><div class="adk-l">Calls Made</div></div>
      <div class="adk"><div class="adk-v" style="color:{sc_color(avg_sc)}">{avg_sc or '—'}</div><div class="adk-l">Avg Score</div></div>
      <div class="adk"><div class="adk-v" style="color:#4ade80">{pr}%</div><div class="adk-l">Placement Rate</div></div>
      <div class="adk"><div class="adk-v" style="color:{'#f87171' if ov else '#4ade80'}">{ov}</div><div class="adk-l">Overdue</div></div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["👥 Users", "📋 Candidates", "📊 Analytics", "⚙️ Settings"])

    with tab1:
        rows = ""
        for u in all_u:
            rb = f'<span style="background:#1e3a5f;border:1px solid #3b82f6;color:#60a5fa;border-radius:5px;padding:2px 8px;font-size:11px;font-weight:600">{"Admin" if u.get("role")=="admin" else "User"}</span>'
            uc = [c for c in all_c if c.get("user_id")==u["id"]]
            rows += f'<tr><td style="font-weight:500">{u.get("name","")}</td><td style="color:#8b949e">{u.get("email","")}</td><td>{rb}</td><td style="text-align:center">{len(uc)}</td><td style="text-align:center;color:#4ade80">{sum(1 for c in uc if c.get("status")=="Placed")}</td><td style="color:#8b949e;font-size:12px">{str(u.get("created_at",""))[:10]}</td></tr>'
        st.markdown(f'<div class="adm-card"><div class="adm-ch">Registered Users ({len(all_u)})</div><table class="adm-table"><thead><tr><th>Name</th><th>Email</th><th>Role</th><th style="text-align:center">Candidates</th><th style="text-align:center">Placed</th><th>Joined</th></tr></thead><tbody>{rows}</tbody></table></div>', unsafe_allow_html=True)

        st.markdown("**Manage Role**")
        m1, m2, m3 = st.columns([3,2,1])
        with m1: te = st.selectbox("User", [u["email"] for u in all_u], key="role_email")
        with m2: nr = st.selectbox("Role", ["user","admin"], key="role_new")
        with m3:
            st.markdown('<div style="height:26px"></div>', unsafe_allow_html=True)
            if st.button("Update", key="role_upd"):
                if sb:
                    try: sb.table("users").update({"role":nr}).eq("email",te).execute(); st.success("Updated!"); st.rerun()
                    except Exception as e: st.error(str(e))
                else: st.info("Demo mode")

    with tab2:
        f1, f2 = st.columns([2,3])
        with f1: fs = st.multiselect("Status", STATUS_LIST, key="adm_sf")
        with f2: fq = st.text_input("Search", key="adm_sq", placeholder="Name, role, email…")
        fc = [c for c in all_c if (not fs or c.get("status") in fs) and (not fq or any(fq.lower() in str(c.get(f,"")).lower() for f in ["name","role","email","skills"]))]
        rows = "".join(f'<tr><td style="font-weight:500">{c.get("name","")}</td><td style="color:#8b949e">{c.get("role","")}</td><td>{badge(c.get("status","New"))}</td><td style="text-align:center;color:{sc_color(c.get("ai_score"))};font-weight:600">{c.get("ai_score","") or "—"}</td><td style="color:#8b949e;font-size:12px">{c.get("followup_date","") or "—"}</td></tr>' for c in fc)
        st.markdown(f'<div class="adm-card"><div class="adm-ch">All Candidates ({len(fc)})</div><table class="adm-table"><thead><tr><th>Name</th><th>Role</th><th>Status</th><th style="text-align:center">Score</th><th>Follow-Up</th></tr></thead><tbody>{rows if rows else "<tr><td colspan=5 style=padding:20px;text-align:center;color:#656d76>No results</td></tr>"}</tbody></table></div>', unsafe_allow_html=True)
        if fc and st.button("⬇️ Export CSV", key="exp_csv"):
            csv = pd.DataFrame(fc).to_csv(index=False)
            st.download_button("Download", csv, "candidates.csv", "text/csv")

    with tab3:
        sc_counts = {s: sum(1 for c in all_c if c.get("status")==s) for s in STATUS_LIST}
        sc_cols   = {"New":"#60a5fa","Called":"#4ade80","Follow-Up":"#fbbf24","Closed":"#f87171","Placed":"#34d399"}
        maxv = max(sc_counts.values()) if sc_counts else 1
        bars = "".join(f'<div style="margin-bottom:10px"><div style="display:flex;justify-content:space-between;margin-bottom:3px"><span style="font-size:13px;color:#8b949e">{s}</span><span style="font-size:13px;font-weight:600;color:{sc_cols[s]}">{v}</span></div><div style="height:5px;background:#1c2330;border-radius:3px"><div style="height:5px;width:{int((v/maxv)*100)}%;background:{sc_cols[s]};border-radius:3px"></div></div></div>' for s,v in sc_counts.items())

        bands = {"≥75 Strong":0,"50–74 Medium":0,"<50 Weak":0,"Unscored":0}
        for c in all_c:
            s = c.get("ai_score")
            if not s: bands["Unscored"]+=1
            elif s>=75: bands["≥75 Strong"]+=1
            elif s>=50: bands["50–74 Medium"]+=1
            else: bands["<50 Weak"]+=1
        bc = {"≥75 Strong":"#4ade80","50–74 Medium":"#fbbf24","<50 Weak":"#f87171","Unscored":"#656d76"}
        tot = sum(bands.values()) or 1
        dist = "".join(f'<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid #21262d"><div style="display:flex;align-items:center;gap:8px"><div style="width:9px;height:9px;border-radius:50%;background:{bc[b]}"></div><span style="font-size:13px;color:#8b949e">{b}</span></div><div><span style="font-size:15px;font-weight:700;color:{bc[b]}">{v}</span><span style="font-size:12px;color:#656d76;margin-left:6px">{int((v/tot)*100)}%</span></div></div>' for b,v in bands.items())

        ga, gb = st.columns(2)
        with ga: st.markdown(f'<div style="font-size:14px;font-weight:600;color:#e6edf3;margin-bottom:12px">Pipeline by Status</div><div style="background:#161b22;border:1px solid #30363d;border-radius:12px;padding:18px">{bars}</div>', unsafe_allow_html=True)
        with gb: st.markdown(f'<div style="font-size:14px;font-weight:600;color:#e6edf3;margin-bottom:12px">Score Distribution</div><div style="background:#161b22;border:1px solid #30363d;border-radius:12px;padding:18px">{dist}</div>', unsafe_allow_html=True)

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
                if st.button("Update", key="adm_bk_save"):
                    st.session_state.bland_key=bki; st.success("Saved!")

        st.markdown("---")
        st.success("✓ Connected to Supabase" if sb else "")
        if not sb: st.warning("⚠ Not connected to Supabase — running in demo mode")

        st.markdown("""
        <div style="background:#161b22;border:1px solid #30363d;border-radius:12px;padding:18px;margin-top:16px">
          <div style="font-size:14px;font-weight:600;color:#e6edf3;margin-bottom:12px">Three-App Pipeline</div>
          <div style="display:flex;align-items:center;gap:8px;font-size:13px;flex-wrap:wrap">
            <div style="background:#1e3a5f;border:1px solid #3b82f6;border-radius:8px;padding:8px 14px;color:#60a5fa;font-weight:600">🔍 Sourcer</div>
            <div style="color:#3d444d;font-size:18px">→</div>
            <div style="background:#052e16;border:1px solid #16a34a;border-radius:8px;padding:8px 14px;color:#4ade80;font-weight:600">📞 The Caller</div>
            <div style="color:#3d444d;font-size:18px">→</div>
            <div style="background:#1e3a5f;border:1px solid #3b82f6;border-radius:8px;padding:8px 14px;color:#60a5fa;font-weight:600">✅ Validator</div>
          </div>
          <div style="margin-top:10px;font-size:12px;color:#656d76">Sourcer writes status <code style="background:#1c2330;padding:1px 5px;border-radius:4px">New</code>. Validator reads <code style="background:#1c2330;padding:1px 5px;border-radius:4px">Called</code> / <code style="background:#1c2330;padding:1px 5px;border-radius:4px">Placed</code>.</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  ROUTER
# ═══════════════════════════════════════════════════════════════════
page = st.session_state.page
if   page == "landing": page_landing()
elif page == "login":   page_login()
elif page == "signup":  page_signup()
elif page == "app":     page_app()
elif page == "admin":   page_admin()
else:
    st.session_state.page = "landing"; st.rerun()
