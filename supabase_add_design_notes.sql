-- Adds narrative fields that power the design detail strategy sections
alter table public.designs
  add column if not exists strategy_notes text,
  add column if not exists psychology_notes text,
  add column if not exists usage_notes text,
  add column if not exists performance_notes text,
  add column if not exists accessibility_notes text;

comment on column public.designs.strategy_notes is 'Notes about the UX narrative, positioning, or go-to-market framing.';
comment on column public.designs.psychology_notes is 'Behavioral or psychological cues supported by the layout.';
comment on column public.designs.usage_notes is 'Interaction patterns, user flows, or product usage context.';
comment on column public.designs.performance_notes is 'Core Web Vitals and performance implementation notes.';
comment on column public.designs.accessibility_notes is 'Accessibility guidance, compliance reminders, and inclusive design fixes.';
