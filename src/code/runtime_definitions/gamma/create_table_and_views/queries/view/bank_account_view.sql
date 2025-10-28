CREATE OR REPLACE VIEW gamma_db.bank_account_view
 AS
 SELECT bank_account.id,
    bank_account.date,
    bank_account.text,
    bank_account.amount,
    bank_account.balance,
    bank_account.balance - bank_account.amount AS balance_before,
    bank_account.status,
    bank_account.reconciled
   FROM gamma_db.bank_account
  ORDER BY bank_account.date;