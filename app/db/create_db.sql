CREATE TABLE IF NOT EXISTS users (
    user_id    INTEGER  PRIMARY KEY NOT NULL,
    first_name      TEXT,
    username TEXT,
    language_code TEXT,
    fsm_state TEXT,
    join_date DATETIME DEFAULT ( (DATETIME('now') ) ) 
                       NOT NULL,
    phone         TEXT,
    donation      DECIMAL  DEFAULT (0) 
);

CREATE TABLE IF NOT EXISTS poll_names (
    poll_id INTEGER PRIMARY KEY AUTOINCREMENT
                    NOT NULL,
    name    TEXT,
    description TEXT
);


CREATE TABLE IF NOT EXISTS poll_results (
    poll_id INTEGER,
    user_id INTEGER,
    data    TEXT,
    description   TEXT
);

