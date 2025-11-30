import db

def get_all_genres():
    sql = "SELECT id, title FROM genres ORDER BY id"
    res = db.query(sql)

    genres = {}
    for id, title in res:
        genres[id] = title

    return genres

def add_new_movie(title, director, release_date, description, user_id, genres):
    sql = """INSERT INTO movies (title, director, release_date, description, user_id) VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, director, release_date, description, user_id])

    movie_id = db.last_insert_id()

    sql = "INSERT INTO movie_genres (movie_id, genre_id) VALUES (?, ?)"
    for genre in genres:
        db.execute(sql, [movie_id, genre])

def get_genres(movie_id):
    sql = """SELECT genres.title
            FROM genres, movie_genres
            WHERE movie_genres.movie_id = ? AND
            genres.id = movie_genres.genre_id"""
    return db.query(sql, [movie_id])

def get_movies():
    sql = "SELECT id, title, release_date FROM movies ORDER BY title"
    return db.query(sql)

def get_movie(movie_id):
    sql = """SELECT movies.id,
            movies.title,
            movies.director,
            movies.release_date,
            movies.description,
            users.id user_id,
            users.username
        FROM movies, users
        WHERE movies.user_id = users.id AND
            movies.id = ?"""
    res = db.query(sql, [movie_id])
    return res[0] if res else None

def see_if_movie_exists(title):
    sql = "SELECT 1 FROM movies WHERE title = ?"
    res = db.query(sql, [title])

    if res:
        return True

    return False

def update_movie(movie_id, title, director, release_date, description, genres):
    sql = """UPDATE movies SET title = ?,
                            director = ?,
                            release_date = ?,
                            description = ?
                            WHERE id = ?"""
    db.execute(sql, [title, director, release_date, description, movie_id])

    sql = "DELETE FROM movie_genres WHERE movie_id = ?"
    db.execute(sql, [movie_id])

    sql = "INSERT INTO movie_genres (movie_id, genre_id) VALUES (?, ?)"
    for genre in genres:
        db.execute(sql, [movie_id, genre])

def remove_movie(movie_id):
    sql = "DELETE FROM movie_genres WHERE movie_id = ?"
    db.execute(sql, [movie_id])
    sql = "DELETE FROM movies WHERE id = ?"
    db.execute(sql, [movie_id])

def search_movies(query):
    sql = """SELECT id, title, director, release_date
            FROM movies
            WHERE title LIKE ? OR director LIKE ?
            ORDER BY title"""
    searching_query = "%" + query + "%"
    return db.query(sql, [searching_query, searching_query])