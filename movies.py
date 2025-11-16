import db

def add_new_movie(title, director, release_date, description, user_id):
    sql = """INSERT INTO movies (title, director, release_date, description, user_id) VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, director, release_date, description, user_id])

def get_movies():
    sql = "SELECT id, title FROM movies ORDER BY title"
    return db.query(sql)

def get_movie(movie_id):
    sql = """SELECT movies.title,
            movies.director,
            movies.release_date,
            movies.description,
            users.username
        FROM movies, users
        WHERE movies.user_id = users.id AND
            movies.id = ?"""
    return db.query(sql, [movie_id])[0]

def see_if_movie_exists(title):
    sql = "SELECT 1 FROM movies WHERE movies.title = ?"
    res = db.query(sql, [title])[0]

    if res is None:
        return True

    return False