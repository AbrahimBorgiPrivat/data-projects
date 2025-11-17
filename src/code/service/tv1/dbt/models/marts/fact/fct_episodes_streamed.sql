{{ config(
    materialized = 'incremental',
    unique_key   = 'tracking_id',
    incremental_strategy = 'merge',
    tags = ['marts', 'episodes'],
    post_hook = [
        "CREATE INDEX IF NOT EXISTS idx_fct_episodes_streamed_event_time ON {{ this }} (event_time);",
        "CREATE INDEX IF NOT EXISTS idx_fct_episodes_streamed_tracking_id ON {{ this }} (tracking_id);"
    ]
) }}

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
    (
        EXTRACT(
            EPOCH FROM (
                (context->>'end_time')::timestamp 
                - (context->>'start_time')::timestamp
            )
        ) / 60.0
    )::numeric(6,2) AS watched_minutes
FROM {{ source('tv_one', 'tracking') }}
WHERE type = 'Episode starts'
