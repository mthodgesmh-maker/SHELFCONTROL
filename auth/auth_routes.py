from flask import Blueprint, render_template, request, redirect, session
from database.db import get_db
from auth.security import verify_password

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            return "Invalid username or password"

        if user["locked"] == 1:
            return "Account locked. Contact manager."

        if verify_password(user["password_hash"], password):
            db.execute(
                "UPDATE users SET failed_attempts = 0 WHERE id = ?",
                (user["id"],)
            )
            db.commit()
            session["user"] = username
            session["role"] = user["role"]
            return redirect("/")
        else:
            attempts = user["failed_attempts"] + 1
            locked = 1 if attempts >= 5 else 0

            db.execute(
                "UPDATE users SET failed_attempts = ?, locked = ? WHERE id = ?",
                (attempts, locked, user["id"])
            )
            db.commit()

            return "Invalid password"

    return render_template("login.html")
@auth.route("/debug_users")
def debug_users():
    db = get_db()
    rows = db.execute("SELECT id, username, role FROM users").fetchall()
    return "<br>".join([f"{row['id']} | {row['username']} | {row['role']}" for row in rows])
