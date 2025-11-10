CREATE OR REPLACE VIEW cph_airport.flights_view
 AS
 SELECT flights.transaction_id,
    flights.flight_number,
    flights.scheduled_utc,
    flights.airline,
    flights.airline_iata,
    flights.airline_icao,
    flights.destination,
    flights.destination_iata,
    flights.destination_icao,
    flights.scheduled_local,
    flights.scheduled_local::date AS scheduled_date,
    flights.revised_utc,
    flights.revised_local,
    EXTRACT(epoch FROM flights.runway_local - flights.scheduled_local) / 60::numeric AS dep_delay_minutes,
    flights.runway_utc,
    flights.runway_local,
    flights.status,
        CASE
            WHEN flights.status = ANY (ARRAY['Canceled'::text, 'CanceledUncertain'::text, 'Unknown'::text]) THEN 'Aflyst'::text
            WHEN flights.status = 'Boarding'::text THEN 'Boarding'::text
            WHEN flights.status = 'Delayed'::text THEN 'Forsinket'::text
            WHEN flights.status = 'Departed'::text THEN 'Afgået'::text
            WHEN flights.status = 'Expected'::text THEN 'Forventet'::text
            ELSE 'Aflyst'::text
        END AS status_da,
    flights.terminal,
    flights.gate,
    flights.aircraft_model,
    flights.aircraft_reg,
        CASE
            WHEN amod.seats IS NULL THEN 180::bigint
            ELSE amod.seats
        END AS seats
   FROM cph_airport.flights
     LEFT JOIN cph_airport.aircraft_models_view amod ON amod.aircraft_model = flights.aircraft_model;