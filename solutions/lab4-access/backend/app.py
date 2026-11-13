import os
from pathlib import Path

from flask import Flask, abort, g, redirect, render_template, request, session

from . import database
from .config import DEMO_GITHUB_TOKEN, FLASK_SECRET_KEY

BASE_DIR = Path(__file__).resolve().parent.parent


def create_app(test_config=None):
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "frontend" / "templates"),
        static_folder=str(BASE_DIR / "frontend" / "static"),
    )
    app.secret_key = FLASK_SECRET_KEY
    app.config.from_mapping(DATABASE_PATH=str(BASE_DIR / "data" / "students.db"))
    if test_config:
        app.config.update(test_config)
    app.config["DEMO_GITHUB_TOKEN"] = DEMO_GITHUB_TOKEN
    database.init_app(app)

    @app.after_request
    def security_headers(response):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response

    @app.get("/")
    def index():
        posts = database.get_db().cursor().execute("SELECT id, title, content FROM posts ORDER BY id").fetchall()
        return render_template("index.html", posts=posts)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            mark = database.placeholder()
            user = database.get_db().cursor().execute(
                f"SELECT id, username, role FROM users WHERE username = {mark} AND password = {mark}",
                (username, password),
            ).fetchone()
            if user:
                session["user_id"] = user[0]
                session["username"] = user[1]
                session["role"] = user[2]
                return redirect("/")
            error = "Неверные учётные данные"
        return render_template("login.html", error=error)

    @app.get("/logout")
    def logout():
        session.clear()
        return redirect("/")

    @app.get("/search")
    def search():
        query_text = request.args.get("q", "")
        cursor = database.get_db().cursor()
        pattern = f"%{query_text}%"
        mark = database.placeholder()
        cursor.execute(
            f"SELECT id, title, content FROM posts WHERE title LIKE {mark} OR content LIKE {mark}",
            (pattern, pattern),
        )
        posts = cursor.fetchall()
        return render_template("search.html", posts=posts, query=query_text)

    @app.route("/comments", methods=["GET", "POST"])
    def comments():
        connection = database.get_db()
        if request.method == "POST":
            author = request.form.get("author", "anonymous")
            content = request.form.get("content", "")
            mark = database.placeholder()
            connection.cursor().execute(
                f"INSERT INTO comments (author, content) VALUES ({mark}, {mark})",
                (author, content),
            )
            connection.commit()
            return redirect("/comments")
        rows = connection.cursor().execute("SELECT id, author, content FROM comments ORDER BY id").fetchall()
        return render_template("comments.html", comments=rows)

    @app.get("/profile")
    def profile():
        if "user_id" not in session:
            abort(401)
        user_id = request.args.get("id", default=session["user_id"], type=int)
        if user_id != session["user_id"] and session.get("role") != "admin":
            abort(403)
        mark = database.placeholder()
        user = database.get_db().cursor().execute(
            f"SELECT id, username, email, role, secret_note FROM users WHERE id = {mark}",
            (user_id,),
        ).fetchone()
        return render_template("profile.html", user=user)

    @app.get("/health")
    def health():
        return {"status": "ok", "database": "postgresql" if os.getenv("DATABASE_URL") else "sqlite"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
