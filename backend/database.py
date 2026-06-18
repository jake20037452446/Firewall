import sqlite3

DATABASE_NAME = "database.db"


# 🟢 Get DB connection
def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None


# 🟢 Create tables
def create_tables():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    except Exception as e:
        print("Error creating tables:", e)


if __name__ == "__main__":
    create_tables()