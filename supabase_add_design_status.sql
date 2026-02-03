-- Adds a status column that lets us archive designs while keeping their slugs for redirects.
alter table public.designs
  add column if not exists status text;

update public.designs
  set status = 'published'
  where status is null;

alter table public.designs
  alter column status set default 'published';

alter table public.designs
  alter column status set not null;

alter table public.designs
  drop constraint if exists designs_status_allowed;

alter table public.designs
  add constraint designs_status_allowed
  check (status in ('published', 'archived'));
