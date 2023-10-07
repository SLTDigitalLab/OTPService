CREATE TABLE IF NOT EXISTS otp_logs(
    id INTEGER generated always as identity PRIMARY KEY,
    tenent_id uuid NOT NULL,
    user_id uuid NOT NULL,
    type VARCHAR(10) NOT NULL,
    sent_to VARCHAR(50) NOT NULL,
    otp VARCHAR(20) NOT NULL,
    otp_client_secret VARCHAR(36) NOT NULL,
    otp_created_at timestamptz NOT NULL,
    otp_expired_at timestamptz NOT NULL,
    otp_validated BOOLEAN DEFAULT FALSE,
    otp_validated_at timestamptz DEFAULT NULL,
    otp_tries INTEGER DEFAULT 0,
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(tenent_id) REFERENCES tenents(id)
)   