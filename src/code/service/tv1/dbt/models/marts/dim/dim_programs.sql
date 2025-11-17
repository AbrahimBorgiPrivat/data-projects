{{ config(
    materialized = 'incremental',
    unique_key   = 'program_id',
    incremental_strategy = 'merge',
    tags = ['marts', 'programs'],
    post_hook = [
        "CREATE INDEX IF NOT EXISTS idx_dim_programs_program_id ON {{ this }} (program_id)"
    ]
) }}

SELECT
    program_id,
    title,
    category,
    seasons,
    url,
    image
FROM {{ ref('stg_programs') }}
