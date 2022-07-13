CREATE TABLE IF NOT EXISTS chat (
    chat_uuid bigint unique,
    chat_name varchar(512),
    shill_message text,
    shill_links varchar(255)[],
    shill_timeout integer default 60,
    msg_timeout integer default 1,
    shill_end float default 1
);

CREATE TABLE IF NOT EXISTS users (
    user_uuid bigint unique,
    current_chat bigint references chat (chat_uuid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_chat (
    chat_uuid bigint references chat (chat_uuid) ON DELETE CASCADE,
    user_uuid bigint references users (user_uuid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS packs (
    pack_uuid serial primary key,
    pack_description text,
    shill_links varchar(255)[]
);