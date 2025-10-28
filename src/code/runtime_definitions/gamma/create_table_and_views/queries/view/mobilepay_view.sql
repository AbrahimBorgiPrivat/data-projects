CREATE OR REPLACE VIEW gamma_db.mobilepay_view
 AS
 SELECT mobilepay.id,
    mobilepay.date,
    mobilepay.timestamp_iso,
    mobilepay.amount,
    mobilepay.message,
    mobilepay.transaction_type,
    mobilepay.transfer_date,
    mobilepay.payner_name
   FROM gamma_db.mobilepay;