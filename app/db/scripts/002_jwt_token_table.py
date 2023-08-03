from db.psql_connector import DB, default_config


def createJWTTokenTable():
    db = DB(default_config())
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS jwt_token (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            deactivated BOOLEAN DEFAULT FALSE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user(id)
        )
    """
    )
    result = db.fetchone()
    return result


print(createJWTTokenTable())
