CREATE OR REPLACE VIEW tv_one.sessions_view AS
SELECT
    tracking_id      AS session_tracking_id,
    session_id,
    tracking_time    AS session_start_time,
    platform,
    user_id
FROM tv_one.tracking
WHERE type = 'Session starts';