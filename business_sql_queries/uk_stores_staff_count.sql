SELECT  ds.store_type,
        COUNT(o.order_date) AS total_orders,
        CAST(SUM(dp.sale_price * o.product_quantity) AS NUMERIC(10,2)) AS total_sales,
        CAST((SUM(dp.sale_price * o.product_quantity) / SUM(SUM(dp.sale_price * o.product_quantity)) OVER ()) * 100 AS NUMERIC(10,2)) AS sales_percentage
FROM orders AS o
JOIN dim_store AS ds ON ds.store_code = o.store_code
JOIN dim_product AS dp ON dp.product_code = o.product_code
GROUP BY ds.store_type;