CREATE TABLE IF NOT EXISTS shilling (
    user_uuid integer primary key,
    chat_uuid integer NOT NULL
);