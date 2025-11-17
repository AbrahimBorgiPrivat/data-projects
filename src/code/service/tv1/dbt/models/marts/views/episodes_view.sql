{{ config(
    materialized = 'view',
    tags = ['marts', 'episodes']
) }}

SELECT
    *
FROM {{ ref('dim_episodes') }}