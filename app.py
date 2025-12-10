import secrets
import sqlite3
from flask import Flask
from flask import abort, flash, redirect, render_template, request, session
import config
import db
import movies
import re
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    all_movies = movies.get_movies()
    return render_template("index.html", movies=all_movies)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)

    if not user:
        abort(404)

    movies = users.get_movies(user_id)
    user_reviews = users.get_user_reviews(user_id)

    return render_template("show_user.html", user=user, movies=movies, user_reviews=user_reviews)

@app.route("/movie/<int:movie_id>")
def show_movie(movie_id):
    movie = movies.get_movie(movie_id)

    if not movie:
        abort(404)

    genres = movies.get_genres(movie_id)
    reviews = movies.get_reviews(movie_id)

    user_id = session["user_id"]
    review_check = movies.see_if_review_exists(movie_id, user_id)

    return render_template("show_movie.html", movie=movie, genres=genres, reviews=reviews, review_check=review_check)

@app.route("/add_movie")
def add_movie():
    require_login()
    genres = movies.get_all_genres()
    return render_template("add_movie.html", genres=genres)

@app.route("/create_movie", methods=["POST"])
def create_movie():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 60 or not re.search(".*\S.*", title):
        abort(403)

    director = request.form["director"]
    if not director or len(director) > 60 or not re.search(".*\S.*", director):
        abort(403)

    release_date = request.form["release_date"]
    if not re.search("^(19|20)\d{2}$", release_date):
        abort(403)

    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)

    user_id = session["user_id"]

    all_genres = movies.get_all_genres()

    genres = []
    section = request.form.getlist("section")

    if section:
        for genre in section:
            if int(genre) not in list(all_genres.keys()):
                abort(403)

        genres = section

    res = movies.see_if_movie_exists(title)

    if "confirm_add" in request.form:
        if not res:
            movies.add_new_movie(title, director, release_date, description, user_id, genres)
        else:
            flash("Elokuva on jo lisätty!")
            return redirect("/add_movie")

    return redirect("/")

@app.route("/create_review", methods=["POST"])
def create_review():
    require_login()
    check_csrf()

    rating = request.form["rating"]
    if not re.search("^[1-5]$", rating):
        abort(403)

    review_text = request.form["review_text"]
    if not review_text or len(review_text) > 1000:
        abort(403)

    movie_id = request.form["movie_id"]
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(403)

    user_id = session["user_id"]

    if "confirm_review" in request.form:
        movies.add_new_review(movie_id, user_id, rating, review_text)

    return redirect("/movie/" + str(movie_id))

@app.route("/edit_movie/<int:movie_id>")
def edit_movie(movie_id):
    require_login()
    movie = movies.get_movie(movie_id)

    if not movie:
        abort(404)

    if movie["user_id"] != session["user_id"]:
        abort(403)

    all_genres = movies.get_all_genres()
    genres = {}

    for genre in all_genres:
        genres[genre] = ""

    for genre in movies.get_genres(movie_id):
        genres[genre] = genre

    return render_template("edit_movie.html", movie=movie, genres=genres, all_genres=all_genres)

@app.route("/update_movie", methods=["POST"])
def update_movie():
    require_login()
    check_csrf()

    movie_id = request.form["movie_id"]
    movie = movies.get_movie(movie_id)

    if not movie:
        abort(404)

    if movie["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 60 or not re.search(".*\S.*", title):
        abort(403)

    director = request.form["director"]
    if not director or len(director) > 60 or not re.search(".*\S.*", director):
        abort(403)

    release_date = request.form["release_date"]
    if not re.search("^(19|20)\d{2}$", release_date):
        abort(403)

    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)

    all_genres = movies.get_all_genres()

    genres = []
    section = request.form.getlist("section")

    if section:
        for genre in section:
            if int(genre) not in list(all_genres.keys()):
                abort(403)

        genres = section

    if "save_edit" in request.form:
        movies.update_movie(movie_id, title, director, release_date, description, genres)

    return redirect("/movie/" + str(movie_id))

@app.route("/remove_movie/<int:movie_id>", methods=["GET", "POST"])
def remove_movie(movie_id):
    require_login()

    movie = movies.get_movie(movie_id)

    if not movie:
        abort(404)

    if movie["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_movie.html", movie=movie)

    if request.method == "POST":
        check_csrf()
        if "confirm_remove" in request.form:
            movies.remove_movie(movie_id)
            return redirect("/")

        return redirect("/movie/" + str(movie_id))

@app.route("/search_movie")
def search_movie():
    query = request.args.get("query")
    if not query:
        query = ""
        res = []
    else:
        res = movies.search_movies(query)
    return render_template("search_movie.html", query=query, res=res)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not username or not password1 or not password2:
        flash("VIRHE: käyttäjänimi tai salasana puuttuu")
        return redirect("/register")
    if len(password1) < 5 or len(password2) < 5:
        flash("VIRHE: salasanan tulee olla minimissään 5 merkkiä")
        return redirect("/register")
    if len(username) > 40 or len(password1) > 250 or len(password2) > 250:
        flash("VIRHE: käyttäjänimi tai salasana on liian pitkä")
        return redirect("/register")

    if not re.search(".*\S.*", username):
        flash("VIRHE: käyttäjänimi ei saa olla tyhjä")
        return redirect("/register")
    if not re.search(".*\S.*", password1) or not re.search(".*\S.*", password2):
        flash("VIRHE: salasana ei saa olla tyhjä")
        return redirect("/register")

    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    flash("Tunnuksen luonti onnistui")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")