CREATE TABLE IF NOT EXISTS users (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY, 
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
    created_ts timestamptz, 
    updated_ts timestamptz, 
    last_login_ts timestamptz
);