{{ config(
    materialized = 'view',
    tags = ['marts', 'programs']
) }}

SELECT
    *
FROM {{ ref('dim_programs') }}