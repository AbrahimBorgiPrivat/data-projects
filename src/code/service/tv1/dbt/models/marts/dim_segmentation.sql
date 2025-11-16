{{ config(
    materialized = 'view',
    tags = ['staging', 'segmentation']
) }}

SELECT segmentation.segment_id,
    segmentation.segment_key,
    segmentation.name,
    segmentation.description,
    segmentation.activity_level
FROM {{ source('tv_one', 'segmentation') }}