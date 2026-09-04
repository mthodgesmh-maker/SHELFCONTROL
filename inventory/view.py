from flask import Blueprint, render_template, request
from database.db import get_db

view = Blueprint("view", __name__)

@view.route("/inventory")
def inventory():
    db = get_db()
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("inventory.html", books=books)
@view.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        title = request.form.get("title", "")
        author = request.form.get("author", "")
        isbn = request.form.get("isbn", "")

        db = get_db()

        query = "SELECT * FROM books WHERE 1=1"
        params = []

        if title:
            query += " AND title LIKE ?"
            params.append(f"%{title}%")

        if author:
            query += " AND author LIKE ?"
            params.append(f"%{author}%")

        if isbn:
            query += " AND isbn LIKE ?"
            params.append(f"%{isbn}%")

        results = db.execute(query, params).fetchall()

        return render_template("search_results.html", results=results)

    return render_template("search.html")
@view.route("/search", methods=["GET", "POST"])
def search_inventory():
    if request.method == "POST":
        title = request.form.get("title", "")
        author = request.form.get("author", "")
        isbn = request.form.get("isbn", "")

        db = get_db()

        query = "SELECT * FROM books WHERE 1=1"
        params = []

        if title:
            query += " AND title LIKE ?"
            params.append(f"%{title}%")

        if author:
            query += " AND author LIKE ?"
            params.append(f"%{author}%")

        if isbn:
            query += " AND isbn LIKE ?"
            params.append(f"%{isbn}%")

        results = db.execute(query, params).fetchall()

        return render_template("search_results.html", results=results)

    return render_template("search.html")