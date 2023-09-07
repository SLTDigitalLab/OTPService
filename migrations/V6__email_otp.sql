CREATE TABLE IF NOT EXISTS email_otp(
            id INTEGER generated always as identity PRIMARY KEY,
            tenent VARCHAR(255) NOT NULL,
            user_id VARCHAR(255) NOT NULL,
            sent_to VARCHAR(50) NOT NULL,
            otp VARCHAR(20) NOT NULL,
            created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
            expired_at timestamptz NOT NULL,
            validated BOOLEAN DEFAULT FALSE,
            validated_at timestamptz DEFAULT NULL,
            tries INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )