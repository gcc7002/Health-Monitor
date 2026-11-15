import streamlit as st

from html import escape


# Import database read and initialization functions.
from storage import init_db, load_data, get_last_value
st.set_page_config(
    page_title="Health Monitoring App",
    page_icon=":guardsman:",
    layout="wide",
    initial_sidebar_state="expanded"
    )
#initialize the database
init_db()

#Here we pick the values from the last check

spo2: float = get_last_value("spo2")
bpm: float = get_last_value("bpm")
systolic: float = get_last_value("systolic")
diastolic: float = get_last_value("diastolic")
temperature:float = get_last_value("temperature")
hydration:int  =0
calories:int =0
sleep_hours:float = get_last_value("sleep_hours")
radiation:int =0


#These functions return the display color and status for each health indicator.

colors = {"normal": "green", "warning": "orange", "critical": "red"}

def oxigen_saturation_indicator(value):
    if value >= 95:
        return colors["normal"], "normal"
    elif 90 <= value < 95:
        return colors["warning"], "warning"
    else:
        return colors["critical"], "critical"

def heart_rate_indicator(value):
    if 60 <= value <= 100:
        return colors["normal"], "normal"
    elif 50 <= value < 60 or 100 < value <= 110:
        return colors["warning"], "warning"
    else:
        return colors["critical"], "critical"

def pressure_indicator(systolic, diastolic):
    if systolic >= 140 or diastolic >= 90:
        return colors["critical"], "critical"
    elif systolic < 120 and diastolic < 80:
        return colors["normal"], "normal"
    elif (120 <= systolic < 130) and diastolic < 80:
        return colors["warning"], "warning"
    elif (130 <= systolic < 140) or (80 <= diastolic < 90):
        return colors["warning"], "warning"
    else:
        return colors["critical"], "critical"

def temperature_indicator(value):
    if 36.1 <= value <= 37.2:
        return colors["normal"], "normal"
    elif 37.2 < value <= 38.0:
        return colors["warning"], "warning"
    else:
        return colors["critical"], "critical"

def hydration_indicator(value):
    if value >= 60:
        return colors["normal"], "normal"
    elif 50 <= value < 60:
        return colors["warning"], "warning"
    else:
        return colors["critical"], "critical"

def calories_indicator(value):
    if 2000 <= value <= 2500:
        return colors["normal"], "normal"
    elif 1500 <= value < 2000 or 2500 < value <= 3000:
        return colors["warning"], "warning"
    else:
        return colors["critical"], "critical"

def sleep_hours_indicator(value):
    if 7 <= value <= 9:
        return colors["normal"], "normal"
    elif 6 <= value < 7 or 9 < value <= 10:
        return colors["warning"], "warning"
    else:
        return colors["critical"], "critical"

def radiation_indicator(value):
    if value < 1.0:
        return colors["normal"], "normal"
    elif 1.0 <= value < 3.0:
        return colors["warning"], "warning"
    else:
        return colors["critical"], "critical"

def display_indicator_status(color, status, messages):
    st.markdown(
        f"<span style='color: {color};'>Status: {status.capitalize()}</span>",
        unsafe_allow_html=True
    )
    message = messages[status]
    role = "alert" if status == "critical" else "status"
    st.markdown(
        f"<div class='indicator-feedback indicator-feedback-{status}' "
        f"title='{escape(message, quote=True)}' role='{role}'>"
        f"<span>{escape(message)}</span></div>",
        unsafe_allow_html=True
    )

def display_indicator_card(label, value, color, status, messages):
    with st.container(height=190, border=True):
        st.metric(label=label, value=value)
        display_indicator_status(color, status, messages)


#------------------------------------------------

#here we will create the main function to display the health indicators in a Streamlit application

