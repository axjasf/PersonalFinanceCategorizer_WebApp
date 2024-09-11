CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    parent_id INTEGER,  -- Optional, for hierarchical categories
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);