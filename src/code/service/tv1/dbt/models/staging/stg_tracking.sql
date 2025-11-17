{{ config(
    materialized = 'view',
    tags = ['staging', 'tracking']
) }}

SELECT
    *
FROM {{ source('tv_one', 'tracking') }}