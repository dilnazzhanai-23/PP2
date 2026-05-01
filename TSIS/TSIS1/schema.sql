CREATE TABLE IF NOT EXISTS phonebook23 (
    id SERIAL PRIMARY KEY,
    first_name TEXT,
    second_name TEXT,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);


CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES phonebook2(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);


INSERT INTO groups (name) VALUES ('Family'), ('Work'), ('Friend'), ('Other') 
ON CONFLICT (name) DO NOTHING;