-- OpenNIW initial schema.
-- Everything lives in the dedicated "openniw" schema so a shared database
-- (e.g. a reused Supabase project) is never polluted. gen_random_uuid() is
-- built into Postgres 13+.
create schema if not exists openniw;
set search_path to openniw;

create table if not exists users (
    id uuid primary key default gen_random_uuid(),
    email text not null unique,
    password_hash text not null,
    created_at timestamptz not null default now()
);

create table if not exists cases (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(id) on delete cascade,
    title text not null default 'My NIW Case',
    field text,
    stage text not null default 'eval'
        check (stage in ('eval','collect','draft','forms','package','rfe')),
    created_at timestamptz not null default now()
);
create index if not exists cases_user_idx on cases(user_id);

create table if not exists profiles (
    case_id uuid primary key references cases(id) on delete cascade,
    scholar_url text,
    homepage_url text,
    raw jsonb not null default '{}'::jsonb,
    parsed jsonb not null default '{}'::jsonb,
    metrics jsonb not null default '{}'::jsonb,
    updated_at timestamptz not null default now()
);

create table if not exists evaluations (
    id uuid primary key default gen_random_uuid(),
    case_id uuid references cases(id) on delete cascade,
    email text,
    input_snapshot jsonb not null default '{}'::jsonb,
    report_md text,
    tier text,
    prong_scores jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);
create index if not exists evaluations_case_idx on evaluations(case_id);

create table if not exists evidence_items (
    id uuid primary key default gen_random_uuid(),
    case_id uuid not null references cases(id) on delete cascade,
    category text not null,
    title text not null,
    description text,
    status text not null default 'suggested'
        check (status in ('suggested','needed','provided','na')),
    source_url text,
    file_path text,
    ai_notes text,
    exhibit_no int,
    created_at timestamptz not null default now()
);
create index if not exists evidence_case_idx on evidence_items(case_id);

create table if not exists recommenders (
    id uuid primary key default gen_random_uuid(),
    case_id uuid not null references cases(id) on delete cascade,
    name text not null,
    title text,
    org text,
    relationship text default 'independent'
        check (relationship in ('independent','dependent')),
    angle text,
    email text,
    status text not null default 'planned'
        check (status in ('planned','drafted','signed')),
    created_at timestamptz not null default now()
);
create index if not exists recommenders_case_idx on recommenders(case_id);

create table if not exists documents (
    id uuid primary key default gen_random_uuid(),
    case_id uuid not null references cases(id) on delete cascade,
    doc_type text not null
        check (doc_type in ('pes','petition_letter','reco_letter','exhibit_list','cover_letter','rfe_response')),
    recommender_id uuid references recommenders(id) on delete set null,
    version int not null default 1,
    content_md text not null default '',
    status text not null default 'draft'
        check (status in ('draft','reviewed','final')),
    created_at timestamptz not null default now()
);
create index if not exists documents_case_idx on documents(case_id);

create table if not exists form_data (
    case_id uuid primary key references cases(id) on delete cascade,
    answers jsonb not null default '{}'::jsonb,
    updated_at timestamptz not null default now()
);

create table if not exists filled_forms (
    id uuid primary key default gen_random_uuid(),
    case_id uuid not null references cases(id) on delete cascade,
    form_code text not null,
    file_path text not null,
    created_at timestamptz not null default now()
);
create index if not exists filled_forms_case_idx on filled_forms(case_id);

create table if not exists jobs (
    id uuid primary key default gen_random_uuid(),
    case_id uuid references cases(id) on delete cascade,
    kind text not null,
    status text not null default 'queued'
        check (status in ('queued','running','done','error')),
    payload jsonb not null default '{}'::jsonb,
    result jsonb not null default '{}'::jsonb,
    error text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);
create index if not exists jobs_case_idx on jobs(case_id);

create table if not exists messages (
    id uuid primary key default gen_random_uuid(),
    case_id uuid not null references cases(id) on delete cascade,
    role text not null check (role in ('user','assistant','system')),
    content text not null,
    created_at timestamptz not null default now()
);
create index if not exists messages_case_idx on messages(case_id);

create table if not exists uploads (
    id uuid primary key default gen_random_uuid(),
    case_id uuid references cases(id) on delete cascade,
    kind text not null default 'other'
        check (kind in ('cv','linkedin','degree','publication','rfe','other')),
    filename text not null,
    file_path text not null,
    text_extract text,
    created_at timestamptz not null default now()
);
create index if not exists uploads_case_idx on uploads(case_id);
