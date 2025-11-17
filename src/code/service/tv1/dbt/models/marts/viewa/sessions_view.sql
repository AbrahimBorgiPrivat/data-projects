{{ config(
    materialized = 'view',
    tags = ['marts', 'segmentation']
) }}

SELECT
    *,
    {{ session_duration_group('session_duration_min') }} AS session_duration_group,
    {{ session_duration_group_order('session_duration_min') }} AS session_duration_group_order
FROM {{ ref('fct_sessions') }}