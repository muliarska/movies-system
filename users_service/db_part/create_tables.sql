
CREATE TABLE users(
    user_id UUID PRIMARY KEY,
    username TEXT,
    password TEXT,
    name TEXT,
    email TEXT,
    dob TEXT,
    log_in BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP

);
