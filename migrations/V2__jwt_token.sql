CREATE TABLE IF NOT EXISTS jwt_token (
            id INTEGER generated always as identity PRIMARY KEY,
            token TEXT NOT NULL,
            user_id VARCHAR NOT NULL,
            deactivated BOOLEAN DEFAULT FALSE,
            created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
    )