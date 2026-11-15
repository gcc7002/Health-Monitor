import sqlite3
import pandas as pd

from datetime import datetime

from indicators import CHECKIN_FIELDS, CHECKIN_OPTIONAL_FIELDS

DB_PATH = "health.db"
LEGACY_CHECKIN_FIELDS = (*CHECKIN_FIELDS, "sleep_hours")
COLUMNS = list(LEGACY_CHECKIN_FIELDS)

TIMELINE_COLUMNS = (
    "timestamp",
    "event_type",
    "context",
    "description",
    "bpm",
    "bpm_source",
    "spo2",
    "systolic",
    "diastolic",
    "temperature",
    "radiation",
    "radiation_source",
    "calories_burned_estimated",
    "calories_source",
    "bpm_average",
    "bpm_average_source",
    "bpm_max",
    "bpm_max_source",
    "intensity",
    "measurement_source",
    "symptoms",
    "observation",
    "mood",
    "stress",
    "isolation",
    "sleep_well",
    "period_start",
    "period_end",
    "sleep_quality",
    "sleep_interruptions",
    "sleep_hours",
)


def _insert_record(table, values, file_path):
    columns = tuple(values)
    placeholders = ", ".join("?" for _ in columns)
    column_sql = ", ".join(columns)
    conn = sqlite3.connect(file_path)
    try:
        with conn:
            conn.execute(
                f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders})",
                tuple(values[column] for column in columns),
            )
    finally:
        conn.close()


def _validate_time_period(start_at, end_at):
    start = datetime.fromisoformat(str(start_at))
    end = datetime.fromisoformat(str(end_at))
    if end <= start:
        raise ValueError("The end time must be after the start time")


def _validate_optional_number(data, field, minimum=None, maximum=None):
    value = data.get(field)
    if value is None or value == "":
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field} must be a number")
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError(f"{field} must be finite")
    if minimum is not None and value < minimum:
        raise ValueError(f"{field} must be at least {minimum}")
    if maximum is not None and value > maximum:
        raise ValueError(f"{field} must be at most {maximum}")
    return value

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

