CREATE TABLE IF NOT EXISTS marketing_logs(
    id INTEGER generated always as identity PRIMARY KEY,
    tenent_id uuid NOT NULL,
    user_id uuid NOT NULL,
    type VARCHAR(10) NOT NULL,
    sent_to VARCHAR(50) NOT NULL,
    body VARCHAR(160) NOT NULL,
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(tenent_id) REFERENCES tenents(id)
)