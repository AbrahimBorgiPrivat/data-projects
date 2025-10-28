CREATE OR REPLACE VIEW gamma_db.users_view
 AS
 SELECT users.id,
    users.name,
        CASE
            WHEN users.status = 0 THEN 'OPRETTET'::text
            WHEN users.status = 1 THEN 'MEDLEM'::text
            WHEN users.status = 2 THEN 'SKYLDER'::text
            ELSE 'DNO'::text
        END AS status,
    users.aargang,
    users.occopation,
    users.last_payment,
    users.created
   FROM gamma_db.users
  ORDER BY users.name;