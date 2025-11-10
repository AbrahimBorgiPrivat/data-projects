CREATE OR REPLACE VIEW default_data.date_view
 AS
 SELECT date_dim_id,
    date_actual,
    day_name,
    day_of_week,
    day_of_month,
    day_of_quarter,
    day_of_year,
    week_of_month,
    week_of_year,
        CASE
            WHEN week_of_year <> 1 AND month_actual = 1 AND week_of_month = 1 THEN 0
            WHEN week_of_year = 1 AND month_actual = 12 THEN 53
            ELSE week_of_year
        END AS week_of_year_conv,
    "substring"(week_of_year_iso::text, 1, 8) AS week_year,
    month_actual,
    month_name,
    quarter_actual,
    quarter_name,
    concat('Q', quarter_actual) AS quarter,
    year_actual,
    first_day_of_week,
    last_day_of_week,
    first_day_of_month,
    last_day_of_month,
    first_day_of_quarter,
    last_day_of_quarter,
    first_day_of_year,
    last_day_of_year,
    mmyyyy,
        CASE
            WHEN month_actual < 10 THEN concat(year_actual, '0', month_actual)::bigint
            ELSE concat(year_actual, month_actual)::bigint
        END AS yyyymm,
    mmddyyyy,
    weekend_indr,
        CASE
            WHEN date_actual = CURRENT_DATE THEN 1
            ELSE 0
        END AS is_today,
        CASE
            WHEN date_actual = (CURRENT_DATE - 1) THEN 1
            ELSE 0
        END AS is_yesterday,
        CASE
            WHEN date_part('week'::text, date_actual) = date_part('week'::text, CURRENT_DATE) AND date_part('year'::text, date_actual) = date_part('year'::text, CURRENT_DATE) THEN 1
            ELSE 0
        END AS is_this_week,
        CASE
            WHEN date_part('week'::text, date_actual) = date_part('week'::text, CURRENT_DATE) AND date_part('year'::text, date_actual) = date_part('year'::text, CURRENT_DATE) THEN 'this week'::text
            WHEN date_part('week'::text, date_actual) = date_part('week'::text, CURRENT_DATE - '7 days'::interval) AND date_part('year'::text, date_actual) = date_part('year'::text, CURRENT_DATE - '7 days'::interval) THEN 'last week'::text
            ELSE ''::text
        END AS last_or_thisweek,
        CASE
            WHEN date_part('month'::text, date_actual) = date_part('month'::text, CURRENT_DATE) AND date_part('year'::text, date_actual) = date_part('year'::text, CURRENT_DATE) THEN 1
            ELSE 0
        END AS is_this_month,
        CASE
            WHEN date_actual >= date_trunc('month'::text, CURRENT_DATE - '1 mon'::interval month) AND date_actual < date_trunc('month'::text, CURRENT_DATE::timestamp with time zone) THEN 1
            ELSE 0
        END AS is_last_month,
        CASE
            WHEN date_actual >= date_trunc('month'::text, CURRENT_DATE - '1 mon'::interval month) AND date_actual < date_trunc('month'::text, CURRENT_DATE::timestamp with time zone) THEN 'last month'::text
            WHEN date_part('month'::text, date_actual) = date_part('month'::text, CURRENT_DATE) AND date_part('year'::text, date_actual) = date_part('year'::text, CURRENT_DATE) THEN 'this month'::text
            ELSE ''::text
        END AS last_or_thismonth,
        CASE
            WHEN date_part('quarter'::text, date_actual) = date_part('quarter'::text, CURRENT_DATE) AND date_part('year'::text, date_actual) = date_part('year'::text, CURRENT_DATE) THEN 1
            ELSE 0
        END AS is_this_quarter,
        CASE
            WHEN year_actual::double precision = date_part('year'::text, CURRENT_DATE) THEN 1
            ELSE 0
        END AS is_this_year,
        CASE
            WHEN year_actual::double precision >= (date_part('year'::text, CURRENT_DATE) - 1::double precision) AND year_actual::double precision <= date_part('year'::text, CURRENT_DATE) THEN 1
            ELSE 0
        END AS is_last_two_year,
        CASE
            WHEN date_actual <= CURRENT_DATE THEN 1
            ELSE 0
        END AS is_past,
        CASE
            WHEN date_actual < date_trunc('month'::text, CURRENT_DATE + '1 mon'::interval month) THEN 1
            ELSE 0
        END AS is_before_next_month
   FROM default_data.d_date
  WHERE date_part('year'::text, date_actual) >= 2024::double precision AND date_part('year'::text, date_actual) <= (date_part('year'::text, CURRENT_DATE) + 1::double precision);
