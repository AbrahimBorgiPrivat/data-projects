SELECT 
    CASE 
        WHEN mp.id IS NULL THEN bac.id 
        ELSE mp.id 
    END AS id,    
    CASE 
        WHEN mp.id IS NULL THEN bac.date 
        ELSE mp.date 
    END AS date,
    CASE 
        WHEN mp.id IS NULL THEN bac.text 
        ELSE CONCAT(mp.transaction_type,'-',mp.message,'-',mp.merchant_name) 
    END AS text, 
    CASE 
        WHEN mp.id IS NULL THEN bac.amount 
        ELSE mp.amount 
    END AS amount,
    bac.id AS bank_account_key,
    mp.id AS mp_key,
    '' AS user_id,
    '' AS account_number
FROM gamma_db.bank_account bac
LEFT JOIN gamma_db.mobilepay mp ON mp.transfer_ref = bac.text ORDER BY bac.date DESC;