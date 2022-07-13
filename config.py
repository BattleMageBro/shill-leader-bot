import os


config = {
    "TOKEN": os.environ.get("TOKEN", "token"),
    "SQL_USER": os.environ.get("SQL_USER"),
    "SQL_PASSWORD": os.environ.get("SQL_PASSWORD", "shill"),
    "SQL_DB": os.environ.get("SQL_DB", "shill_db"),
    "SQL_HOST": os.environ.get("SQL_HOST", "localhost"),
    "SQL_PORT": os.environ.get("SQL_PORT", 5432),
    "LOG_LEVEL": os.environ.get("LOG_LEVEL", "DEBUG")
}