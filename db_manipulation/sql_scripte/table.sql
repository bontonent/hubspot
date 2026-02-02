
-- 1. Dim Reviewer
CREATE TABLE dim_reviewer (
    reviewer_id VARCHAR(255) PRIMARY KEY,
    client_company VARCHAR(255),
    client_industry VARCHAR(255)
);

-- 2. Data (Календар)
CREATE TABLE data (
    data_id INT PRIMARY KEY,
    year INT,
    mouth INT, 
    day INT
);

-- 3. Dim Language
CREATE TABLE dim_language (
    language_id INT PRIMARY KEY,
    original_language VARCHAR(50)
);

-- 4. Dim Company
CREATE TABLE Dim_company (
    company_id BIGINT PRIMARY KEY,
    company_name VARCHAR(255),
    tier VARCHAR(50),
    budget_range VARCHAR(50),
    partner_type VARCHAR(50)
);

-- 5. Location
CREATE TABLE location (
    location_id INT PRIMARY KEY,
    country_code VARCHAR(10),
    city VARCHAR(255),
    region VARCHAR(255) 
);

-- 6. Dim Service
CREATE TABLE dim_service (
    service_id INT PRIMARY KEY,
    service_name VARCHAR(255),
    api_name VARCHAR(255),
    category_id INT
);

-- 7. Dim Credential
CREATE TABLE dim_credential (
    credential_id INT PRIMARY KEY,
    internal_name VARCHAR(255),
    meta_lang VARCHAR(50),
    grantee_type VARCHAR(50)
);

-- 8. Products
CREATE TABLE products (
    products_id BIGINT PRIMARY KEY,
    products VARCHAR(255),
    client_industry TEXT,
    location_id INT REFERENCES location(location_id)
);

-- 9. Service Product (Bridge)
CREATE TABLE service_product (
    service_product_id INT PRIMARY KEY,
    products_id BIGINT REFERENCES products(products_id),
    service_id INT REFERENCES dim_service(service_id)
);

-- 10. Credential Product (Bridge)
CREATE TABLE credential_product (
    credenttial_product_id INT PRIMARY KEY,
    products_id BIGINT REFERENCES products(products_id),
    credential_id INT REFERENCES dim_credential(credential_id)
);

-- 11. Comment (Fact Table with Analytics)
CREATE TABLE Comment (
    comment_id BIGINT PRIMARY KEY,
    reviewer_id VARCHAR(255) REFERENCES dim_reviewer(reviewer_id),
    company_id BIGINT REFERENCES Dim_company(company_id),
    products_id BIGINT REFERENCES products(products_id),
    data_id INT REFERENCES data(data_id),
    language_id INT REFERENCES dim_language(language_id),
    
    -- Аналітичні метрики з діаграми
    total_comment INT,
    min_rating INT,
    avg_rating NUMERIC(3, 2), -- Використовуємо NUMERIC для точності середнього
    max_rating INT
);

/*
-- 1. Таблиця календаря
CREATE TABLE dim_mounth (
    dim_mounth_id INT PRIMARY KEY,
    year INT,
    mouth INT,
    mounth_name VARCHAR(50),
    Quarter VARCHAR(10)
);

-- 2. Таблиця компаній
CREATE TABLE dim_company (
    dim_company_id BIGINT PRIMARY KEY,
    company_name VARCHAR(255),
    tier VARCHAR(50),
    budget_range VARCHAR(50),
    partner_type VARCHAR(50)
);

-- 3. Таблиця регіонів
CREATE TABLE dim_region (
    dim_region_id INT PRIMARY KEY,
    Region_name VARCHAR(255),
    region VARCHAR(255)
);

-- 4. Таблиця сервісів (Технічні параметри)
CREATE TABLE dim_service (
    dim_service_id INT PRIMARY KEY,
    service_name VARCHAR(255),
    api_name VARCHAR(255),
    category_id INT
);

-- 5. Таблиця креденціалів (Технічні параметри)
CREATE TABLE dim_credential (
    dim_credential_id INT PRIMARY KEY,
    internal_name VARCHAR(255),
    meta_lang VARCHAR(50),
    grantee_type VARCHAR(50)
);

-- 6. Міст між сервісами та креденціалами (Bridge Table)
CREATE TABLE bridge_service_and_credential (
    bridge_service_and_credential_id INT PRIMARY KEY,
    dim_credential_id INT REFERENCES dim_credential(dim_credential_id),
    dim_service_id INT REFERENCES dim_service(dim_service_id)
);

-- 7. Таблиця продуктів (Зв'язок з регіоном та технічним мостом)
CREATE TABLE dim_products (
    products_id BIGINT PRIMARY KEY,
    dim_region_id INT REFERENCES dim_region(dim_region_id),
    client_industry TEXT,
    bridge_service_and_credential_id INT REFERENCES bridge_service_and_credential(bridge_service_and_credential_id)
);

-- 8. Таблиця фактів (Comment)
CREATE TABLE Comment (
    -- У сховищах часто додають surrogate key для фактів, але базуємося на FK з діаграми
    dim_mounth_id INT REFERENCES dim_mounth(dim_mounth_id),
    dim_products_id BIGINT REFERENCES dim_products(products_id),
    dim_company_id BIGINT REFERENCES dim_company(dim_company_id),
    
    -- Метрики
    total_comment INT,
    min_rating INT,
    avg_rating NUMERIC(3, 2),
    max_rating INT
);
*/