import sqlite3
import pandas as pd

from datetime import datetime

DB_PATH = "health.db"
COLUMNS = [
    "spo2",
    "bpm",
    "systolic",
    "diastolic",
    "temperature",
    "sleep_hours",
]

def load_data(file_path=DB_PATH):
    conn = sqlite3.connect(file_path)
    try:
        df = pd.read_sql("SELECT * from checkins",
            conn,
            parse_dates=["timestamp"],
        )
    finally:
        conn.close()
    return df

def get_last_value(column: str) -> float:
    df = load_data()
    if df.empty:
        return None
    if column not in df.columns:
        raise KeyError(f"Unknown health data column: {column}")
    value = df[column].iloc[-1]
    if pd.isna(value):
        return None
    return float(value)

def init_db(file_path=DB_PATH):
    """Cria o banco e a tabela, se ainda não existirem."""
    conn = sqlite3.connect(file_path)
    try:
        with conn:
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
    finally:
        conn.close()

def save_data(readings, file_path=DB_PATH):
    if not isinstance(readings, dict):
        raise TypeError("readings must be a dictionary")

    if set(readings) != set(COLUMNS):
        missing = sorted(set(COLUMNS) - set(readings))
        unexpected = sorted(set(readings) - set(COLUMNS))
        raise ValueError(
            f"Expected fields {COLUMNS}; missing={missing}, unexpected={unexpected}"
        )

    for column in COLUMNS:
        value = readings[column]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{column} must be a number")
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError(f"{column} must be finite")

    init_db(file_path)
    timestamp = datetime.now().isoformat(timespec="microseconds")
    values = [timestamp] + [readings[column] for column in COLUMNS]
    placeholders = ", ".join("?" for _ in values)
    columns = ", ".join(["timestamp"] + COLUMNS)

    conn = sqlite3.connect(file_path)
    try:
        with conn:
            conn.execute(
                f"INSERT INTO checkins ({columns}) VALUES ({placeholders})",
                values,
            )
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    conn = sqlite3.connect(DB_PATH)
    print(conn.execute("SELECT * FROM checkins").fetchall())
    conn.close()