{{ config(
    materialized = 'view',
    tags = ['marts', 'seasons']
) }}

SELECT
    *
FROM {{ ref('dim_seasons') }}