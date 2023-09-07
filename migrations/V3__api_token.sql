CREATE TABLE IF NOT EXISTS api_token (
            id INTEGER generated always as identity PRIMARY KEY,
            token TEXT NOT NULL,
            user_id VARCHAR(255) NOT NULL,
            deactivated BOOLEAN DEFAULT FALSE,
            origin VARCHAR(255) DEFAULT NULL,
            created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )