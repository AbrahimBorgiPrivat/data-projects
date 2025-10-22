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
        WHEN mp.id IS NULL THEN CONCAT('BANK:',bac.text) 
        ELSE CONCAT('MP TRANS: ', mp.transaction_type,'/',mp.message,'/',mp.payner_name) 
    END AS text, 
    CASE 
        WHEN mp.id IS NULL THEN bac.amount 
        ELSE mp.amount 
    END AS amount,
    bac.id AS bank_account_key,
    mp.id AS mp_key,
	CASE 
        WHEN us.id IS NULL THEN ''
        ELSE us.id
    END AS user_id,
    '' AS account_number,
    '' AS posting_group_id,
    '' AS document
FROM gamma_db.bank_account bac
LEFT JOIN gamma_db.mobilepay mp ON mp.transfer_ref = bac.text 
LEFT JOIN gamma_db.users us ON us.name = mp.payner_name
ORDER BY bac.date ASC;