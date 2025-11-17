{{ config(
    materialized = 'incremental',
    unique_key   = 'season_id',
    incremental_strategy = 'merge',
    tags = ['marts', 'programs'],
    post_hook = [
        "CREATE INDEX IF NOT EXISTS idx_dim_season_season_id ON {{ this }} (season_id)",
        "CREATE INDEX IF NOT EXISTS idx_dim_season_program_id ON {{ this }} (program_id)"
    ]
) }}

SELECT season_id,
    program_id,
    season,
    url
FROM {{ ref('stg_seasons')}}