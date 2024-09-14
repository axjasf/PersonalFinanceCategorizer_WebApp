-- View: Order Details
CREATE VIEW vw_order_details AS
SELECT
    o.order_id,
    o.order_date,
    o.total_amount,
    oi.item_description,
    oi.item_price,
    oi.quantity,
    c.name AS category_name,
    p.name AS payee_name
FROM
    orders o
JOIN
    order_items oi ON o.id = oi.order_id
LEFT JOIN
    categories c ON oi.category_id = c.id
LEFT JOIN
    payees p ON o.payee_id = p.id;
