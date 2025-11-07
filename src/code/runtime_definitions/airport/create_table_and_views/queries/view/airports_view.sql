CREATE OR REPLACE VIEW cph_airport.airports_view
 AS
 SELECT icao AS iata,
    name,
    city,
    country,
    country_code,
    latitude,
    longitude,
    world_area_code,
    city_name_geo_name_id,
    country_name_geo_name_id
   FROM cph_airport.airports;