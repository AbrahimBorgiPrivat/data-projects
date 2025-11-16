{{ config(
    materialized = 'view',
    tags = ['staging', 'segmentation']
) }}

SELECT *
FROM {{ source('tv_one', 'segmentation') }}