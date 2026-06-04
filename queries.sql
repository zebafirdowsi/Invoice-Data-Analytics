-- ================================================
-- Business Analytics on Invoice Data
-- Project by: Zeeba Firdows
-- Database: SQLite (Invoice Bot)
-- ================================================


-- Q1: Top 5 Customers by Revenue
-- Note: grand_total column has data quality issues
-- Actual revenue extracted via Python from JSON

SELECT 
    customer_name, 
    SUM(grand_total) AS total_revenue
FROM invoice_records
GROUP BY customer_name
ORDER BY total_revenue DESC
LIMIT 5;


-- Q2: Most Sold Products by Quantity
-- Note: product data lives in invoice_details.full_data (JSON)
-- Extracted via Python loop

SELECT 
    name, 
    use_count
FROM products
ORDER BY use_count DESC
LIMIT 5;


-- Q3: Monthly Invoice Trend
SELECT 
    strftime('%Y-%m', created_at) AS month,
    COUNT(*) AS total_invoices,
    SUM(grand_total) AS total_revenue
FROM invoice_records
GROUP BY month
ORDER BY month;


-- Q4: Inactive Customers (No activity in 30+ days)
SELECT 
    name, 
    last_used_at
FROM customers
WHERE last_used_at < date('now', '-30 days')
ORDER BY last_used_at ASC;