CREATE TABLE IF NOT EXISTS tv_one.tracking
(
    tracking_id bigint NOT NULL,
    tracking_time timestamp without time zone,
    type text COLLATE pg_catalog."default",
    session_id bigint,
    target_id bigint,
    platform text COLLATE pg_catalog."default",
    context jsonb,
    user_id bigint,
    CONSTRAINT tracking_pkey PRIMARY KEY (tracking_id)
)