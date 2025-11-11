CREATE OR REPLACE VIEW tv_one.sessions_view
 AS
 SELECT tracking.tracking_id AS session_tracking_id,
    tracking.session_id,
    tracking.tracking_time AS session_start_time,
    tracking.tracking_time::date AS session_start_date,
    tracking.platform,
    tracking.user_id
   FROM tv_one.tracking
  WHERE tracking.type = 'Session starts'::text