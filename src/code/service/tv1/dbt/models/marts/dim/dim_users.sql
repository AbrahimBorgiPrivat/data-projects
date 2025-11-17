{{ config(
    materialized = 'incremental',
    unique_key   = 'user_id',
    incremental_strategy = 'merge',
    tags = ['marts', 'users'],
    post_hook = [
        "CREATE INDEX IF NOT EXISTS idx_dim_users_user_id ON {{ this }} (user_id)"
    ]
) }}

SELECT
    user_id,
    age_group,
    region,
    segment_id
FROM {{ref('stg_users')}}