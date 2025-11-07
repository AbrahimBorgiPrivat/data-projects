CREATE OR REPLACE VIEW cph_airport.flights_view
 AS
 SELECT transaction_id,
    flight_number,
    scheduled_utc,
    airline,
    airline_iata,
    airline_icao,
    destination,
    destination_iata,
    destination_icao,
    scheduled_local,
    scheduled_local::date AS scheduled_date,
    revised_utc,
    revised_local,
    EXTRACT(epoch FROM runway_local - scheduled_local) / 60::numeric AS dep_delay_minutes,
    runway_utc,
    runway_local,
    status,
        CASE
            WHEN status = ANY (ARRAY['Canceled'::text, 'CanceledUncertain'::text, 'Unknown'::text]) THEN 'Aflyst'::text
            WHEN status = 'Boarding'::text THEN 'Boarding'::text
            WHEN status = 'Delayed'::text THEN 'Forsinket'::text
            WHEN status = 'Departed'::text THEN 'Afgået'::text
            WHEN status = 'Expected'::text THEN 'Forventet'::text
            ELSE 'Aflyst'::text
        END AS status_da,
    terminal,
    gate,
    aircraft_model,
    aircraft_reg
   FROM cph_airport.flights;