-- Part 16: SQL Business Queries & Quality Checks

-- 1. How many total orders are available?
SELECT COUNT(*) AS total_orders 
FROM final_sales;

-- 2. What is the total net sales amount?
SELECT ROUND(SUM(net_amount), 2) AS total_net_sales 
FROM final_sales;

-- 3. Which five products generated the highest sales?
SELECT 
    product_name, 
    ROUND(SUM(net_amount), 2) AS total_sales
FROM final_sales
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 5;

-- 4. Which five cities generated the highest sales?
SELECT 
    city,
    ROUND(SUM(net_amount), 2) AS total_sales
FROM final_sales
GROUP BY city
ORDER BY total_sales DESC
LIMIT 5;

-- 5. How many orders have missing customer information?
SELECT COUNT(*) AS missing_customer_orders 
FROM final_sales 
WHERE customer_id IS NULL OR customer_name IS NULL;

-- 6. How many duplicate order IDs were detected?
SELECT 
    order_id, 
    COUNT(*) AS duplicate_count
FROM final_sales
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 7. What is the average order value?
SELECT ROUND(AVG(net_amount), 2) AS average_order_value 
FROM final_sales;

-- 8. How many orders were placed through each sales channel?
SELECT 
    sales_channel, 
    COUNT(*) AS order_count
FROM final_sales
GROUP BY sales_channel
ORDER BY order_count DESC;

-- 9. What is the payment-status distribution?
SELECT 
    payment_status, 
    COUNT(*) as status_count
FROM final_sales
GROUP BY payment_status
ORDER BY status_count DESC;

-- 10. Which customers placed more than three orders?
SELECT 
    customer_id, 
    customer_name, 
    COUNT(order_id) AS total_orders
FROM final_sales
GROUP BY customer_id, customer_name
Having COUNT(order_id) > 3
ORDER BY total_orders DESC;