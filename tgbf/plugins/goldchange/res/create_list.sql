CREATE TABLE price_change (
    token_symbol TEXT NOT NULL PRIMARY KEY,
    avg_price REAL NOT NULL,
    last_price REAL NOT NULL,
    chg_perc INTEGER NOT NULL,
    date_added TEXT NOT NULL
)