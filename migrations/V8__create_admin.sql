INSERT INTO users (
    first_name, 
    last_name, 
    email,
    password, 
    is_super_admin,
    email_verified,
    tel_verified,
    tel
) VALUES ('Admin', '1', 'admin1@example.com', '$argon2id$v=19$m=65536,t=3,p=4$HEf3pE/E7nxC5wnZW4RFKQ$GyYShPvetnOh546jG/Xvi1XfG+j9J8oVWnKANkJqF5s', true, true, true, '0000000000');
INSERT INTO users (
    first_name, 
    last_name, 
    email,
    password, 
    is_super_admin,
    email_verified,
    tel_verified,
    tel
) VALUES ('Admin', '2', 'admin2@example.com', '$argon2id$v=19$m=65536,t=3,p=4$nxFbcYpyOn9r5tKuu68iFA$IUV4QqVli5wbRrzFHa39XJRMmrDeIJj8FxSzCzRuZ4g', true, true, true, '0000000000');