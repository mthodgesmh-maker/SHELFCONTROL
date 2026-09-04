from database.db import get_db
from auth.security import hash_password

def seed_users():
    db = get_db()

    users = [
        ("manager", "manager123", "manager"),
        ("employee", "employee123", "employee"),
        ("tester", "tester123", "tester"),
        ("dev", "dev123", "manager")
    ]

    for username, password, role in users:
        db.execute("""
            INSERT OR IGNORE INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (username, hash_password(password), role))

    db.commit()
