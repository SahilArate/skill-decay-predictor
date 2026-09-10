alter table skills
add column user_id uuid references auth.users(id) on delete cascade;

alter table practice_events
add column user_id uuid references auth.users(id) on delete cascade;