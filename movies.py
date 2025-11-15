import db

def add_new_movie(title, director, release_date, description, user_id):
    sql = """INSERT INTO movies (title, director, release_date, description, user_id) VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, director, release_date, description, user_id])