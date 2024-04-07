import sqlite3

def init_db():
    """Create the database file and execute the SQL script."""
    with open("schema.sql", "r") as file:
        sql = file.read()

    db_file = "db.sqlite3"
    conn = sqlite3.connect(db_file)

    cursor = conn.cursor()
    cursor.executescript(sql)

    conn.commit()
    conn.close()
    print("Database created.")

init_db()