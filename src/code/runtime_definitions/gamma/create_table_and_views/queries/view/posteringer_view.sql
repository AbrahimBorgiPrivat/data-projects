CREATE OR REPLACE VIEW gamma_db.posteringer_view
 AS
 WITH member_payments AS (
         SELECT posteringer.user_id,
            posteringer.date AS payment_date
           FROM gamma_db.posteringer
          WHERE posteringer.account_number = 'K-3-12-1'::text
        )
 SELECT p1.id,
    p1.date,
    p1.text,
    p1.amount,
    p1.bank_account_key,
    p1.mp_key,
    p1.user_id,
    p1.account_number,
    p1.posting_group_id,
    p1.document,
    p1.belongs_to_last_year,
    p2.last_member_payment_date,
        CASE
            WHEN p1.account_number <> 'K-3-12-1'::text AND p2.last_member_payment_date IS NULL THEN 'NOT MEMBER'::text
            WHEN p1.account_number <> 'K-3-12-1'::text AND date_part('year'::text, p1.date) = date_part('year'::text, p2.last_member_payment_date) THEN 'MEMBER'::text
            WHEN p1.account_number = 'K-3-12-1'::text AND (date_part('year'::text, p1.date) - 1::double precision) <= date_part('year'::text, p2.last_member_payment_date) THEN 'RESIGNING'::text
            WHEN p1.account_number = 'K-3-12-1'::text AND ((date_part('year'::text, p1.date) - 1::double precision) > date_part('year'::text, p2.last_member_payment_date) OR p2.last_member_payment_date IS NULL) THEN 'NEW OR RELIVE'::text
            ELSE NULL::text
        END AS member_context
   FROM gamma_db.posteringer p1
     LEFT JOIN LATERAL ( SELECT mp.payment_date AS last_member_payment_date
           FROM member_payments mp
          WHERE mp.user_id = p1.user_id AND (p1.account_number = 'K-3-12-1'::text AND mp.payment_date < p1.date OR p1.account_number <> 'K-3-12-1'::text AND mp.payment_date <= p1.date)
          ORDER BY mp.payment_date DESC
         LIMIT 1) p2 ON true
  ORDER BY p1.user_id, p1.date DESC;