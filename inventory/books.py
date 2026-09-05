from flask import Blueprint, render_template, request
from database.db import get_db
from auth.roles import require_role
import io
import csv

# Blueprint with URL prefix
books = Blueprint("books", __name__, url_prefix="/books")

# -----------------------------
# Add a Single Book (Manager)
# -----------------------------
@books.route("/add_book", methods=["GET", "POST"])
@require_role("manager")
def add_book_route():   # ← UNIQUE NAME
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        isbn = request.form["isbn"]
        quantity = request.form["quantity"]
        genre = request.form["category"]

        db = get_db()
        db.execute("""
            INSERT INTO books (title, author, isbn, quantity, genre)
            VALUES (?, ?, ?, ?, ?)
        """, (title, author, isbn, quantity, genre))
        db.commit()
        db.close()

        return "Book added successfully!"

    return render_template("add_book.html")


# -----------------------------
# Bulk Upload Books (Manager)
# -----------------------------
@books.route("/bulk_upload", methods=["GET", "POST"])
@require_role("manager")
def bulk_upload_route():   # ← UNIQUE NAME
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return "No file uploaded."

        db = get_db()

        # Convert uploaded bytes → text for CSV reader
        text_stream = io.TextIOWrapper(file.stream, encoding="utf-8")
        reader = csv.DictReader(text_stream)

        for row in reader:
            db.execute("""
                INSERT INTO books (title, author, isbn, quantity, genre)
                VALUES (?, ?, ?, ?, ?)
            """, (
                row.get("title", ""),
                row.get("author", ""),
                row.get("isbn", ""),
                row.get("quantity", 0),
                row.get("genre", "")
            ))

        db.commit()
        db.close()

        return "Bulk upload complete!"

    return render_template("bulk_upload.html")