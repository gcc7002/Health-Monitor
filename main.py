import streamlit as st
import random
from html import escape

st.set_page_config(
    page_title="Health Monitoring App",
    page_icon=":guardsman:",
    layout="wide",
    initial_sidebar_state="expanded"
    )

#Just to simulate the values to check the results of the indicators

spo2 = random.randint(85, 100)  # Simulated oxygen saturation value
bpm = random.randint(40, 120)  # Simulated heart rate value
systolic = random.randint(90, 160)  # Simulated systolic blood pressure value
diastolic = random.randint(60, 100)  # Simulated diastolic blood pressure value
temperature = random.uniform(35.0, 40.0)  # Simulated body temperature value
hydration = random.randint(40, 100)  # Simulated hydration level value
calories = random.randint(1500, 3000)  # Simulated calorie intake value
sleep_hours = random.uniform(4.0, 10.0)  # Simulated sleep hours value
radiation = random.uniform(0.0, 5.0)  # Simulated radiation exposure value


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
    with st.container(height=360, border=True):
        st.metric(label=label, value=value)
        display_indicator_status(color, status, messages)

#------------------------------------------------

#here we will create the main function to display the health indicators in a Streamlit application

def main():
    st.title("Health Monitoring App")
    st.divider()

    # Health Indicators Section
    st.header("Health Indicators")
    st.markdown(
        """
        <style>
        .st-key-health-indicators-panel {
            padding: 1.25rem !important;
        }
        .indicator-feedback {
            height: 8rem;
            width: 100%;
            box-sizing: border-box;
            overflow: hidden;
            display: flex;
            align-items: center;
            padding: 0.75rem;
            border-radius: 0.5rem;
        }
        .indicator-feedback span {
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 4;
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
    left_panel, _ = st.columns([1, 1])
    with left_panel:
        with st.container(border=True, key="health-indicators-panel"):
            row1 = st.columns(4)
            with row1[0]:
                color, status = oxigen_saturation_indicator(spo2)
                display_indicator_card("Oxigen saturation", spo2, color, status, {
                    "normal": "Oxygen saturation is within the normal range.",
                    "warning": "Oxygen saturation is slightly low. Monitor your health.",
                    "critical": "Low oxygen saturation! Seek medical attention."
                })
            with row1[1]:
                color, status = heart_rate_indicator(bpm)
                display_indicator_card("Heart Rate", bpm, color, status, {
                    "normal": "Heart rate is within the normal range.",
                    "warning": "Heart rate is slightly abnormal. Monitor your health.",
                    "critical": "Abnormal heart rate! Seek medical attention."
                })
            with row1[2]:
                # Simulated blood pressure values
                systolic = random.randint(90, 160)
                diastolic = random.randint(60, 100)
                color, status = pressure_indicator(systolic, diastolic)
                display_indicator_card("Blood Pressure", f"{systolic}/{diastolic}", color, status, {
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
                display_indicator_card("Hydration Level", f"{hydration}%", color, status, {
                    "normal": "Hydration level is within the normal range.",
                    "warning": "Hydration level is low. Increase water intake.",
                    "critical": "Hydration level is critically low. Seek medical attention."
                })
            with row2[1]:
                color, status = calories_indicator(calories)
                display_indicator_card("Calorie Intake", f"{calories} kcal", color, status, {
                    "normal": "Calorie intake is within the target range.",
                    "warning": "Calorie intake is outside the target range. Monitor your intake.",
                    "critical": "Calorie intake is far outside the target range."
                })
            with row2[2]:
                color, status = sleep_hours_indicator(sleep_hours)
                display_indicator_card("Sleep Hours", f"{sleep_hours:.1f} hrs", color, status, {
                    "normal": "Sleep duration is within the normal range.",
                    "warning": "Sleep duration is outside the recommended range. Monitor your sleep.",
                    "critical": "Insufficient or excessive sleep duration. Review your sleep habits."
                })
            with row2[3]:
                color, status = radiation_indicator(radiation)
                display_indicator_card("Radiation Exposure", f"{radiation:.2f} mSv", color, status, {
                    "normal": "Radiation exposure is within the normal range.",
                    "warning": "Radiation exposure is slightly high. Monitor your exposure.",
                    "critical": "High radiation exposure! Seek medical attention."
                })
    if st.button("health check"):
        pass

if __name__ == "__main__":
    main() 