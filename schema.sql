CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE forums (
    id SERIAL PRIMARY KEY,
    forum_name TEXT,
    visible INTEGER
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    thread_name TEXT,
    content TEXT,
    visible INTEGER,
    forum_id INTEGER REFERENCES forums,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads,
    sent_at TIMESTAMP
);

CREATE TABLE onlineUsers (
    id SERIAL PRIMARY KEY,
    username TEXT
);
