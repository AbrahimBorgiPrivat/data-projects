{{ config(
    materialized = 'incremental',
    unique_key   = 'segment_id',
    incremental_strategy = 'merge',
    tags = ['marts', 'segmentation'],
    post_hook = [
        "CREATE INDEX IF NOT EXISTS idx_dim_segmentation_segment_id ON {{ this }} (segment_id)"
    ]
) }}

SELECT segment_id,
    segment_key,
    name,
    description,
    activity_level
FROM {{ ref('stg_segmentation') }}