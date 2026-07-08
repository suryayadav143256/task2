# Exploratory Data Analysis & Business Intelligence Report

This report presents descriptive statistics, univariate analysis, and solutions to key business questions using SQL and visualizations.

## 1. Descriptive Statistics & Univariate Analysis

### Numerical Summary Statistics

| index | Quantity | UnitPrice | LineTotal | IsCancelled |
| --- | --- | --- | --- | --- |
| count | 534129.0 | 534129.0 | 534129.0 | 534129.0 |
| mean | 9.916817847373949 | 4.695863909280343 | 18.250518271803255 | 0.017319786044195318 |
| std | 216.45211328273834 | 95.07918905022295 | 380.9453852431704 | 0.13046012003768043 |
| min | -80995.0 | 0.001 | -168469.6 | 0.0 |
| 25% | 1.0 | 1.25 | 3.75 | 0.0 |
| 50% | 3.0 | 2.1 | 9.9 | 0.0 |
| 75% | 10.0 | 4.13 | 17.57 | 0.0 |
| max | 80995.0 | 38970.0 | 168469.6 | 1.0 |


### Correlation Matrix

| index | Quantity | UnitPrice | LineTotal | IsCancelled |
| --- | --- | --- | --- | --- |
| Quantity | 1.0 | -0.0013759687078026613 | 0.9011503072176871 | -0.024352107315281504 |
| UnitPrice | -0.0013759687078026613 | 1.0 | -0.179054572341207 | 0.06126224810568492 |
| LineTotal | 0.9011503072176871 | -0.179054572341207 | 1.0 | -0.04003796094081848 |
| IsCancelled | -0.024352107315281504 | 0.06126224810568492 | -0.04003796094081848 | 1.0 |


#### Correlation Heatmap (Multivariate):

![Correlation Matrix Heatmap](C:/Users/HP/.gemini/antigravity/brain/fa836e50-85bb-4edf-afb3-7208fd016c50/images/correlation_heatmap.png)

> [!NOTE]
> There is a negative correlation between `IsCancelled` and `Quantity`/`LineTotal` as cancellations contain negative values.

## 2. SQL Business Questions and Results

### Q1: Top 5 Products by Revenue in the Last 6 Months

#### SQL Query:
```sql
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
```

#### Results Table:

| StockCode | Description | TotalRevenue | TotalQuantity |
| --- | --- | --- | --- |
| 23843 | PAPER CRAFT , LITTLE BIRDIE | 168469.6 | 80995 |
| DOT | DOTCOM POSTAGE | 123556.41 | 320 |
| 22423 | REGENCY CAKESTAND 3 TIER | 73147.51 | 5825 |
| 23084 | RABBIT NIGHT LIGHT | 64427.25 | 29539 |
| 85099B | JUMBO BAG RED RETROSPOT | 55645.76 | 28217 |


---

### Q2: Monthly Sales and Active Customer Trends

#### SQL Query:
```sql
SELECT 
    InvoiceYear || '-' || PRINTF('%02d', InvoiceMonth) AS Month,
    ROUND(SUM(LineTotal), 2) AS MonthlyRevenue,
    COUNT(DISTINCT CustomerID) AS ActiveCustomers,
    COUNT(DISTINCT InvoiceNo) AS TotalOrders
FROM transactions
GROUP BY InvoiceYear, InvoiceMonth
ORDER BY InvoiceYear, InvoiceMonth;
```

#### Results Table:

| Month | MonthlyRevenue | ActiveCustomers | TotalOrders |
| --- | --- | --- | --- |
| 2010-12 | 746723.61 | 1125 | 1885 |
| 2011-01 | 558448.56 | 893 | 1346 |
| 2011-02 | 497026.41 | 916 | 1319 |
| 2011-03 | 682013.98 | 1173 | 1772 |
| 2011-04 | 492367.84 | 1001 | 1486 |
| 2011-05 | 722094.1 | 1225 | 1995 |
| 2011-06 | 689977.23 | 1206 | 1862 |
| 2011-07 | 680156.99 | 1145 | 1745 |
| 2011-08 | 703510.58 | 1076 | 1639 |
| 2011-09 | 1017596.68 | 1395 | 2170 |
| 2011-10 | 1069368.23 | 1564 | 2402 |
| 2011-11 | 1456145.8 | 1835 | 3210 |
| 2011-12 | 432701.06 | 730 | 965 |


