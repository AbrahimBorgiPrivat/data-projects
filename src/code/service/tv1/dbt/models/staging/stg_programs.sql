{{ config(
    materialized = 'view',
    tags = ['staging', 'programs']
) }}

SELECT
    *
FROM {{ source('tv_one', 'programs') }}