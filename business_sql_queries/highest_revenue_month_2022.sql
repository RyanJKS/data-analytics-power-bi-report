SELECT ROUND(CAST(SUM(dp.sale_price * o.product_quantity) AS NUMERIC),2) AS revenue,
        EXTRACT(MONTH FROM o.order_date::timestamp) AS month
FROM dim_product AS dp
JOIN orders AS o ON dp.product_code = o.product_code
WHERE  EXTRACT(YEAR FROM o.order_date::timestamp) = '2022'
GROUP BY month
ORDER BY revenue DESC;