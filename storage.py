import sqlite3
import pandas as pd

from datetime import datetime

DB_PATH = "health.db"
COLUMNS = []


def init_db():
    """Cria o banco e a tabela, se ainda não existirem."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            spo2 REAL,
            bpm REAL,
            systolic REAL,
            diastolic REAL,
            temperature REAL,
            sleep_hours REAL,
            mood REAL,
            radiation REAL
        )
    """)
    conn.commit()
    conn.close()

def save_data(readings):
    timestamp = datetime
    values = [timestamp] + [readings.get(col) for col in COLUMNS]
    placeholders = ", ".join("?" * len(values))
    columns = ", ".join(["timestamp"] + COLUMNS)

    conn = sqlite3.connect(DB_PATH)
    conn.execute(f"INSERT INTO checkins ({columns}) VALUES ({placeholders})", values)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    conn = sqlite3.connect(DB_PATH)
    print(conn.execute("SELECT * FROM checkins").fetchall())
    conn.close()