
CREATE TABLE IF NOT EXISTS hcpcs_codes (
    id BIGSERIAL PRIMARY KEY,
    hcpcs_code VARCHAR(50) NOT NULL,
    group_code VARCHAR(50),
    category_name VARCHAR(255),
    long_description TEXT NOT NULL,
    desc_hash CHAR(32) NOT NULL,
    effective_date DATE NOT NULL DEFAULT CURRENT_DATE,
    end_date DATE,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    inserted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_hcpcs_current
ON hcpcs_codes (hcpcs_code)
WHERE is_current = TRUE;

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id BIGSERIAL PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL,
    extracted_rows INT DEFAULT 0,
    valid_rows INT DEFAULT 0,
    inserted_versions INT DEFAULT 0,
    error_message TEXT
);

CREATE OR REPLACE VIEW v_hcpcs_current AS
SELECT *
FROM hcpcs_codes
WHERE is_current = TRUE;

CREATE OR REPLACE VIEW v_hcpcs_history AS
SELECT *
FROM hcpcs_codes;
