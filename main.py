from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

# Shared indicator rules and reusable UI components.
from components import (
    display_dashboard_timeline_event,
    display_indicator_card,
    load_indicator_styles,
)
from indicators import (
    INDICATOR_MESSAGES,
    WHY_MEASURE,
    has_resting_heart_rate_context,
    heart_rate_indicator,
    oxigen_saturation_indicator,
    pressure_indicator,
    temperature_indicator,
)
from storage import (
    init_db,
    load_data,
    load_timeline,
    save_activity,
    save_checkin,
    save_sleep_record,
    save_wellbeing,
)
st.set_page_config(
    page_title="Health Monitoring App",
    page_icon=":guardsman:",
    layout="wide",
    initial_sidebar_state="collapsed"
    )
#initialize the database
init_db()

#------------------------------------------------

#here we will create the main function to display the health indicators in a Streamlit application

def format_time_ago(timestamp):
    if pd.isna(timestamp):
        return "time unavailable"

    timestamp = pd.Timestamp(timestamp)
    now = pd.Timestamp.now(tz=timestamp.tz) if timestamp.tz else pd.Timestamp.now()
    elapsed_seconds = max(0, int((now - timestamp).total_seconds()))
    if elapsed_seconds < 60:
        return "just now"

    for seconds_per_unit, unit in ((86400, "day"), (3600, "hour"), (60, "minute")):
        amount = elapsed_seconds // seconds_per_unit
        if amount:
            plural = "" if amount == 1 else "s"
            return f"was {amount} {unit}{plural} ago"

    return "just now"


def last_data_value(data, column):
    values = data[column].dropna()
    return None if values.empty else values.iloc[-1]


def display_why_measure(key):
    explanation, source_label, source_url = WHY_MEASURE[key]
    with st.expander("Why track this?"):
        st.write(explanation)
        st.markdown(f"[{source_label}]({source_url})")


def timeline_event_summary(event):
    if event["event_type"] == "Health check-in":
        values = []
        for label, field, suffix in (
            ("Heart rate", "bpm", " bpm"),
            ("SpO₂", "spo2", "%"),
        ):
            value = event[field]
            if pd.notna(value):
                values.append(f"{label} {float(value):g}{suffix}")
        source = event["measurement_source"]
        source = (
            "Not recorded"
            if pd.isna(source) or not str(source).strip()
            else str(source)
        )
        values.append(f"Source: {source}")
        return " · ".join(values)

    if event["event_type"] == "Activity":
        description = event["description"]
        details = [] if pd.isna(description) else [str(description)]
        for label, field, source_field, suffix in (
            ("Average BPM", "bpm_average", "bpm_average_source", " bpm"),
            ("Maximum BPM", "bpm_max", "bpm_max_source", " bpm"),
            (
                "Calories burned (estimated)",
                "calories_burned_estimated",
                "calories_source",
                " kcal",
            ),
        ):
            value = event[field]
            if pd.notna(value):
                source = event[source_field]
                source = (
                    "source not recorded"
                    if pd.isna(source) or not str(source).strip()
                    else str(source)
                )
                details.append(f"{label}: {float(value):g}{suffix} · {source}")
        return " · ".join(details)

    if event["event_type"] == "Well-being check-in":
        mood = event["mood"]
        return f"Self-reported mood {int(mood)}/5" if pd.notna(mood) else ""

    if event["event_type"] == "Sleep":
        hours = event["sleep_hours"]
        return f"Duration from recorded period: {float(hours):g} hours" if pd.notna(hours) else ""

    return ""


