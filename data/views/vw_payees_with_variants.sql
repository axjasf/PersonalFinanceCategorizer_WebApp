CREATE VIEW vw_payees_with_variants AS
SELECT 
    pv.id AS variant_id,
    p.name AS standard_payee_name,
    pv.payee_variant AS variant_payee_name
FROM 
    payee_variants pv
JOIN 
    payees p ON pv.payee_standard_id = p.id;
