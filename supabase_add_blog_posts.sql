-- Blog posts table for /blog
create table if not exists posts (
  id uuid primary key default uuid_generate_v4(),
  slug text unique not null,
  title text not null,
  excerpt text,
  content text not null,
  category text,
  author text,
  author_role text,
  author_avatar_url text,
  cover_image_url text,
  tags text[],
  published_at timestamptz,
  status text not null default 'draft',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Basic status constraint
do $$
begin
  if not exists (
    select 1
    from pg_constraint
    where conname = 'posts_status_check'
  ) then
    alter table posts
      add constraint posts_status_check
      check (status in ('draft', 'published'));
  end if;
end $$;

-- Enable Row Level Security
alter table posts enable row level security;

-- Public read policy for published posts
drop policy if exists "Public can read published posts" on posts;
create policy "Public can read published posts"
  on posts
  for select
  using (status = 'published');

-- Optional: update updated_at on change
create or replace function set_posts_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

drop trigger if exists set_posts_updated_at on posts;
create trigger set_posts_updated_at
before update on posts
for each row
execute function set_posts_updated_at();

alter table posts add column if not exists author_role text;
alter table posts add column if not exists author_avatar_url text;
alter table posts add column if not exists cover_image_url text;
alter table posts add column if not exists tags text[];
