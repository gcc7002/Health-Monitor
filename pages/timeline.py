from datetime import date, datetime, time, timedelta

import pandas as pd
import streamlit as st

from components import display_timeline_event
from storage import build_timeline_trend_data, load_timeline

st.set_page_config(page_title="Health Timeline", layout="wide")


def number_text(value, suffix=""):
    if pd.isna(value):
        return None
    return f"{float(value):g}{suffix}"


def source_text(value):
    if pd.isna(value) or not str(value).strip():
        return "source not recorded"
    return str(value)


def period_text(start, end):
    return (
        f"{pd.Timestamp(start):%Y-%m-%d %H:%M} – "
        f"{pd.Timestamp(end):%Y-%m-%d %H:%M}"
    )


def event_display_data(event):
    event_type = event["event_type"]
    metrics = []
    details = []

    if event_type == "Health check-in":
        source = event["measurement_source"]
        source_suffix = (
            f" · {source}"
            if pd.notna(source) and str(source).strip()
            else " · source not recorded"
        )
        for label, field, suffix in (
            ("Heart rate", "bpm", " bpm"),
            ("SpO₂", "spo2", "%"),
            ("Temperature", "temperature", " °C"),
            ("Radiation", "radiation", " mSv"),
        ):
            value = number_text(event[field], suffix)
            if value is not None:
                metrics.append((f"{label}{source_suffix}", value))
        if pd.notna(event["systolic"]) and pd.notna(event["diastolic"]):
            metrics.append((
                f"Blood pressure{source_suffix}",
                f"{number_text(event['systolic'])}/{number_text(event['diastolic'])} mmHg",
            ))
        details.extend([
            ("Measurement source", event["measurement_source"]),
            ("Radiation source", event["radiation_source"]),
            ("Symptoms", event["symptoms"]),
            ("Observation", event["observation"]),
        ])
    elif event_type == "Activity":
        for label, field, suffix in (
            (
                f"Average BPM · {source_text(event['bpm_average_source'])}",
                "bpm_average",
                " bpm",
            ),
            (
                f"Maximum BPM · {source_text(event['bpm_max_source'])}",
                "bpm_max",
                " bpm",
            ),
            (
                f"Calories burned · {source_text(event['calories_source'])}",
                "calories_burned_estimated",
                " kcal (estimated)",
            ),
            ("Perceived intensity", "intensity", "/10"),
        ):
            value = number_text(event[field], suffix)
            if value is not None:
                metrics.append((label, value))
        metrics.append((
            "Activity period",
            period_text(event["period_start"], event["period_end"]),
        ))
        details.extend([
            ("Activity", event["context"]),
            ("Description", event["description"]),
            ("Period start", event["period_start"]),
            ("Period end", event["period_end"]),
            ("Average BPM source", event["bpm_average_source"]),
            ("Maximum BPM source", event["bpm_max_source"]),
            ("Calories source", event["calories_source"]),
            ("Observation", event["observation"]),
        ])
    elif event_type == "Well-being check-in":
        mood_labels = {
            1: "1 — Very bad",
            2: "2 — Bad",
            3: "3 — Neutral",
            4: "4 — Good",
            5: "5 — Very good",
        }
        mood = event["mood"]
        if pd.notna(mood):
            metrics.append(("Mood · self-reported", mood_labels[int(mood)]))
        details.extend([
            ("Stress", event["stress"]),
            ("Feeling of isolation", event["isolation"]),
            ("Slept well?", event["sleep_well"]),
            ("Note", event["observation"]),
        ])
    elif event_type == "Sleep":
        duration = number_text(event["sleep_hours"], " hours")
        if duration is not None:
            metrics.append(("Sleep duration · derived from period", duration))
        metrics.append((
            "Sleep period",
            period_text(event["period_start"], event["period_end"]),
        ))
        details.extend([
            ("Sleep quality", event["sleep_quality"]),
            ("Period start", event["period_start"]),
            ("Period end", event["period_end"]),
            ("Interruptions", event["sleep_interruptions"]),
            ("Observation", event["observation"]),
        ])

    return metrics, details


