CREATE TABLE aliases (
    user_id TEXT NOT NULL,
    alias TEXT NOT NULL,
    address TEXT NOT NULL,
	date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (user_id, alias)
)