def main():
    st.title("Health Monitoring App")
    navigation = st.columns(3)
    with navigation[0]:
        st.page_link("main.py", label="Dashboard")
    with navigation[1]:
        st.page_link("pages/timeline.py", label="Timeline")
    with navigation[2]:
        st.page_link("pages/calendar.py", label="Calendar")
    st.divider()

    st.markdown(
        """
        <style>
        .st-key-health-indicators-panel {
            padding: 0.75rem !important;
        }
        div[data-testid="stMetricLabel"] p {
            font-size: 0.8rem;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.35rem;
        }
        .indicator-feedback {
            height: 3.25rem;
            width: 100%;
            box-sizing: border-box;
            overflow: hidden;
            display: flex;
            align-items: center;
            padding: 0.5rem;
            border-radius: 0.35rem;
            font-size: 0.75rem;
            line-height: 1.2;
        }
        .indicator-feedback span {
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 2;
            overflow: hidden;
        }
        .indicator-feedback-normal {
            background: rgba(0, 128, 0, 0.1);
            border-left: 0.25rem solid green;
        }
        .indicator-feedback-warning {
            background: rgba(255, 165, 0, 0.12);
            border-left: 0.25rem solid orange;
        }
        .indicator-feedback-critical {
            background: rgba(255, 0, 0, 0.1);
            border-left: 0.25rem solid red;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    left_panel, right_panel = st.columns([1, 1])

    with left_panel:
        st.header("Health Indicators")
        df = load_data()
        if not df.empty:
            st.caption(f"Last health check: {df.iloc[-1]['timestamp']}")

        has_readings = all(
            value is not None
            for value in (spo2, bpm, systolic, diastolic, temperature, sleep_hours)
        )
        if not has_readings:
            st.info("No health check data yet. Complete a check to populate the dashboard.")
        else:
            with st.container(border=True, key="health-indicators-panel"):
                row1 = st.columns(4)
                with row1[0]:
                    color, status = oxigen_saturation_indicator(spo2)
                    display_indicator_card("Oxygen", f"{spo2:g}%", color, status, {
                        "normal": "Oxygen saturation is within the normal range.",
                        "warning": "Oxygen saturation is slightly low. Monitor your health.",
                        "critical": "Low oxygen saturation! Seek medical attention."
                    })
                with row1[1]:
                    color, status = heart_rate_indicator(bpm)
                    display_indicator_card("Heart Rate", f"{bpm:g} bpm", color, status, {
                        "normal": "Heart rate is within the normal range.",
                        "warning": "Heart rate is slightly abnormal. Monitor your health.",
                        "critical": "Abnormal heart rate! Seek medical attention."
                    })
                with row1[2]:
                    color, status = pressure_indicator(systolic, diastolic)
                    display_indicator_card("Blood Pressure", f"{systolic:g}/{diastolic:g}", color, status, {
                        "normal": "Blood pressure is within the normal range.",
                        "warning": "Blood pressure is slightly elevated. Monitor your health.",
                        "critical": "High blood pressure! Seek medical attention."
                    })
                with row1[3]:
                    color, status = temperature_indicator(temperature)
                    display_indicator_card("Temperature", f"{temperature:.1f} °C", color, status, {
                        "normal": "Body temperature is within the normal range.",
                        "warning": "Body temperature is slightly elevated. Monitor your health.",
                        "critical": "Abnormal body temperature! Seek medical attention."
                    })

                row2 = st.columns(4)
                with row2[0]:
                    color, status = hydration_indicator(hydration)
                    display_indicator_card("Hydration", f"{hydration}%", color, status, {
                        "normal": "Hydration level is within the normal range.",
                        "warning": "Hydration level is low. Increase water intake.",
                        "critical": "Hydration level is critically low. Seek medical attention."
                    })
                with row2[1]:
                    color, status = calories_indicator(calories)
                    display_indicator_card("Calories", f"{calories} kcal", color, status, {
                        "normal": "Calorie intake is within the target range.",
                        "warning": "Calorie intake is outside the target range. Monitor your intake.",
                        "critical": "Calorie intake is far outside the target range."
                    })
                with row2[2]:
                    color, status = sleep_hours_indicator(sleep_hours)
                    display_indicator_card("Sleep", f"{sleep_hours:.1f} hrs", color, status, {
                        "normal": "Sleep duration is within the normal range.",
                        "warning": "Sleep duration is outside the recommended range. Monitor your sleep.",
                        "critical": "Insufficient or excessive sleep duration. Review your sleep habits."
                    })
                with row2[3]:
                    color, status = radiation_indicator(radiation)
                    display_indicator_card("Radiation", f"{radiation} mSv", color, status, {
                        "normal": "Radiation exposure is within the normal range.",
                        "warning": "Radiation exposure is slightly high. Monitor your exposure.",
                        "critical": "High radiation exposure! Seek medical attention."
                    })

        if df.empty:
            st.caption("The trend chart will appear after the first health check.")
        else:
            indicators = {
                "Oxygen (SpO₂ %)": "spo2",
                "Heart Rate (bpm)": "bpm",
                "Systolic (mmHg)": "systolic",
                "Diastolic (mmHg)": "diastolic",
                "Temperature (°C)": "temperature",
                "Sleep (hours)": "sleep_hours"
            }
            indicator_name = st.selectbox(
                "Trend",
                options=list(indicators.keys()),
                label_visibility="collapsed"
            )
            column = indicators[indicator_name]
            chart = df[["timestamp", column]].dropna().sort_values("timestamp")
            st.line_chart(chart, x="timestamp", y=column, height=220)

    with right_panel:
        st.subheader("Health Records")
        st.caption("Form layout preview. Saving is not enabled yet.")
        checkin_tab, activity_tab, wellbeing_tab, sleep_tab = st.tabs(
            ["Check-in", "Activity", "Well-being", "Sleep"]
        )

        with checkin_tab:
            with st.form("health_check_form"):
                st.number_input(
                    "Heart rate (bpm)", min_value=30, max_value=200,
                    value=int(bpm) if bpm is not None else 70,
                    key="heart_rate_input"
                )
                st.number_input(
                    "SpO₂ (%)", min_value=70, max_value=100,
                    value=int(spo2) if spo2 is not None else 98,
                    key="spo2_input"
                )
                checkin_pressure = st.columns(2)
                with checkin_pressure[0]:
                    st.number_input(
                        "Systolic (mmHg)", min_value=80, max_value=200,
                        value=int(systolic) if systolic is not None else 120,
                        key="systolic_input"
                    )
                with checkin_pressure[1]:
                    st.number_input(
                        "Diastolic (mmHg)", min_value=50, max_value=150,
                        value=int(diastolic) if diastolic is not None else 80,
                        key="diastolic_input"
                    )
                st.number_input(
                    "Temperature (°C)", min_value=30.0, max_value=45.0,
                    value=temperature if temperature is not None else 37.0,
                    step=0.1, key="temperature_input"
                )
                st.selectbox(
                    "Measurement context",
                    ["At rest", "After exercise", "Other"],
                    key="checkin_context"
                )
                st.selectbox(
                    "Measurement source",
                    ["Sensor", "Reported by user", "Estimated"],
                    key="checkin_source"
                )
                st.text_area("Symptoms (optional)", key="checkin_symptoms")
                st.text_area("Observation (optional)", key="checkin_observation")
                st.form_submit_button("Save check-in", disabled=True)

        with activity_tab:
            with st.form("activity_form"):
                st.text_input("Activity type", key="activity_type")
                st.text_area("Activity description", key="activity_description")
                activity_start = st.columns(2)
                with activity_start[0]:
                    st.date_input("Start date", key="activity_start_date")
                    st.time_input("Start time", key="activity_start_time")
                with activity_start[1]:
                    st.date_input("End date", key="activity_end_date")
                    st.time_input("End time", key="activity_end_time")
                st.slider(
                    "Perceived intensity (optional)", 1, 10, value=5,
                    key="activity_intensity"
                )
                st.text_input(
                    "Average BPM (optional)", placeholder="e.g. 120",
                    key="activity_average_bpm"
                )
                st.selectbox(
                    "Average BPM source",
                    ["Not provided", "Sensor", "Reported by user", "Estimated"],
                    key="activity_bpm_source"
                )
                st.text_input(
                    "Maximum BPM (optional)", placeholder="e.g. 150",
                    key="activity_maximum_bpm"
                )
                st.selectbox(
                    "Maximum BPM source",
                    ["Not provided", "Sensor", "Reported by user", "Estimated"],
                    key="activity_max_bpm_source"
                )
                st.text_input(
                    "Estimated calories burned (optional)",
                    placeholder="Calories burned, not consumed",
                    key="activity_calories"
                )
                st.selectbox(
                    "Calories source",
                    ["Not provided", "Sensor", "Reported by user", "Estimated"],
                    key="activity_calories_source"
                )
                st.text_area("Observation (optional)", key="activity_observation")
                st.form_submit_button("Save activity", disabled=True)

        with wellbeing_tab:
            with st.form("wellbeing_form"):
                st.radio(
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
                st.selectbox(
                    "Stress level (optional)",
                    ["Not provided", "Low", "Moderate", "High"],
                    key="wellbeing_stress"
                )
                st.selectbox(
                    "Feeling of isolation (optional)",
                    ["Not provided", "None", "Some", "Strong"],
                    key="wellbeing_isolation"
                )
                st.selectbox(
                    "Did you sleep well? (optional)",
                    ["No response", "Yes", "No"],
                    key="wellbeing_sleep_quality"
                )
                st.text_area("Free note (optional)", key="wellbeing_note")
                st.form_submit_button("Save well-being check-in", disabled=True)

        with sleep_tab:
            with st.form("sleep_form"):
                sleep_start = st.columns(2)
                with sleep_start[0]:
                    st.date_input("Sleep start date", key="sleep_start_date")
                    st.time_input("Sleep start time", key="sleep_start_time")
                with sleep_start[1]:
                    st.date_input("Sleep end date", key="sleep_end_date")
                    st.time_input("Sleep end time", key="sleep_end_time")
                st.selectbox(
                    "Perceived sleep quality (optional)",
                    ["Not provided", "Very poor", "Poor", "Fair", "Good", "Very good"],
                    key="sleep_quality"
                )
                st.text_area(
                    "Interruptions (optional)", key="sleep_interruptions"
                )
                st.text_area("Observation (optional)", key="sleep_observation")
                st.form_submit_button("Save sleep record", disabled=True)

        with st.container(border=True, height=140):
            st.caption("Reserved for another feature.")


if __name__ == "__main__":
    main() 