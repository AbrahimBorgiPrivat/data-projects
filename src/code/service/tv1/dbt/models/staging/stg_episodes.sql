{{ config(
    materialized = 'view',
    tags = ['staging', 'episodes']
) }}

SELECT
    *
FROM {{ source('tv_one', 'episodes') }}