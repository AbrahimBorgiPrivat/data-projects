{{ config(
    materialized = 'view',
    tags = ['marts', 'users']
) }}

SELECT
    *
FROM {{ ref('dim_users') }}