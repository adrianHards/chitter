DROP TABLE IF EXISTS relationships;
DROP SEQUENCE IF EXISTS relationships_id_seq;

DROP TABLE IF EXISTS messages;
DROP SEQUENCE IF EXISTS messages_id_seq;

DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS users_id_seq;

CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE,
    password VARCHAR(64),
    email VARCHAR(20),
    join_date TIMESTAMP
);

CREATE SEQUENCE IF NOT EXISTS messages_id_seq;
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    content VARCHAR(255),
    pub_date TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE SEQUENCE IF NOT EXISTS relationships_id_seq;
CREATE TABLE relationships (
    id SERIAL PRIMARY KEY,
    from_user_id INTEGER,
    to_user_id INTEGER,
    FOREIGN KEY (from_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (to_user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- The UNIQUE constraint ensures that the combination of values in the from_user_id and to_user_id columns must be unique across the table.
CREATE UNIQUE INDEX relationship_index ON relationships (from_user_id, to_user_id);
