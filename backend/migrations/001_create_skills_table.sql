create table if not exists skills (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    category text,
    last_practiced_at timestamptz,
    stability float8 default 1.0,
    created_at timestamptz default now()
);