{{ config(
    materialized = 'incremental',
    unique_key   = 'session_tracking_id',
    incremental_strategy = 'merge',
    tags = ['marts', 'sessions'],
    post_hook = [
        "CREATE INDEX IF NOT EXISTS idx_fct_sessions_session_tracking_id ON {{ this }} (session_tracking_id)",
        "CREATE INDEX IF NOT EXISTS idx_fct_sessions_user_id ON {{ this }} (user_id)",
        "CREATE INDEX IF NOT EXISTS idx_fct_sessions_platform ON {{ this }} (platform)",
        "CREATE INDEX IF NOT EXISTS idx_fct_sessions_start_time ON {{ this }} (session_start_time)"
    ]
) }}

WITH episode_summary AS (
    SELECT
        session_id,
        MAX((context ->> 'end_time')::timestamp)      AS last_end_time,
        COUNT(*)                                      AS episodes_in_session
    FROM {{ source('tv_one','tracking') }}
    WHERE type = 'Episode starts'
    GROUP BY session_id
),
base AS (
    SELECT
        s.tracking_id                                  AS session_tracking_id,
        s.session_id,
        s.tracking_time                                AS session_start_time,
        s.tracking_time::date                          AS session_start_date,
        s.platform,
        s.user_id,
        COALESCE(e.last_end_time, s.tracking_time)     AS last_end_time,
        COALESCE(
            ROUND(
                EXTRACT(EPOCH FROM (e.last_end_time - s.tracking_time)) / 60.0,
                2
            ),
        0)                                             AS session_duration_min,

        COALESCE(e.episodes_in_session, 0)             AS episodes_in_session
    FROM {{ source('tv_one','tracking') }} s
    LEFT JOIN episode_summary e
        ON s.session_id = e.session_id
    WHERE s.type = 'Session starts'
)
SELECT
    *
FROM base