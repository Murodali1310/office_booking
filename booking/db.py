import sqlite3
from datetime import datetime

DB_PATH = "booking.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY,
            room_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            start_ts TIMESTAMP NOT NULL,
            end_ts TIMESTAMP NOT NULL,
            FOREIGN KEY(room_id) REFERENCES rooms(id)
        );
        """)
        c.executemany(
            "INSERT OR IGNORE INTO rooms(id, name) VALUES(?, ?)",
            [(i, f"Cabinet {i}") for i in range(1, 6)]
        )
        conn.commit()

def is_free(room_id: int, start_ts: datetime, end_ts: datetime):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("""SELECT * FROM bookings
            WHERE room_id = ? AND NOT (end_ts <= ? OR start_ts >= ?)""",
            (room_id, start_ts, end_ts))
        return c.fetchone() is None

def get_current_booking(room_id: int, start_ts: datetime, end_ts: datetime):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("""SELECT * FROM bookings
            WHERE room_id = ? AND NOT (end_ts <= ? OR start_ts >= ?)""",
            (room_id, start_ts, end_ts))
        return c.fetchone()

def add_booking(room_id: int, user_name: str, email: str, phone: str,
                start_ts: datetime, end_ts: datetime):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("""
        INSERT INTO bookings(room_id, user_name, email, phone, start_ts, end_ts)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (room_id, user_name, email, phone, start_ts, end_ts))
        conn.commit()
