CREATE TABLE dim_reviewer (
    reviewer_id SERIAL PRIMARY KEY,
    client_company TEXT,
    client_industry TEXT
);

CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    year INT,
    month INT,
    day INT
);

CREATE TABLE dim_company (
    company_id SERIAL PRIMARY KEY,
    company_name TEXT
);

CREATE TABLE dim_service (
    service_id SERIAL PRIMARY KEY,
    service_name TEXT
);

CREATE TABLE dim_credential (
    credential_id SERIAL PRIMARY KEY,
    internal_name TEXT
);

CREATE TABLE dim_location (
    location_id SERIAL PRIMARY KEY,
    country_code VARCHAR(10),
    city_name TEXT,
    region_name TEXT
);

CREATE TABLE dim_product (
    products_id SERIAL PRIMARY KEY,
    product_name TEXT,
    location_id INT REFERENCES dim_location(location_id),
    credential_id BIGINT REFERENCES dim_credential(credential_id),
    service_id BIGINT REFERENCES dim_service(service_id)
);

-- Створення таблиці фактів (агрегована версія)
CREATE TABLE fact_comments (
    fact_id SERIAL PRIMARY KEY,
    reviewer_id INT REFERENCES dim_reviewer(reviewer_id),
    company_id BIGINT REFERENCES dim_company(company_id),
    products_id BIGINT REFERENCES dim_product(products_id),
    date_id INT REFERENCES dim_date(date_id),
    count_comment INT,
    min_rating NUMERIC(3,2),
    avg_rating NUMERIC(3,2),
    max_rating NUMERIC(3,2)
);
