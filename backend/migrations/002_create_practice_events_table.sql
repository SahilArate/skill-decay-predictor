create table if not exists practice_events (
    id uuid primary key default gen_random_uuid(),
    skill_id uuid not null references skills(id) on delete cascade,
    source text not null,
    practiced_at timestamptz not null,
    intensity float8 default 1.0,
    raw_reference text,
    created_at timestamptz default now()
);