def main():
    navigation = st.columns(3)
    with navigation[0]:
        st.page_link("main.py", label="Dashboard")
    with navigation[1]:
        st.page_link("pages/timeline.py", label="Timeline")
    with navigation[2]:
        st.page_link("pages/calendar.py", label="Calendar")
    st.divider()

    load_indicator_styles()
    with st.container(border=True, key="dashboard-container"):
        st.title("Health Monitoring App")
        left_panel, right_panel = st.columns([1.1, 0.9], gap="large")
        df = load_data()
        timeline = load_timeline()
        spo2 = last_data_value(df, "spo2")
        bpm = last_data_value(df, "bpm")
        systolic = last_data_value(df, "systolic")
        diastolic = last_data_value(df, "diastolic")
        temperature = last_data_value(df, "temperature")
        latest_bpm_rows = df.dropna(subset=["bpm"]).sort_values("timestamp")
        latest_bpm = latest_bpm_rows.iloc[-1] if not latest_bpm_rows.empty else None

        with left_panel:
            st.header("Health indicators")
            st.caption(
                "Range labels use generic prototype references, not clinical "
                "thresholds or NASA protocols."
            )
            if not df.empty:
                latest_check = df["timestamp"].max()
                st.caption(f"Last health check {format_time_ago(latest_check)}")
            else:
                st.caption("No health check has been recorded yet.")

            with st.container(border=True, key="health-indicators-panel"):
                for values in (
                    (
                        (
                            "Oxygen",
                            spo2,
                            lambda value: f"{value:g}%",
                            oxigen_saturation_indicator,
                            "oxygen",
                        ),
                        (
                            "Heart rate",
                            bpm,
                            lambda value: f"{value:g} bpm",
                            heart_rate_indicator,
                            "heart_rate",
                        ),
                    ),
                    (
                        (
                            "Blood pressure (mmHg)",
                            (systolic, diastolic),
                            lambda value: f"{value[0]:g}/{value[1]:g}",
                            lambda value: pressure_indicator(*value),
                            "blood_pressure",
                        ),
                        (
                            "Temperature",
                            temperature,
                            lambda value: f"{value:.1f} °C",
                            temperature_indicator,
                            "temperature",
                        ),
                    ),
                ):
                    row = st.columns(2)
                    for column, (label, value, format_value, indicator, message_key) in zip(
                        row, values
                    ):
                        with column:
                            missing = (
                                any(item is None for item in value)
                                if isinstance(value, tuple)
                                else value is None
                            )
                            rest_context = (
                                latest_bpm is not None
                                and has_resting_heart_rate_context(
                                    latest_bpm["measurement_context"]
                                )
                            )
                            if missing:
                                display_indicator_card(
                                    label,
                                    "—",
                                    None,
                                    None,
                                    INDICATOR_MESSAGES[message_key],
                                    WHY_MEASURE[message_key],
                                )
                            elif label == "Heart rate" and not rest_context:
                                display_indicator_card(
                                    label,
                                    format_value(value),
                                    None,
                                    None,
                                    INDICATOR_MESSAGES[message_key],
                                    WHY_MEASURE[message_key],
                                )
                            else:
                                color, status = indicator(value)
                                display_indicator_card(
                                    label,
                                    format_value(value),
                                    color,
                                    status,
                                    INDICATOR_MESSAGES[message_key],
                                    WHY_MEASURE[message_key],
                                )
                            if label == "Heart rate" and latest_bpm is not None:
                                bpm_context = latest_bpm["measurement_context"]
                                bpm_source = latest_bpm["measurement_source"]
                                bpm_context = (
                                    "Not recorded"
                                    if pd.isna(bpm_context) or not str(bpm_context).strip()
                                    else str(bpm_context)
                                )
                                bpm_source = (
                                    "Not recorded"
                                    if pd.isna(bpm_source) or not str(bpm_source).strip()
                                    else str(bpm_source)
                                )
                                st.caption(
                                    f"{bpm_context} · Source: {bpm_source} · "
                                    f"{latest_bpm['timestamp']:%Y-%m-%d %H:%M}"
                                )

            if df.empty:
                st.caption("The trend chart will appear after the first health check.")
            else:
                indicators = {
                    "Oxygen (SpO₂ %)": "spo2",
                    "Heart rate (bpm)": "bpm",
                    "Systolic (mmHg)": "systolic",
                    "Diastolic (mmHg)": "diastolic",
                    "Temperature (°C)": "temperature",
                    "Sleep (hours)": "sleep_hours",
                }
                indicator_name = st.selectbox(
                    "Trend",
                    options=list(indicators.keys()),
                    label_visibility="collapsed",
                )
                column = indicators[indicator_name]
                chart = (
                    df[
                        [
                            "timestamp",
                            column,
                            "measurement_context",
                            "measurement_source",
                        ]
                    ]
                    .dropna(subset=[column])
                    .sort_values("timestamp")
                    .rename(columns={column: "value"})
                )
                if chart.empty:
                    st.caption("No values are available for this trend yet.")
                else:
                    chart["context"] = chart["measurement_context"].fillna(
                        "Not recorded"
                    )
                    st.scatter_chart(
                        chart,
                        x="timestamp",
                        y="value",
                        color="context",
                        y_label=indicator_name,
                        height=240,
                    )
                    latest_point = chart.iloc[-1]
                    point_source = latest_point["measurement_source"]
                    point_source = (
                        "Not recorded"
                        if pd.isna(point_source) or not str(point_source).strip()
                        else str(point_source)
                    )
                    st.caption(
                        f"Latest point: {latest_point['timestamp']:%Y-%m-%d %H:%M} · "
                        f"{latest_point['context']} · Source: {point_source}"
                    )

            st.divider()
            st.subheader("Recent timeline")
            if timeline.empty:
                st.caption("Saved records will appear here.")
            else:
                st.caption(f"{len(timeline)} saved records · showing the latest 3")
                for _, event in timeline.head(3).iterrows():
                    display_dashboard_timeline_event(
                        event["event_type"],
                        format_time_ago(event["timestamp"]),
                        event["context"],
                        timeline_event_summary(event),
                    )
                st.page_link("pages/timeline.py", label="Open full timeline")

        with right_panel:
            st.subheader("Health records")
            st.caption("Records are saved locally and appear in the Timeline.")
            checkin_tab, activity_tab, wellbeing_tab, sleep_tab = st.tabs(
                ["Check-in", "Activity", "Well-being", "Sleep"]
            )

            with checkin_tab:
                with st.form("health_check_form"):
                    check_bpm = st.number_input(
                        "Heart rate (bpm)", min_value=30, max_value=200,
                        value=None,
                        key="heart_rate_input"
                    )
                    check_spo2 = st.number_input(
                        "SpO₂ (%)", min_value=70, max_value=100,
                        value=None,
                        key="spo2_input"
                    )
                    pressure_columns = st.columns(2)
                    with pressure_columns[0]:
                        check_systolic = st.number_input(
                            "Systolic (mmHg)", min_value=80, max_value=200,
                            value=None,
                            key="systolic_input"
                        )
                    with pressure_columns[1]:
                        check_diastolic = st.number_input(
                            "Diastolic (mmHg)", min_value=50, max_value=150,
                            value=None,
                            key="diastolic_input"
                        )
                    check_temperature = st.number_input(
                        "Temperature (°C)", min_value=30.0, max_value=45.0,
                        value=None,
                        step=0.1, key="temperature_input"
                    )
                    context_choice = st.selectbox(
                        "Measurement context",
                        ["At rest", "During activity", "After exercise", "Other"],
                        key="checkin_context"
                    )
                    other_context = st.text_input(
                        "Describe other context (optional)",
                        key="checkin_other_context"
                    )
                    measurement_source = st.selectbox(
                        "Measurement source",
                        ["Sensor", "Reported by user", "Estimated"],
                        key="checkin_source"
                    )
                    check_radiation = st.number_input(
                        "Radiation dose in mSv (reference period not recorded)",
                        min_value=0.0, max_value=1000.0, value=None, step=0.1,
                        key="checkin_radiation"
                    )
                    st.caption(
                        "Recorded with its timestamp and source; no exposure limit "
                        "or alert is applied."
                    )
                    radiation_source_choice = st.selectbox(
                        "Radiation data source",
                        ["Not provided", "Sensor", "Reported by user", "Estimated"],
                        key="checkin_radiation_source"
                    )
                    symptoms = st.text_area(
                        "Symptoms (optional)", height=68, key="checkin_symptoms"
                    )
                    checkin_observation = st.text_area(
                        "Observation (optional)", height=68, key="checkin_observation"
                    )
                    checkin_submitted = st.form_submit_button("Save check-in", type="primary")
                if checkin_submitted:
                    required_readings = (
                        check_bpm,
                        check_spo2,
                        check_systolic,
                        check_diastolic,
                        check_temperature,
                    )
                    if any(value is None for value in required_readings):
                        st.error("Enter all required health measurements before saving.")
                    else:
                        context = context_choice
                        if context_choice == "Other" and other_context.strip():
                            context = f"Other: {other_context.strip()}"
                        save_checkin({
                            "bpm": check_bpm,
                            "spo2": check_spo2,
                            "systolic": check_systolic,
                            "diastolic": check_diastolic,
                            "temperature": check_temperature,
                            "measurement_context": context,
                            "measurement_source": measurement_source,
                            "symptoms": symptoms.strip() or None,
                            "observation": checkin_observation.strip() or None,
                            "radiation": check_radiation,
                            "radiation_source": (
                                None if check_radiation is None
                                or radiation_source_choice == "Not provided"
                                else radiation_source_choice
                            ),
                        })
                        st.success("Health check-in saved.")

            with activity_tab:
                display_why_measure("activity")
                with st.form("activity_form"):
                    activity_type = st.text_input("Activity type", key="activity_type")
                    activity_description = st.text_area(
                        "Activity description", height=80, key="activity_description"
                    )
                    activity_now = datetime.now().replace(second=0, microsecond=0)
                    activity_start_default = activity_now - timedelta(hours=1)
                    activity_start = st.columns(2)
                    with activity_start[0]:
                        activity_start_date = st.date_input(
                            "Start date", value=activity_start_default.date(),
                            key="activity_start_date"
                        )
                        activity_start_time = st.time_input(
                            "Start time", value=activity_start_default.time(),
                            key="activity_start_time"
                        )
                    with activity_start[1]:
                        activity_end_date = st.date_input(
                            "End date", value=activity_now.date(),
                            key="activity_end_date"
                        )
                        activity_end_time = st.time_input(
                            "End time", value=activity_now.time(),
                            key="activity_end_time"
                        )
                    activity_intensity = st.number_input(
                        "Perceived intensity (optional, 1–10)",
                        min_value=1, max_value=10, value=None, step=1,
                        key="activity_intensity"
                    )
                    activity_bpm_average = st.number_input(
                        "Average BPM (optional)", min_value=30, max_value=250,
                        value=None, key="activity_average_bpm"
                    )
                    activity_bpm_average_source = st.selectbox(
                        "Average BPM source",
                        ["Not provided", "Sensor", "Reported by user", "Estimated"],
                        key="activity_bpm_source"
                    )
                    activity_bpm_max = st.number_input(
                        "Maximum BPM (optional)", min_value=30, max_value=250,
                        value=None, key="activity_maximum_bpm"
                    )
                    activity_bpm_max_source = st.selectbox(
                        "Maximum BPM source",
                        ["Not provided", "Sensor", "Reported by user", "Estimated"],
                        key="activity_max_bpm_source"
                    )
                    activity_calories = st.number_input(
                        "Estimated calories burned (optional)",
                        min_value=0.0, max_value=10000.0, value=None, step=1.0,
                        key="activity_calories"
                    )
                    activity_calories_source = st.selectbox(
                        "Calories estimate source",
                        ["Not provided", "Sensor", "Reported by user", "Estimated"],
                        key="activity_calories_source"
                    )
                    activity_observation = st.text_area(
                        "Observation (optional)", height=68,
                        key="activity_observation"
                    )
                    activity_submitted = st.form_submit_button(
                        "Save activity", type="primary"
                    )
                if activity_submitted:
                    activity_start_at = datetime.combine(
                        activity_start_date, activity_start_time
                    )
                    activity_end_at = datetime.combine(
                        activity_end_date, activity_end_time
                    )
                    if not activity_type.strip() or not activity_description.strip():
                        st.error("Enter an activity type and description.")
                    elif activity_end_at <= activity_start_at:
                        st.error("Activity end must be after its start.")
                    else:
                        save_activity({
                            "activity_type": activity_type,
                            "description": activity_description,
                            "start_at": activity_start_at.isoformat(),
                            "end_at": activity_end_at.isoformat(),
                            "intensity": activity_intensity,
                            "bpm_average": activity_bpm_average,
                            "bpm_average_source": (
                                None if activity_bpm_average is None
                                or activity_bpm_average_source == "Not provided"
                                else activity_bpm_average_source
                            ),
                            "bpm_max": activity_bpm_max,
                            "bpm_max_source": (
                                None if activity_bpm_max is None
                                or activity_bpm_max_source == "Not provided"
                                else activity_bpm_max_source
                            ),
                            "calories_burned_estimated": activity_calories,
                            "calories_source": (
                                None if activity_calories is None
                                or activity_calories_source == "Not provided"
                                else activity_calories_source
                            ),
                            "observation": activity_observation.strip() or None,
                        })
                        st.success("Activity saved.")

            with wellbeing_tab:
                display_why_measure("wellbeing")
                with st.form("wellbeing_form"):
                    mood = st.radio(
                        "Mood",
                        [1, 2, 3, 4, 5],
                        format_func=lambda value: {
                            1: "1 — Very bad",
                            2: "2 — Bad",
                            3: "3 — Neutral",
                            4: "4 — Good",
                            5: "5 — Very good",
                        }[value],
                        horizontal=True,
                        key="wellbeing_mood"
                    )
                    stress_choice = st.selectbox(
                        "Stress level (optional)",
                        ["Not provided", "Low", "Moderate", "High"],
                        key="wellbeing_stress"
                    )
                    isolation_choice = st.selectbox(
                        "Feeling of isolation (optional)",
                        ["Not provided", "None", "Some", "Strong"],
                        key="wellbeing_isolation"
                    )
                    sleep_well_choice = st.selectbox(
                        "Did you sleep well? (optional)",
                        ["No response", "Yes", "No"],
                        key="wellbeing_sleep_quality"
                    )
                    wellbeing_note = st.text_area(
                        "Free note (optional)", height=68, key="wellbeing_note"
                    )
                    wellbeing_submitted = st.form_submit_button(
                        "Save well-being check-in", type="primary"
                    )
                if wellbeing_submitted:
                    save_wellbeing({
                        "mood": mood,
                        "stress": (
                            None if stress_choice == "Not provided" else stress_choice
                        ),
                        "isolation": (
                            None if isolation_choice == "Not provided" else isolation_choice
                        ),
                        "sleep_well": (
                            None if sleep_well_choice == "No response"
                            else sleep_well_choice == "Yes"
                        ),
                        "note": wellbeing_note.strip() or None,
                    })
                    st.success("Well-being check-in saved.")

            with sleep_tab:
                display_why_measure("sleep")
                with st.form("sleep_form"):
                    sleep_now = datetime.now().replace(second=0, microsecond=0)
                    sleep_start_default = sleep_now - timedelta(hours=8)
                    sleep_period = st.columns(2)
                    with sleep_period[0]:
                        sleep_start_date = st.date_input(
                            "Sleep start date", value=sleep_start_default.date(),
                            key="sleep_start_date"
                        )
                        sleep_start_time = st.time_input(
                            "Sleep start time", value=sleep_start_default.time(),
                            key="sleep_start_time"
                        )
                    with sleep_period[1]:
                        sleep_end_date = st.date_input(
                            "Sleep end date", value=sleep_now.date(),
                            key="sleep_end_date"
                        )
                        sleep_end_time = st.time_input(
                            "Sleep end time", value=sleep_now.time(),
                            key="sleep_end_time"
                        )
                    sleep_quality = st.selectbox(
                        "Perceived sleep quality (optional)",
                        ["Not provided", "Very poor", "Poor", "Fair", "Good", "Very good"],
                        key="sleep_quality"
                    )
                    sleep_interruptions = st.text_area(
                        "Interruptions (optional)", height=68,
                        key="sleep_interruptions"
                    )
                    sleep_observation = st.text_area(
                        "Observation (optional)", height=68,
                        key="sleep_observation"
                    )
                    sleep_submitted = st.form_submit_button(
                        "Save sleep record", type="primary"
                    )
                if sleep_submitted:
                    sleep_start_at = datetime.combine(sleep_start_date, sleep_start_time)
                    sleep_end_at = datetime.combine(sleep_end_date, sleep_end_time)
                    if sleep_end_at <= sleep_start_at:
                        st.error("Sleep end must be after its start.")
                    else:
                        save_sleep_record({
                            "start_at": sleep_start_at.isoformat(),
                            "end_at": sleep_end_at.isoformat(),
                            "quality": (
                                None if sleep_quality == "Not provided" else sleep_quality
                            ),
                            "interruptions": sleep_interruptions.strip() or None,
                            "observation": sleep_observation.strip() or None,
                        })
                        st.success("Sleep record saved.")

if __name__ == "__main__":
    main() 