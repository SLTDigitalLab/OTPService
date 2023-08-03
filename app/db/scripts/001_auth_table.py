from psql_connector import DB, default_config


def createAuthTable():
    db = DB(default_config())
    db.exec(
        """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(255) PRIMARY KEY, 
            first_name VARCHAR(255), 
            last_name VARCHAR(255), 
            email VARCHAR(255) UNIQUE,
            password VARCHAR(255), 
            is_super_admin BOOLEAN DEFAULT FALSE,
            disabled BOOLEAN DEFAULT FALSE,
            email_verified BOOLEAN DEFAULT FALSE,
            tel_verified BOOLEAN DEFAULT FALSE,
            tel VARCHAR(255) DEFAULT NULL, 
            company VARCHAR(255) DEFAULT NULL,
            company_id_number VARCHAR(255) DEFAULT NULL,
            company_id_url VARCHAR(255) DEFAULT NULL,
            created_ts TIMESTAMP, 
            updated_ts TIMESTAMP, 
            last_login_ts TIMESTAMP);
    """
    )
    result = db.fetchone()
    return result


print(createAuthTable())
