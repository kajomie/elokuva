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
    user_id INTEGER REFERENCES users ON DELETE CASCADE
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    movie_id INTEGER REFERENCES movies ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    rating INTEGER,
    review_text TEXT,
    UNIQUE(movie_id, user_id)
);

CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    title TEXT
);

CREATE TABLE movie_genres (
    id INTEGER PRIMARY KEY,
    movie_id INTEGER REFERENCES movies ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genres ON DELETE CASCADE
);