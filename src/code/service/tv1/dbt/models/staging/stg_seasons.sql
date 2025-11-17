{{ config(
    materialized = 'view',
    tags = ['staging', 'seasons']
) }}

SELECT
    *
FROM {{ source('tv_one', 'seasons') }}