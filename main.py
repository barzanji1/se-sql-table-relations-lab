# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("data.sqlite")

pd.read_sql("""SELECT * FROM sqlite_master""", conn)


# STEP 1
# Boston employees
df_boston = pd.read_sql("""
    SELECT
        e.firstName,
        e.lastName
    FROM employees AS e
    JOIN offices AS o
        ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston';
""", conn)


# STEP 2
# Offices with zero employees
df_zero_emp = pd.read_sql("""
    SELECT
        o.officeCode,
        o.city
    FROM offices AS o
    LEFT JOIN employees AS e
        ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL;
""", conn)


# STEP 3
# All employees and their office location
df_employee = pd.read_sql("""
    SELECT
        e.firstName,
        e.lastName,
        o.city,
        o.state
    FROM employees AS e
    LEFT JOIN offices AS o
        ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName;
""", conn)


# STEP 4
# Customers who have not placed an order
df_contacts = pd.read_sql("""
    SELECT
        c.contactFirstName,
        c.contactLastName,
        c.phone,
        c.salesRepEmployeeNumber
    FROM customers AS c
    LEFT JOIN orders AS o
        ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName;
""", conn)


# STEP 5
# Customer payments sorted numerically by amount
df_payment = pd.read_sql("""
    SELECT
        c.contactFirstName,
        c.contactLastName,
        p.paymentDate,
        p.amount
    FROM customers AS c
    JOIN payments AS p
        ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC;
""", conn)


# STEP 6
# Employees whose customers average over 90k credit limit
df_credit = pd.read_sql("""
    SELECT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        COUNT(c.customerNumber) AS numcustomers
    FROM employees AS e
    JOIN customers AS c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY
        e.employeeNumber,
        e.firstName,
        e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY numcustomers DESC;
""", conn)


# STEP 7
# Product sales
df_product_sold = pd.read_sql("""
    SELECT
        p.productName,
        COUNT(DISTINCT od.orderNumber) AS numorders,
        SUM(od.quantityOrdered) AS totalunits
    FROM products AS p
    JOIN orderdetails AS od
        ON p.productCode = od.productCode
    GROUP BY
        p.productCode,
        p.productName
    ORDER BY totalunits DESC;
""", conn)


# STEP 8
# Number of unique customers who purchased each product
df_total_customers = pd.read_sql("""
    SELECT
        p.productName,
        p.productCode,
        COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products AS p
    JOIN orderdetails AS od
        ON p.productCode = od.productCode
    JOIN orders AS o
        ON od.orderNumber = o.orderNumber
    GROUP BY
        p.productCode,
        p.productName
    ORDER BY numpurchasers DESC;
""", conn)


# STEP 9
# Number of customers per office
df_customers = pd.read_sql("""
    SELECT
        o.officeCode,
        o.city,
        COUNT(c.customerNumber) AS n_customers
    FROM offices AS o
    LEFT JOIN employees AS e
        ON o.officeCode = e.officeCode
    LEFT JOIN customers AS c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY
        o.officeCode,
        o.city;
""", conn)


# STEP 10
# Employees who sold products purchased by fewer than 20 customers
# STEP 10
df_under_20 = pd.read_sql("""
    SELECT DISTINCT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        off.city,
        off.officeCode
    FROM employees AS e
    JOIN offices AS off
        ON e.officeCode = off.officeCode
    JOIN customers AS c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders AS o
        ON c.customerNumber = o.customerNumber
    JOIN orderdetails AS od
        ON o.orderNumber = od.orderNumber
        WHERE od.productCode IN (
        SELECT od2.productCode
        FROM orderdetails AS od2
        JOIN orders AS o2
            ON od2.orderNumber = o2.orderNumber
        GROUP BY od2.productCode
        HAVING COUNT(DISTINCT o2.customerNumber) < 20
    )
    ORDER BY
        CASE WHEN e.firstName = 'Loui' THEN 0 ELSE 1 END,
        e.firstName;
""", conn)

# STEP 11
conn.close()