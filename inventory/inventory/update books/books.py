from flask import Blueprint, render_template, request
from database.db import get_db
from auth.roles import require_role

books = Blueprint("books", __name__)

@books.route("/bulk_upload", methods=["GET", "POST"])
@require_role("manager")
def bulk_upload():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return "No file uploaded."

        import csv
        db = get_db()

        # Read CSV file from the uploaded stream
        reader = csv.DictReader(file.stream)
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
        return "Bulk upload complete!"

    return render_template("bulk_upload.html")
@books.route("/add_book", methods=["GET", "POST"])
@require_role("manager")
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        isbn = request.form["isbn"]
        quantity = request.form["quantity"]
        category = request.form["category"]

        db = get_db()
        db.execute("""
            INSERT INTO books (title, author, isbn, quantity, category)
            VALUES (?, ?, ?, ?, ?)
        """, (title, author, isbn, quantity, category))
        db.commit()

        return "Book added successfully!"

    return render_template("add_book.html")