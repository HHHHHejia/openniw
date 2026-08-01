-- v0.2: citation pipeline, canonical facts, evidence intake, endeavor object
set search_path to openniw;

-- One row per citing paper discovered for this case.
create table if not exists citing_papers (
    id uuid primary key default gen_random_uuid(),
    case_id uuid not null references cases(id) on delete cascade,
    cited_title text not null,
    cited_openalex_id text,
    citing_openalex_id text,
    citing_title text not null,
    citing_authors jsonb not null default '[]'::jsonb,
    citing_institutions jsonb not null default '[]'::jsonb,
    citing_venue text,
    citing_venue_type text,
    citing_year int,
    doi text,
    oa_pdf_url text,
    published boolean,
    independent boolean,
    same_surname_flag boolean not null default false,
    verified_in_text boolean,
    quote_context text,
    use_type text,
    score int,
    negative boolean,
    status text not null default 'harvested'
        check (status in ('harvested','verified','scored','selected','rejected')),
    reject_reason text,
    pdf_path text,
    created_at timestamptz not null default now(),
    unique (case_id, citing_openalex_id, cited_openalex_id)
);
create index if not exists citing_papers_case_idx on citing_papers(case_id);

-- Canonical fact table: the single source of truth every artifact must match.
create table if not exists case_facts (
    id uuid primary key default gen_random_uuid(),
    case_id uuid not null references cases(id) on delete cascade,
    category text not null,
    key text not null,
    value text not null,
    as_of date,
    source text,
    created_at timestamptz not null default now()
);
create index if not exists case_facts_case_idx on case_facts(case_id);

-- Evidence intake extensions
alter table evidence_items add column if not exists extracted jsonb;
alter table evidence_items add column if not exists date_class text
    check (date_class in ('pre_filing','post_filing','unknown'));

-- Endeavor object + filing date on the case
alter table cases add column if not exists endeavor jsonb not null default '{}'::jsonb;
alter table cases add column if not exists filed_date date;

-- New generated-document type for the citation-examples control file
alter table documents drop constraint if exists documents_doc_type_check;
alter table documents add constraint documents_doc_type_check
    check (doc_type in ('pes','petition_letter','reco_letter','exhibit_list',
                        'cover_letter','rfe_response','citation_examples'));
