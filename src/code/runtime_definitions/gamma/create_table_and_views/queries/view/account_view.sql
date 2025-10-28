CREATE OR REPLACE VIEW gamma_db.account_view
 AS
 SELECT account.id,
    account.main_account,
    account.account_key,
    account.sub_account,
    account.sub_account_key,
    account.context,
    account.context_key
   FROM gamma_db.account;