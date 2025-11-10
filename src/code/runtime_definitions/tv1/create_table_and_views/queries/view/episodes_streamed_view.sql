CREATE OR REPLACE VIEW tv_one.episodes_streamed_view AS
SELECT
    tracking_id,
    session_id,
    user_id,
    tracking_time      AS event_time,
    target_id          AS episode_id,
    platform,
    (context->>'start_time')::timestamp AS episode_start_time,
    (context->>'end_time')::timestamp   AS episode_end_time,
    (context->>'finished')::boolean     AS finished,
    ((EXTRACT(EPOCH FROM ((context->>'end_time')::timestamp - (context->>'start_time')::timestamp)) / 60)::NUMERIC(6,2)) AS watched_minutes
FROM tv_one.tracking
WHERE type = 'Episode starts';