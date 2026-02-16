-- 1. Calendar
CREATE TABLE dim_mounth (
    dim_mounth_id BIGINT PRIMARY KEY,
    year BIGINT,
    month BIGINT,
    month_name VARCHAR(50),
    quarter VARCHAR(10)
);

-- 2. Company
CREATE TABLE dim_company (
    dim_company_id BIGINT PRIMARY KEY,
    company_name VARCHAR(255)
);

-- 3. Locations
CREATE TABLE dim_locations (
    dim_region_id BIGINT PRIMARY KEY,
    location_name VARCHAR(255),
    locality VARCHAR(255)
);

-- 4. Language
CREATE TABLE dim_language (
    dim_language_id BIGINT PRIMARY KEY,
    original_language VARCHAR(50)
);

-- 5. Service
CREATE TABLE dim_service (
    dim_service_id BIGINT PRIMARY KEY,
    service_name VARCHAR(255)
);

-- 6. Credential
CREATE TABLE dim_credential (
    dim_credential_id BIGINT PRIMARY KEY,
    internal_name VARCHAR(255)
);
CREATE TABLE dim_products (
    products_id BIGINT PRIMARY KEY,
    dim_region_id BIGINT REFERENCES dim_locations(dim_region_id),
    product_name VARCHAR(255),
    product_tier TEXT,
    partner_type VARCHAR(50)
);
CREATE TABLE bridge_product_service (
    bridge_product_service_id BIGINT PRIMARY KEY,
    dim_products_id BIGINT REFERENCES dim_products(products_id),
    dim_service_id BIGINT REFERENCES dim_service(dim_service_id),
    UNIQUE (dim_products_id, dim_service_id)
);

CREATE TABLE bridge_product_credential (
    bridge_product_credential_id BIGINT PRIMARY KEY,
    dim_products_id BIGINT REFERENCES dim_products(products_id),
    dim_credential_id BIGINT REFERENCES dim_credential(dim_credential_id),
    UNIQUE (dim_products_id, dim_credential_id)
);

CREATE TABLE fact_comment (
    fact_comment_id BIGSERIAL PRIMARY KEY,
    dim_month_id     BIGINT NOT NULL REFERENCES dim_mounth(dim_mounth_id),
    dim_product_id   BIGINT NOT NULL REFERENCES dim_products(products_id),
    dim_company_id   BIGINT REFERENCES dim_company(dim_company_id),
    dim_language_id  BIGINT NOT NULL REFERENCES dim_language(dim_language_id),

    comment_count BIGINT NOT NULL,
    min_rating    SMALLINT,
    avg_rating    NUMERIC(3,2),
    max_rating    SMALLINT,

    -- гарантуємо grain
    CONSTRAINT uq_fact_comment_grain UNIQUE (
        dim_month_id,
        dim_product_id,
        dim_company_id,
        dim_language_id
    )
);
