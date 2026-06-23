import sqlite3

def setup_database():
    conn = sqlite3.connect("garage.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    
    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    setup_database()