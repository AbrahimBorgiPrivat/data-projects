CREATE TABLE IF NOT EXISTS tv_one.users
(
    user_id bigint NOT NULL,
    age_group text COLLATE pg_catalog."default",
    household_size integer,
    region text COLLATE pg_catalog."default",
    children_under5 boolean,
    segment_id bigint,
    CONSTRAINT users_pkey PRIMARY KEY (user_id)
)