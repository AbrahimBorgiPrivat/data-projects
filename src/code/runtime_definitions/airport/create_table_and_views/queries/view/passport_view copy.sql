CREATE OR REPLACE VIEW cph_airport.ticket_view
 AS
 SELECT ti.unique_id,
    ti.transaction_id,
    ti.seat_number,
    ti.passport_number,
    ti.check_in_type,
    ti.checkin_time,
    ti.passed_security_time,
    fl.scheduled_local,
        CASE
            WHEN ti.checkin_time IS NOT NULL THEN fl.scheduled_local - ti.checkin_time
            ELSE NULL::interval
        END AS check_in_time_bef_sched,
        CASE
            WHEN ti.passed_security_time IS NOT NULL THEN fl.scheduled_local - ti.passed_security_time
            ELSE NULL::interval
        END AS sek_time_bef_sched
   FROM cph_airport.tickets ti
     JOIN cph_airport.flights fl ON fl.transaction_id = ti.transaction_id;