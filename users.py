import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    res = db.query(sql, [user_id])
    return res[0] if res else None

def get_movies(user_id):
    sql = "SELECT id, title, release_date FROM movies WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])