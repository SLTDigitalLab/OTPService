from db.psql_connector import DB, default_config


def createAPITokenTable():
    db = DB(default_config())
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS api_token (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            deactivated BOOLEAN DEFAULT FALSE,
            origin VARCHAR(255) DEFAULT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user(id)
        )
    """
    )
    result = db.fetchone()
    return result


print(createAPITokenTable())
