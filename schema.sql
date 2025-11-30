CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    director TEXT,
    release_date INTEGER,
    description TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    title TEXT
);

CREATE TABLE movie_genres (
    id INTEGER PRIMARY KEY,
    movie_id INTEGER REFERENCES movies,
    genre_id INTEGER REFERENCES genres
);