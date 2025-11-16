import db

def add_new_movie(title, director, release_date, description, user_id):
    sql = """INSERT INTO movies (title, director, release_date, description, user_id) VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, director, release_date, description, user_id])

def get_movies():
    sql = "SELECT id, title FROM movies ORDER BY title"
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
    return db.query(sql, [movie_id])[0]

def see_if_movie_exists(title):
    sql = "SELECT 1 FROM movies WHERE title = ?"
    res = db.query(sql, [title])

    if res:
        return True

    return False

def update_movie(movie_id, title, director, release_date, description):
    sql = """UPDATE movies SET title = ?,
                            director = ?,
                            release_date = ?,
                            description = ?
                            WHERE id = ?"""
    db.execute(sql, [title, director, release_date, description, movie_id])

def remove_movie(movie_id):
    sql = "DELETE FROM movies WHERE id = ?"
    db.execute(sql, [movie_id])