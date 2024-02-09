SELECT ROUND(CAST(SUM(dp.sale_price * o.product_quantity) AS NUMERIC),2) AS revenue,
        ds.store_type
FROM orders AS o
JOIN dim_product AS dp ON dp.product_code = o.product_code
JOIN dim_store AS ds ON ds.store_code = o.store_code
WHERE ds.country_code = 'DE'
GROUP BY store_type
ORDER BY revenue DESC;