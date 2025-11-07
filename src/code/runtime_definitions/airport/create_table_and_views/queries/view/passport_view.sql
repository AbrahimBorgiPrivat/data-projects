CREATE OR REPLACE VIEW cph_airport.passport_view
 AS
 SELECT passport_number,
    name,
    country
   FROM cph_airport.passports;
