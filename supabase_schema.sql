-- ═══════════════════════════════════════════════════════════════
--  THE CALLER · Supabase Schema v2
--  Run this in your Supabase SQL Editor
-- ═══════════════════════════════════════════════════════════════

-- ── Users ────────────────────────────────────────────────────────
create table if not exists users (
  id            bigserial primary key,
  name          text not null,
  email         text unique not null,
  password_hash text not null,
  role          text default 'user' check (role in ('user','admin')),
  created_at    timestamptz default now()
);

-- Seed admin account  (password: admin123)
insert into users (name, email, password_hash, role) values (
  'Admin',
  'admin@thecaller.ai',
  '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',  -- sha256('admin123')
  'admin'
) on conflict (email) do nothing;

-- ── Candidates ────────────────────────────────────────────────────
create table if not exists candidates (
  id              bigserial primary key,
  user_id         bigint references users(id) on delete set null,
  name            text not null,
  phone           text,
  email           text,
  role            text,
  experience      integer default 0,
  skills          text,
  status          text default 'New'
                    check (status in ('New','Called','Follow-Up','Closed','Placed')),
  ai_score        integer,
  transcript      text,
  followup_date   date,
  notes           text,
  bland_call_id   text,
  created_at      timestamptz default now(),
  updated_at      timestamptz default now()
);

-- Auto-update updated_at
create or replace function update_updated_at()
returns trigger as $$
begin new.updated_at = now(); return new; end;
$$ language plpgsql;

drop trigger if exists set_updated_at on candidates;
create trigger set_updated_at
  before update on candidates
  for each row execute function update_updated_at();

-- ── RLS ──────────────────────────────────────────────────────────
alter table users      enable row level security;
alter table candidates enable row level security;

-- Open policies for MVP (tighten later with Supabase Auth)
create policy "Allow all users"      on users      for all using (true) with check (true);
create policy "Allow all candidates" on candidates for all using (true) with check (true);

-- ── Sample candidates ─────────────────────────────────────────────
-- (Linked to admin user id=1 — adjust if needed)
insert into candidates (user_id, name, phone, email, role, experience, skills, status) values
  (1, 'Aditya Sharma',  '+91-98765-43210', 'aditya@email.com',  'Senior Backend Engineer', 6, 'Python, Django, AWS',           'New'),
  (1, 'Priya Menon',    '+91-87654-32109', 'priya@email.com',   'Product Manager',          5, 'Roadmapping, Agile, Data',     'New'),
  (1, 'Rajan Verma',    '+91-76543-21098', 'rajan@email.com',   'DevOps Engineer',          4, 'Kubernetes, Terraform, CI/CD', 'New')
on conflict do nothing;
