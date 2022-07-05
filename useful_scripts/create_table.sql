CREATE TABLE IF NOT EXISTS chat (
    chat_uuid serial primary key,
    chat_name varchar(512),
    shill_message text,
    shill_links varchar(255)[],
    shill_timeout integer default 60,
    msg_timeout integer default 1
);

CREATE TABLE IF NOT EXISTS users (
    user_uuid serial primary key,
    current_chat integer references chat (chat_uuid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_chat (
    chat_uuid integer references chat (chat_uuid) ON DELETE CASCADE,
    user_uuid integer references users (user_uuid) ON DELETE CASCADE
);