#### Visualization:

![Monthly Revenue Trend](C:/Users/HP/.gemini/antigravity/brain/fa836e50-85bb-4edf-afb3-7208fd016c50/images/monthly_revenue_trend.png)

---

### Q3: Top 5 Countries by Revenue (Excluding UK)

#### SQL Query:
```sql
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
```

#### Results Table:

| Country | TotalRevenue | UniqueCustomers |
| --- | --- | --- |
| Netherlands | 285446.34 | 9 |
| EIRE | 283140.52 | 31 |
| Germany | 228678.4 | 94 |
| France | 209625.37 | 90 |
| Australia | 138453.81 | 9 |


#### Visualization:

![Top Countries Revenue](C:/Users/HP/.gemini/antigravity/brain/fa836e50-85bb-4edf-afb3-7208fd016c50/images/top_countries_revenue.png)

---

### Q4: Average Order Value (AOV) by Country (Top 10)

#### SQL Query:
```sql
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
```

#### Results Table:

| Country | TotalRevenue | TotalOrders | AOV |
| --- | --- | --- | --- |
| Netherlands | 285446.34 | 94 | 3036.66 |
| Australia | 138453.81 | 57 | 2429.01 |
| Switzerland | 57067.6 | 54 | 1056.81 |
| EIRE | 283140.52 | 288 | 983.13 |
| Spain | 61558.56 | 90 | 683.98 |
| Portugal | 33683.05 | 58 | 580.74 |
| France | 209625.37 | 392 | 534.76 |
| Germany | 228678.4 | 457 | 500.39 |
| United Kingdom | 9001744.09 | 18019 | 499.57 |
| Belgium | 41196.34 | 98 | 420.37 |


---

### Q5: Customer Retention - Repeat vs One-Time Buyers

#### SQL Query:
```sql
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
```

#### Results Table:

| BuyerType | CustomerCount | Percentage |
| --- | --- | --- |
| One-Time Buyer | 1493 | 34.42 |
| Repeat Customer | 2845 | 65.58 |


---

### Q6: Hour of the Day Transaction Density and Revenue

#### SQL Query:
```sql
SELECT 
    InvoiceHour AS HourOfDay,
    COUNT(DISTINCT InvoiceNo) AS OrderCount,
    ROUND(SUM(LineTotal), 2) AS Revenue,
    ROUND(SUM(LineTotal) * 100.0 / (SELECT SUM(LineTotal) FROM transactions WHERE IsCancelled = 0), 2) AS RevenuePercentage
FROM transactions
WHERE IsCancelled = 0
GROUP BY InvoiceHour
ORDER BY OrderCount DESC;
```

#### Results Table:

| HourOfDay | OrderCount | Revenue | RevenuePercentage |
| --- | --- | --- | --- |
| 12.0 | 3220.0 | 1439324.66 | 13.52 |
| 13.0 | 2753.0 | 1261195.2 | 11.85 |
| 14.0 | 2457.0 | 1177907.52 | 11.07 |
| 11.0 | 2396.0 | 1236573.29 | 11.62 |
| 10.0 | 2361.0 | 1444814.77 | 13.58 |
| 15.0 | 2336.0 | 1350333.31 | 12.69 |
| 9.0 | 1484.0 | 990054.99 | 9.3 |
| 16.0 | 1335.0 | 752487.96 | 7.07 |
| 17.0 | 667.0 | 460963.92 | 4.33 |
| 8.0 | 566.0 | 283750.68 | 2.67 |
| 18.0 | 192.0 | 144603.61 | 1.36 |
| 19.0 | 146.0 | 50204.95 | 0.47 |
| 7.0 | 29.0 | 31059.21 | 0.29 |
| 20.0 | 18.0 | 18832.48 | 0.18 |
| 6.0 | 1.0 | 4.25 | 0.0 |


#### Visualization:

![Hourly Order Density](C:/Users/HP/.gemini/antigravity/brain/fa836e50-85bb-4edf-afb3-7208fd016c50/images/hourly_order_density.png)

---