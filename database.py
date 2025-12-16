import sqlite3

def init_db():
    conn = sqlite3.connect("parking.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS parking_slots (
        slot_id TEXT PRIMARY KEY,
        is_available INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        plate TEXT,
        slot_id TEXT,
        entry_time TEXT
    )
    """)

    # Insert slots only once
    slots = ["A1", "A2", "B1", "B2"]
    for s in slots:
        c.execute("INSERT OR IGNORE INTO parking_slots VALUES (?, ?)", (s, 1))

    conn.commit()
    conn.close()
