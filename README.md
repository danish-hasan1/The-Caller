# 📞 The Caller — AI Recruitment Agent v2

## 🗂 File Structure
```
app.py                          # Main router (entry point)
requirements.txt
supabase_schema.sql             # Run once in Supabase SQL Editor
pages_internal/
  __init__.py
  utils.py                      # Supabase, Bland.ai, AI scoring, helpers
  landing.py                    # Public landing page
  auth.py                       # Login + Signup
  main_app.py                   # Recruiter pipeline view
  admin.py                      # Admin dashboard
```

## 🚀 Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to share.streamlit.io → New app → your repo → `app.py`
3. Add secrets:
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
```

## 🔑 Default Admin Login
```
Email:    admin@thecaller.ai
Password: admin123
```
Change this in Supabase after first login.

## 🗄️ Supabase Setup
1. Create project at supabase.com (free)
2. SQL Editor → paste `supabase_schema.sql` → Run
3. Copy URL + Anon Key

## 📞 Bland.ai Setup
1. Sign up at bland.ai (free trial)
2. Get API key from dashboard
3. Enter in app Settings sidebar or Admin → Settings

## 🔗 Pipeline Integration
- **Sourcer** → writes to `candidates` table with `status = 'New'` and `user_id`
- **The Caller** → updates `status`, `transcript`, `ai_score`, `followup_date`  
- **Validator** → reads candidates with `status IN ('Called', 'Placed')`
