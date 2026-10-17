-- queries.sql
-- SQL queries for the Car Wash analysis (SQLite).
-- Table name: bookings
-- Columns: booking_id, date, hour, service, vehicle_type, washing_point,
--          payment_method, price_pkr, rating

-- Query 1: Total bookings and total revenue
SELECT COUNT(*) AS total_bookings,
       SUM(price_pkr) AS total_revenue_pkr,
       ROUND(AVG(price_pkr), 0) AS avg_booking_value_pkr
FROM bookings;

-- Query 2: Revenue and bookings by service
SELECT service,
       COUNT(*) AS bookings,
       SUM(price_pkr) AS revenue_pkr
FROM bookings
GROUP BY service
ORDER BY revenue_pkr DESC;

-- Query 3: Bookings by month
SELECT strftime('%Y-%m', date) AS month,
       COUNT(*) AS bookings,
       SUM(price_pkr) AS revenue_pkr
FROM bookings
GROUP BY month
ORDER BY month;

-- Query 4: Revenue by washing point
SELECT washing_point,
       COUNT(*) AS bookings,
       SUM(price_pkr) AS revenue_pkr
FROM bookings
GROUP BY washing_point
ORDER BY revenue_pkr DESC;

-- Query 5: Average rating by service (ignoring missing ratings)
SELECT service,
       ROUND(AVG(rating), 2) AS avg_rating,
       COUNT(rating) AS rated_bookings
FROM bookings
WHERE rating IS NOT NULL
GROUP BY service
ORDER BY avg_rating DESC;

-- Query 6: Top 5 busiest days
SELECT date,
       COUNT(*) AS bookings
FROM bookings
GROUP BY date
ORDER BY bookings DESC
LIMIT 5;
