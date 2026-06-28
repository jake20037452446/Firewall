import sqlite3
import hashlib

DATABASE_NAME = "database.db"


# 🟢 Get DB connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# 🔐 Password hashing (IMPORTANT for login systems)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# 🟢 Create tables
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# 🟢 Helper: insert user
def create_user(name, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
    """, (name, email, hash_password(password)))

    conn.commit()
    conn.close()


# 🟢 Helper: get user by email
def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE email = ?
    """, (email,))

    user = cursor.fetchone()
    conn.close()
    return user


if __name__ == "__main__":
    create_tables()
