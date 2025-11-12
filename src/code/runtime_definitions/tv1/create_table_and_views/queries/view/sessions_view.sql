CREATE OR REPLACE VIEW tv_one.sessions_view
 AS
 WITH episode_summary AS (
         SELECT tracking.session_id,
            max((tracking.context ->> 'end_time'::text)::timestamp without time zone) AS last_end_time,
            count(*) AS episodes_in_session
           FROM tv_one.tracking
          WHERE tracking.type = 'Episode starts'::text
          GROUP BY tracking.session_id
        ), base AS (
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
        )
 SELECT base.session_tracking_id,
    base.session_id,
    base.session_start_time,
    base.session_start_date,
    base.platform,
    base.user_id,
    base.last_end_time,
    base.session_duration_min,
    base.episodes_in_session,
        CASE
            WHEN base.session_duration_min = 0::numeric THEN '0 min'::text
            WHEN base.session_duration_min <= 1::numeric THEN '0–1 min'::text
            WHEN base.session_duration_min <= 2::numeric THEN '1–2 min'::text
            WHEN base.session_duration_min <= 3::numeric THEN '2–3 min'::text
            WHEN base.session_duration_min <= 5::numeric THEN '3–5 min'::text
            WHEN base.session_duration_min <= 10::numeric THEN '5–10 min'::text
            WHEN base.session_duration_min <= 15::numeric THEN '10–15 min'::text
            WHEN base.session_duration_min <= 20::numeric THEN '15–20 min'::text
            WHEN base.session_duration_min <= 30::numeric THEN '20–30 min'::text
            WHEN base.session_duration_min <= 40::numeric THEN '30–40 min'::text
            WHEN base.session_duration_min <= 50::numeric THEN '40–50 min'::text
            WHEN base.session_duration_min <= 60::numeric THEN '50–60 min'::text
            WHEN base.session_duration_min <= 75::numeric THEN '60–75 min'::text
            WHEN base.session_duration_min <= 90::numeric THEN '75–90 min'::text
            WHEN base.session_duration_min <= 120::numeric THEN '90–120 min'::text
            WHEN base.session_duration_min <= 150::numeric THEN '120–150 min'::text
            WHEN base.session_duration_min <= 180::numeric THEN '150–180 min'::text
            WHEN base.session_duration_min <= 210::numeric THEN '180–210 min'::text
            WHEN base.session_duration_min <= 240::numeric THEN '210–240 min'::text
            ELSE '240+ min'::text
        END AS session_duration_group,
        CASE
            WHEN base.session_duration_min = 0::numeric THEN 0
            WHEN base.session_duration_min <= 1::numeric THEN 1
            WHEN base.session_duration_min <= 2::numeric THEN 2
            WHEN base.session_duration_min <= 3::numeric THEN 3
            WHEN base.session_duration_min <= 5::numeric THEN 4
            WHEN base.session_duration_min <= 10::numeric THEN 5
            WHEN base.session_duration_min <= 15::numeric THEN 6
            WHEN base.session_duration_min <= 20::numeric THEN 7
            WHEN base.session_duration_min <= 30::numeric THEN 8
            WHEN base.session_duration_min <= 40::numeric THEN 9
            WHEN base.session_duration_min <= 50::numeric THEN 10
            WHEN base.session_duration_min <= 60::numeric THEN 11
            WHEN base.session_duration_min <= 75::numeric THEN 12
            WHEN base.session_duration_min <= 90::numeric THEN 13
            WHEN base.session_duration_min <= 120::numeric THEN 14
            WHEN base.session_duration_min <= 150::numeric THEN 15
            WHEN base.session_duration_min <= 180::numeric THEN 16
            WHEN base.session_duration_min <= 210::numeric THEN 17
            WHEN base.session_duration_min <= 240::numeric THEN 18
            ELSE 19
        END AS session_duration_group_order
   FROM base;