CREATE TABLE IF NOT EXISTS tv_one.segmentation
(
    segment_id bigint NOT NULL,
    segment_key text COLLATE pg_catalog."default",
    name text COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    activity_level text COLLATE pg_catalog."default",
    child_focus boolean,
    preferred_platform_weights jsonb,
    weekday_time_windows jsonb,
    weekend_time_windows jsonb,
    avg_daily_minutes_weekday jsonb,
    avg_daily_minutes_weekend jsonb,
    avg_session_minutes jsonb,
    kids_content_share double precision,
    CONSTRAINT segmentation_pkey PRIMARY KEY (segment_id)
)