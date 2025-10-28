CREATE OR REPLACE VIEW gamma_db.forecast_view
 AS
 SELECT forecast.id,
    forecast.account_id,
    forecast.postering_group_id,
    forecast.year_actual,
    forecast.forecast,
    forecast.forecast_type
   FROM gamma_db.forecast;