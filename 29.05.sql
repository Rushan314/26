SELECT * FROM new_schema.orders;

SELECT 
id, 
order_date,
CASE
WHEN bucket = "less than equal to 100" THEN "маленький"
WHEN bucket = "101 to 300" THEN "средний"
ELSE "большой"
END AS ducket_size
FROM orders;
