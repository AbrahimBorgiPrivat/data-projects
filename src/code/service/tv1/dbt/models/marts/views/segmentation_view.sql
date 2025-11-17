{{ config(
    materialized = 'view',
    tags = ['marts', 'segmentation']
) }}

SELECT
    *
FROM {{ ref('dim_segmentation') }}