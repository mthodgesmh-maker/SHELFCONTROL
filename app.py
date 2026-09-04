from flask import Flask, render_template

# Blueprints
from auth.auth_routes import auth
from inventory.books import books
from inventory.view import view

# Database setup
from database.db import close_db
from database.inventory_tables import create_users_table, create_inventory_tables
from database.seed import seed_users

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(books)
app.register_blueprint(view)

@app.route("/")
def home():
    return render_template("home.html")

# Ensure DB closes properly
app.teardown_appcontext(close_db)

import os

if __name__ == "__main__":
    # IMPORTANT: Run DB setup inside app context
    with app.app_context():
        create_users_table()
        create_inventory_tables()
        seed_users()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)