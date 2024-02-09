SELECT SUM((dp.sale_price - dp.cost_price) * o.product_quantity) AS profit,
       dp.category AS product_category
FROM dim_product AS dp
JOIN orders AS o ON dp.product_code = o.product_code
JOIN dim_store AS ds ON ds.store_code = o.store_code
WHERE ds.full_region = 'Wiltshire, UK' AND EXTRACT(YEAR FROM o.order_date::timestamp) = '2021'
GROUP BY dp.category
ORDER BY profit DESC