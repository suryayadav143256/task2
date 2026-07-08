-- ==========================================
-- SQL Queries for Business Intelligence (Task 2)
-- ==========================================

-- Q1: Top 5 products by revenue in the last 6 months of the dataset
-- (Max date in dataset is 2011-12-09, so the last 6 months starts from 2011-06-09)
-- We filter out cancellations to reflect actual sales.
SELECT 
    StockCode, 
    Description, 
    ROUND(SUM(LineTotal), 2) AS TotalRevenue,
    SUM(Quantity) AS TotalQuantity
FROM transactions
WHERE InvoiceDate >= '2011-06-09 00:00:00'
  AND IsCancelled = 0
GROUP BY StockCode, Description
ORDER BY TotalRevenue DESC
LIMIT 5;

-- Q2: Monthly revenue, active customer count, and total orders trend
SELECT 
    InvoiceYear || '-' || PRINTF('%02d', InvoiceMonth) AS Month,
    ROUND(SUM(LineTotal), 2) AS MonthlyRevenue,
    COUNT(DISTINCT CustomerID) AS ActiveCustomers,
    COUNT(DISTINCT InvoiceNo) AS TotalOrders
FROM transactions
GROUP BY InvoiceYear, InvoiceMonth
ORDER BY InvoiceYear, InvoiceMonth;

-- Q3: Top 5 countries by revenue (excluding the United Kingdom)
SELECT 
    Country, 
    ROUND(SUM(LineTotal), 2) AS TotalRevenue,
    COUNT(DISTINCT CustomerID) AS UniqueCustomers
FROM transactions
WHERE Country != 'United Kingdom'
  AND IsCancelled = 0
GROUP BY Country
ORDER BY TotalRevenue DESC
LIMIT 5;

-- Q4: Average Order Value (AOV) by Country (Top 10 countries with at least 50 orders)
SELECT 
    Country,
    ROUND(SUM(LineTotal), 2) AS TotalRevenue,
    COUNT(DISTINCT InvoiceNo) AS TotalOrders,
    ROUND(SUM(LineTotal) / COUNT(DISTINCT InvoiceNo), 2) AS AOV
FROM transactions
WHERE IsCancelled = 0
GROUP BY Country
HAVING TotalOrders >= 50
ORDER BY AOV DESC
LIMIT 10;

-- Q5: Customer Retention - Repeat vs One-Time Buyers (excluding guest checkouts)
WITH CustomerOrders AS (
    SELECT 
        CustomerID,
        COUNT(DISTINCT InvoiceNo) AS OrderCount
    FROM transactions
    WHERE CustomerID NOT LIKE 'Guest_%'
      AND IsCancelled = 0
    GROUP BY CustomerID
)
SELECT 
    CASE 
        WHEN OrderCount = 1 THEN 'One-Time Buyer'
        ELSE 'Repeat Customer'
    END AS BuyerType,
    COUNT(*) AS CustomerCount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM CustomerOrders), 2) AS Percentage
FROM CustomerOrders
GROUP BY BuyerType;

-- Q6: Hour of the Day Transaction Density and Revenue
SELECT 
    InvoiceHour AS HourOfDay,
    COUNT(DISTINCT InvoiceNo) AS OrderCount,
    ROUND(SUM(LineTotal), 2) AS Revenue,
    ROUND(SUM(LineTotal) * 100.0 / (SELECT SUM(LineTotal) FROM transactions WHERE IsCancelled = 0), 2) AS RevenuePercentage
FROM transactions
WHERE IsCancelled = 0
GROUP BY InvoiceHour
ORDER BY OrderCount DESC;