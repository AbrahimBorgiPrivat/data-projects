{{ config(materialized='view', 
          tags=['marts', 'users']) }}

SELECT
    user_id,
    age_group,
    region,
    segment_id
FROM {{ source('tv_one', 'users')}}