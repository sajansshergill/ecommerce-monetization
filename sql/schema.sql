CREATE TABLE IF NOT EXISTS retail_clean (
    invoiceno TEXT,
    customerid BIGINT,
    invoicedate TIMESTAMP,
    quantity NUMERIC,
    unitprice NUMERIC,
    revenue NUMERIC,
    country TEXT,
    iscancel BOOLEAN,
    isnegativeqty BOOLEAN,
    isleakage BOOLEAN
);
