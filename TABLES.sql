SELECT * FROM od.new_table;

ALTER TABLE new_table
ADD COLUMN Status VARCHAR(20) DEFAULT 'Pending';

ALTER TABLE new_table
MODIFY COLUMN TotalAmount DECIMAL(14,2);

ALTER TABLE new_table
RENAME COLUMN CustomerID TO CliID;

ALTER TABLE new_table
MODIFY COLUMN OrderDate DATE NOT NULL;

ALTER TABLE new_table
DROP COLUMN Status;

CREATE INDEX idx_orderDate ON new_table(OrderDate);

CREATE INDEX idx_CliID ON new_table(CliID, OrderDate);

CREATE UNIQUE INDEX idx_UN ON new_table(OrderID);


SHOW INDEX FROM new_table;

DROP INDEX idx_orderDate ON new_table;

CREATE TEMPORARY TABLE tempy LIKE new_table;

DROP TEMPORARY TABLE tempy;

TRUNCATE TABLE new_table;

DROP TABLE new_table;