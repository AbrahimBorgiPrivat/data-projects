{{ config(
    materialized = 'view',
    tags = ['staging', 'users']
) }}

SELECT
    *
FROM {{ source('tv_one', 'users') }}