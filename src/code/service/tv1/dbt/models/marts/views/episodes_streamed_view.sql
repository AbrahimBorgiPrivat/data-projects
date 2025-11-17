{{ config(
    materialized = 'view',
    tags = ['marts', 'episodes_streamed']
) }}

SELECT
    *
FROM {{ ref('fct_episodes_streamed') }}