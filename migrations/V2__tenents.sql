CREATE TABLE IF NOT EXISTS tenents (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id uuid NOT NULL,
    name VARCHAR(50) NOT NULL,
    email_otp_size INTEGER NOT NULL DEFAULT 6,
    email_otp_expired_in_s INTEGER NOT NULL DEFAULT 300,
    email_otp_max_tries INTEGER NOT NULL DEFAULT 3,
    sms_otp_size INTEGER NOT NULL DEFAULT 6,
    sms_otp_expired_in_s INTEGER NOT NULL DEFAULT 300,
    sms_otp_max_tries INTEGER  NOT NULL DEFAULT 3,
    sms_otp_template VARCHAR (160)  NOT NULL DEFAULT 'Your OTP is {otp}. It''s expired at {expired_at}. (Created: {created_at}))',
    email_otp_template VARCHAR (2048) NOT NULL DEFAULT 'Your OTP is {otp}. It''s expired at {expired_at}. (Created: {created_at}))',
    verified BOOLEAN DEFAULT FALSE,
    disabled BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)