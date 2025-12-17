import sqlite3

DB_NAME = "metro.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            txn_id TEXT,
            from_station TEXT,
            to_station TEXT,
            tickets INTEGER,
            total_fare INTEGER,
            journey_date TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ticket_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            txn_id TEXT,
            ticket_id TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_booking(txn_id, frm, to, tickets, fare, date, created_at):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO bookings 
        (txn_id, from_station, to_station, tickets, total_fare, journey_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (txn_id, frm, to, tickets, fare, date, created_at))

    conn.commit()
    conn.close()

def save_ticket(txn_id, ticket_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO ticket_details (txn_id, ticket_id)
        VALUES (?, ?)
    """, (txn_id, ticket_id))

    conn.commit()
    conn.close()
