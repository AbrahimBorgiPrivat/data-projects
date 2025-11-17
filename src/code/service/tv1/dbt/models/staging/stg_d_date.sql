{{ config(
    materialized = 'view',
    tags = ['staging', 'd_date']
) }}

SELECT
    *
FROM {{ source('default_data', 'd_date') }}