st.title("Health Timeline")
st.caption(
    "Follow health measurements, activities, well-being, and sleep in one chronological view."
)
st.caption("Use the app navigation to return to the Dashboard or open Calendar.")
st.caption(
    "Indicator categories are generic prototype references, not clinical thresholds "
    "or NASA protocols. Values are plotted as individual records, without interpolation."
)

timeline = load_timeline()
if timeline.empty:
    st.info("No records yet. Save a check-in or another health record from the Dashboard.")

today = date.today()
filters = st.columns([1.2, 1, 1.4])
with filters[0]:
    date_range = st.date_input(
        "Date range",
        value=(today - timedelta(days=13), today),
        key="timeline_date_range",
    )
with filters[1]:
    available_types = sorted(timeline["event_type"].dropna().unique().tolist())
    selected_types = st.multiselect(
        "Record types",
        options=available_types,
        default=available_types,
        key="timeline_record_types",
    )
with filters[2]:
    st.caption("Calories shown here are burned during activity, not consumed.")

if not isinstance(date_range, tuple) or len(date_range) != 2:
    st.info("Select both a start and end date to view the timeline.")
    st.stop()

start_date, end_date = date_range
if start_date > end_date:
    st.error("The start date must be on or before the end date.")
    st.stop()

start_at = datetime.combine(start_date, time.min)
end_at = datetime.combine(end_date, time.max)
recent = timeline.loc[
    timeline["timestamp"].between(start_at, end_at)
    & timeline["event_type"].isin(selected_types)
].copy()

summary_columns = st.columns(4)
for column, event_type, label in zip(
    summary_columns,
    ("Health check-in", "Activity", "Well-being check-in", "Sleep"),
    ("Check-ins", "Activities", "Well-being", "Sleep periods"),
):
    with column:
        st.metric(label, int((recent["event_type"] == event_type).sum()))

timeline_tab, trends_tab = st.tabs(["Event timeline", "Indicator trends"])

with timeline_tab:
    st.subheader("Chronological events")
    if recent.empty:
        st.info("No records match the selected dates and types.")
    else:
        recent = recent.sort_values("timestamp", ascending=False)
        for event_date in sorted(recent["timestamp"].dt.date.unique(), reverse=True):
            st.markdown(f"### {event_date.strftime('%A, %B %d, %Y')}")
            daily_events = recent.loc[recent["timestamp"].dt.date == event_date]
            for _, event in daily_events.iterrows():
                metrics, details = event_display_data(event)
                display_timeline_event(
                    event["event_type"],
                    event["timestamp"].strftime("%H:%M"),
                    event["context"],
                    metrics,
                    details,
                )

with trends_tab:
    st.subheader("Measurements over time")
    trend_options = {
        "Heart rate (bpm)": "heart_rate",
        "Oxygen saturation (SpO₂ %)": "spo2",
        "Systolic pressure (mmHg)": "systolic",
        "Diastolic pressure (mmHg)": "diastolic",
        "Temperature (°C)": "temperature",
        "Calories burned (estimated)": "calories_burned_estimated",
        "Radiation exposure (mSv)": "radiation",
        "Sleep duration (hours)": "sleep_hours",
        "Mood (1–5)": "mood",
    }
    trend_label = st.selectbox("Indicator", options=list(trend_options))
    metric = trend_options[trend_label]
    trend_data = build_timeline_trend_data(recent, metric)
    if trend_data.empty:
        st.info("No values for this indicator in the selected date range.")
    else:
        st.scatter_chart(
            trend_data,
            x="timestamp",
            y="value",
            color="series",
            y_label=trend_label,
            height=320,
        )
        st.caption("Recorded measurement context and source")
        st.dataframe(
            trend_data[
                [
                    "timestamp",
                    "period_start",
                    "period_end",
                    "event_type",
                    "measurement",
                    "context",
                    "source",
                    "value",
                ]
            ],
            hide_index=True,
            width="stretch",
        )
