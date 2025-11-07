CREATE OR REPLACE VIEW cph_airport.aircraft_models_view
 AS
 SELECT aircraft_model,
    manufacturer,
    country,
    seats,
    range_km,
    engine_type,
    icao_code,
    iata_code,
        CASE
            WHEN seats = 0 THEN '0'::text
            WHEN seats >= 1 AND seats <= 50 THEN '50≤'::text
            WHEN seats >= 51 AND seats <= 100 THEN '51–100'::text
            WHEN seats >= 101 AND seats <= 150 THEN '101–150'::text
            WHEN seats >= 151 AND seats <= 200 THEN '151–200'::text
            WHEN seats >= 201 AND seats <= 300 THEN '201–300'::text
            WHEN seats >= 301 AND seats <= 400 THEN '301–400'::text
            WHEN seats > 400 THEN '400<'::text
            ELSE 'Unknown'::text
        END AS seat_interval,
        CASE
            WHEN seats = 0 THEN 1
            WHEN seats >= 1 AND seats <= 50 THEN 2
            WHEN seats >= 51 AND seats <= 100 THEN 3
            WHEN seats >= 101 AND seats <= 150 THEN 4
            WHEN seats >= 151 AND seats <= 200 THEN 5
            WHEN seats >= 201 AND seats <= 300 THEN 6
            WHEN seats >= 301 AND seats <= 400 THEN 7
            WHEN seats > 400 THEN 8
            ELSE 9
        END AS seat_index
   FROM cph_airport.aircraft_models;