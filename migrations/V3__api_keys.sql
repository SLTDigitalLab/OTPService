CREATE TABLE IF NOT EXISTS api_keys (
    api_key VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    user_id uuid NOT NULL,
    tenent_id uuid NOT NULL,
    allowed_origins TEXT[],
    scope json,
    expire_ts timestamptz,
    disabled BOOLEAN DEFAULT FALSE,
    date_disabled timestamptz DEFAULT NULL,
    last_used timestamptz DEFAULT NULL,
    created_ts timestamptz DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(tenent_id) REFERENCES tenents(id)
)