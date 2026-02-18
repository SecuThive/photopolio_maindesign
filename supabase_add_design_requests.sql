create extension if not exists pgcrypto;

create table if not exists design_requests (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  description text not null,
  category text,
  target_audience text,
  reference_notes text,
  requester_email text,
  vote_count integer not null default 0,
  status text not null default 'pending' check (status in ('pending', 'in_progress', 'completed', 'rejected')),
  linked_design_id uuid references designs(id) on delete set null,
  ip_address text,
  user_agent text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table design_requests
  add column if not exists vote_count integer not null default 0;

create table if not exists design_request_votes (
  id uuid primary key default gen_random_uuid(),
  request_id uuid not null references design_requests(id) on delete cascade,
  token text not null,
  created_at timestamptz not null default now()
);

create unique index if not exists uq_design_request_votes_request_token
  on design_request_votes (request_id, token);

create index if not exists idx_design_requests_status_created_at
  on design_requests (status, created_at desc);

create index if not exists idx_design_requests_created_at
  on design_requests (created_at desc);

create or replace function update_design_requests_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

drop trigger if exists trg_design_requests_updated_at on design_requests;
create trigger trg_design_requests_updated_at
before update on design_requests
for each row
execute function update_design_requests_updated_at();
