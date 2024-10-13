CREATE TABLE IF NOT EXISTS log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    request_date VARCHAR(50),
    periods INT,
    amount DECIMAL(10, 2),
    rate DECIMAL(5, 2),
    results TEXT
);