def get_last_value(column: str, file_path=DB_PATH):
    df = load_data(file_path)
    if df.empty:
        return None
    if column not in df.columns:
        raise KeyError(f"Unknown health data column: {column}")
    values = df[column].dropna()
    if values.empty:
        return None
    return values.iloc[-1]

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
            checkin_columns = {
                row[1] for row in conn.execute("PRAGMA table_info(checkins)")
            }
            optional_column_types = {
                "measurement_context": "TEXT",
                "measurement_source": "TEXT",
                "symptoms": "TEXT",
                "observation": "TEXT",
                "radiation_source": "TEXT",
            }
            for name, column_type in optional_column_types.items():
                if name not in checkin_columns:
                    conn.execute(
                        f"ALTER TABLE checkins ADD COLUMN {name} {column_type}"
                    )

            conn.executescript("""
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activity_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    start_at TEXT NOT NULL,
                    end_at TEXT NOT NULL,
                    intensity REAL,
                    bpm_average REAL,
                    bpm_average_source TEXT,
                    bpm_max REAL,
                    bpm_max_source TEXT,
                    calories_burned_estimated REAL,
                    calories_source TEXT,
                    observation TEXT
                );
                CREATE TABLE IF NOT EXISTS wellbeing_checkins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    mood INTEGER NOT NULL CHECK (mood BETWEEN 1 AND 5),
                    stress TEXT,
                    isolation TEXT,
                    sleep_well INTEGER,
                    note TEXT
                );
                CREATE TABLE IF NOT EXISTS sleep_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_at TEXT NOT NULL,
                    end_at TEXT NOT NULL,
                    quality TEXT,
                    interruptions TEXT,
                    observation TEXT
                );
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


def save_checkin(readings, file_path=DB_PATH):
    if not isinstance(readings, dict):
        raise TypeError("readings must be a dictionary")
    required = set(CHECKIN_FIELDS)
    allowed = required | set(CHECKIN_OPTIONAL_FIELDS)
    if not required.issubset(readings) or set(readings) - allowed:
        raise ValueError(
            f"Check-in requires {sorted(required)} and allows "
            f"{sorted(allowed - required)}"
        )

    values = {}
    for field in CHECKIN_FIELDS:
        value = _validate_optional_number(readings, field)
        if value is None:
            raise ValueError(f"{field} is required")
        values[field] = value
    values["radiation"] = _validate_optional_number(
        readings, "radiation", minimum=0
    )
    values["timestamp"] = datetime.now().isoformat(timespec="microseconds")
    for field in CHECKIN_OPTIONAL_FIELDS:
        if field in readings and field != "radiation":
            values[field] = readings[field] or None

    init_db(file_path)
    _insert_record("checkins", values, file_path)


def save_activity(activity, file_path=DB_PATH):
    required = {"activity_type", "description", "start_at", "end_at"}
    if not isinstance(activity, dict) or not required.issubset(activity):
        raise ValueError(f"Activity requires {sorted(required)}")
    _validate_time_period(activity["start_at"], activity["end_at"])

    values = {
        "activity_type": str(activity["activity_type"]).strip(),
        "description": str(activity["description"]).strip(),
        "start_at": str(activity["start_at"]),
        "end_at": str(activity["end_at"]),
        "intensity": _validate_optional_number(
            activity, "intensity", minimum=1, maximum=10
        ),
        "bpm_average": _validate_optional_number(
            activity, "bpm_average", minimum=30, maximum=250
        ),
        "bpm_average_source": activity.get("bpm_average_source") or None,
        "bpm_max": _validate_optional_number(
            activity, "bpm_max", minimum=30, maximum=250
        ),
        "bpm_max_source": activity.get("bpm_max_source") or None,
        "calories_burned_estimated": _validate_optional_number(
            activity, "calories_burned_estimated", minimum=0
        ),
        "calories_source": activity.get("calories_source") or None,
        "observation": activity.get("observation") or None,
    }
    if not values["activity_type"]:
        raise ValueError("Activity type is required")
    if not values["description"]:
        raise ValueError("Activity description is required")
    init_db(file_path)
    _insert_record("activities", values, file_path)


def save_wellbeing(reading, file_path=DB_PATH):
    required = {"mood"}
    if not isinstance(reading, dict) or not required.issubset(reading):
        raise ValueError("Well-being check-in requires a mood score")
    mood = _validate_optional_number(reading, "mood", minimum=1, maximum=5)
    if mood is None or int(mood) != mood:
        raise ValueError("Mood must be a whole number from 1 to 5")

    values = {
        "timestamp": datetime.now().isoformat(timespec="microseconds"),
        "mood": int(mood),
        "stress": reading.get("stress") or None,
        "isolation": reading.get("isolation") or None,
        "sleep_well": (
            None if reading.get("sleep_well") is None
            else int(bool(reading["sleep_well"]))
        ),
        "note": reading.get("note") or None,
    }
    init_db(file_path)
    _insert_record("wellbeing_checkins", values, file_path)


def save_sleep_record(record, file_path=DB_PATH):
    required = {"start_at", "end_at"}
    if not isinstance(record, dict) or not required.issubset(record):
        raise ValueError("Sleep record requires start_at and end_at")
    _validate_time_period(record["start_at"], record["end_at"])
    values = {
        "start_at": str(record["start_at"]),
        "end_at": str(record["end_at"]),
        "quality": record.get("quality") or None,
        "interruptions": record.get("interruptions") or None,
        "observation": record.get("observation") or None,
    }
    init_db(file_path)
    _insert_record("sleep_records", values, file_path)


def load_timeline(file_path=DB_PATH):
    init_db(file_path)
    conn = sqlite3.connect(file_path)
    try:
        checkins = pd.read_sql_query("SELECT * FROM checkins", conn)
        activities = pd.read_sql_query("SELECT * FROM activities", conn)
        wellbeing = pd.read_sql_query("SELECT * FROM wellbeing_checkins", conn)
        sleep_records = pd.read_sql_query("SELECT * FROM sleep_records", conn)
    finally:
        conn.close()

    events = []
    for item in checkins.to_dict("records"):
        event = {column: None for column in TIMELINE_COLUMNS}
        event.update({
            "timestamp": item["timestamp"],
            "event_type": "Health check-in",
            "context": item.get("measurement_context") or "Not specified",
            "description": item.get("symptoms"),
            "bpm": item.get("bpm"),
            "bpm_source": item.get("measurement_source"),
            "spo2": item.get("spo2"),
            "systolic": item.get("systolic"),
            "diastolic": item.get("diastolic"),
            "temperature": item.get("temperature"),
            "radiation": item.get("radiation"),
            "radiation_source": item.get("radiation_source"),
            "measurement_source": item.get("measurement_source"),
            "symptoms": item.get("symptoms"),
            "observation": item.get("observation"),
            "sleep_hours": item.get("sleep_hours"),
        })
        events.append(event)

    for item in activities.to_dict("records"):
        event = {column: None for column in TIMELINE_COLUMNS}
        event.update({
            "timestamp": item["start_at"],
            "event_type": "Activity",
            "context": item["activity_type"],
            "description": item["description"],
            "bpm_average": item["bpm_average"],
            "bpm_average_source": item["bpm_average_source"],
            "bpm_max": item["bpm_max"],
            "bpm_max_source": item["bpm_max_source"],
            "calories_burned_estimated": item["calories_burned_estimated"],
            "calories_source": item["calories_source"],
            "intensity": item["intensity"],
            "observation": item["observation"],
            "period_start": item["start_at"],
            "period_end": item["end_at"],
        })
        events.append(event)

    for item in wellbeing.to_dict("records"):
        event = {column: None for column in TIMELINE_COLUMNS}
        sleep_well = item["sleep_well"]
        event.update({
            "timestamp": item["timestamp"],
            "event_type": "Well-being check-in",
            "context": "Well-being",
            "mood": item["mood"],
            "stress": item["stress"],
            "isolation": item["isolation"],
            "sleep_well": (
                None if sleep_well is None else "Yes" if sleep_well else "No"
            ),
            "observation": item["note"],
        })
        events.append(event)

    for item in sleep_records.to_dict("records"):
        event = {column: None for column in TIMELINE_COLUMNS}
        event.update({
            "timestamp": item["start_at"],
            "event_type": "Sleep",
            "context": "Sleep period",
            "period_start": item["start_at"],
            "period_end": item["end_at"],
            "sleep_quality": item["quality"],
            "sleep_interruptions": item["interruptions"],
            "observation": item["observation"],
            "sleep_hours": (
                datetime.fromisoformat(item["end_at"])
                - datetime.fromisoformat(item["start_at"])
            ).total_seconds() / 3600,
        })
        events.append(event)

    timeline = pd.DataFrame(events, columns=TIMELINE_COLUMNS)
    if not timeline.empty:
        timeline["timestamp"] = pd.to_datetime(
            timeline["timestamp"], format="mixed"
        )
        timeline = timeline.sort_values("timestamp", ascending=False).reset_index(drop=True)
    return timeline

if __name__ == "__main__":
    init_db()
    conn = sqlite3.connect(DB_PATH)
    print(conn.execute("SELECT * FROM checkins").fetchall())
    conn.close()