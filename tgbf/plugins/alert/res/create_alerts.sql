CREATE TABLE alerts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_id REAL NOT NULL,
    token TEXT NOT NULL,
    price REAL NOT NULL,
    date_time DATETIME DEFAULT CURRENT_TIMESTAMP
)