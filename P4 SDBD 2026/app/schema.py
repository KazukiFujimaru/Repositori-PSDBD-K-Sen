import sqlite3

def init_db():
    # Database 1: Tanpa Constraint (Hanya untuk demonstrasi celah keamanan)
    conn1 = sqlite3.connect('database1.db')
    conn1.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    conn1.execute("INSERT INTO users VALUES ('Kazuki', 'PSDBD2026')")
    conn1.commit()
    conn1.close()

    # Database 2: Dengan Constraint (Struktur Data yang Benar)
    conn2 = sqlite3.connect('database2.db')
    conn2.execute("PRAGMA foreign_keys = ON")
    conn2.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL, 
            password TEXT NOT NULL CHECK(length(password) >= 8)
        )
    """)
    # Input data awal
    try:
        conn2.execute("INSERT INTO users (username, password) VALUES ('Kazuki', 'PSDBD2026')")
    except:
        pass
    conn2.commit()
    conn2.close()
    print("Database berhasil diinisialisasi.")

if __name__ == "__main__":
    init_db()