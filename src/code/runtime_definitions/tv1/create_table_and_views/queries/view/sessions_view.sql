CREATE OR REPLACE VIEW tv_one.sessions_view
 AS
 WITH episode_summary AS (
         SELECT tracking.session_id,
            max((tracking.context ->> 'end_time'::text)::timestamp without time zone) AS last_end_time,
            count(*) AS episodes_in_session
           FROM tv_one.tracking
          WHERE tracking.type = 'Episode starts'::text
          GROUP BY tracking.session_id
        )
 SELECT s.tracking_id AS session_tracking_id,
    s.session_id,
    s.tracking_time AS session_start_time,
    s.tracking_time::date AS session_start_date,
    s.platform,
    s.user_id,
    COALESCE(e.last_end_time, s.tracking_time) AS last_end_time,
    COALESCE(round(EXTRACT(epoch FROM e.last_end_time - s.tracking_time) / 60.0, 2), 0::numeric) AS session_duration_min,
    COALESCE(e.episodes_in_session, 0::bigint) AS episodes_in_session
   FROM tv_one.tracking s
     LEFT JOIN episode_summary e ON s.session_id = e.session_id
  WHERE s.type = 'Session starts'::text