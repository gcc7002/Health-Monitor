import streamlit as st
import random

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
    if status == "critical":
        st.error(message)
    elif status == "warning":
        st.warning(message)
    else:
        st.success(message)

#------------------------------------------------

#here we will create the main function to display the health indicators in a Streamlit application

def main():
    st.title("Health Monitoring App")
    st.divider()

    # Health Indicators Section
    st.header("Health Indicators")
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        color, status = oxigen_saturation_indicator(spo2)
        st.metric(label="Oxigen saturation", value=spo2)
        display_indicator_status(color, status, {
            "normal": "Oxygen saturation is within the normal range.",
            "warning": "Oxygen saturation is slightly low. Monitor your health.",
            "critical": "Low oxygen saturation! Seek medical attention."
        })
    with col2:
        color, status = heart_rate_indicator(bpm)
        st.metric(label="Heart Rate", value=bpm)
        display_indicator_status(color, status, {
            "normal": "Heart rate is within the normal range.",
            "warning": "Heart rate is slightly abnormal. Monitor your health.",
            "critical": "Abnormal heart rate! Seek medical attention."
        })
    with col3:
        # Simulated blood pressure values
        systolic = random.randint(90, 160)
        diastolic = random.randint(60, 100)
        color, status = pressure_indicator(systolic, diastolic)
        st.metric(label="Blood Pressure", value=f"{systolic}/{diastolic}")
        display_indicator_status(color, status, {
            "normal": "Blood pressure is within the normal range.",
            "warning": "Blood pressure is slightly elevated. Monitor your health.",
            "critical": "High blood pressure! Seek medical attention."
        })
    with col4:
        color, status = temperature_indicator(temperature)
        st.metric(label="Temperature", value=f"{temperature:.1f} °C")
        display_indicator_status(color, status, {
            "normal": "Body temperature is within the normal range.",
            "warning": "Body temperature is slightly elevated. Monitor your health.",
            "critical": "Abnormal body temperature! Seek medical attention."
        })
    with col5:
        color, status = hydration_indicator(hydration)
        st.metric(label="Hydration Level", value=f"{hydration}%")
        display_indicator_status(color, status, {
            "normal": "Hydration level is within the normal range.",
            "warning": "Hydration level is low. Increase water intake.",
            "critical": "Hydration level is critically low. Seek medical attention."
        })
    with col6:
        color, status = calories_indicator(calories)
        st.metric(label="Calorie Intake", value=f"{calories} kcal")
        display_indicator_status(color, status, {
            "normal": "Calorie intake is within the target range.",
            "warning": "Calorie intake is outside the target range. Monitor your intake.",
            "critical": "Calorie intake is far outside the target range."
        })

    with col7:
        color, status = sleep_hours_indicator(sleep_hours)
        st.metric(label="Sleep Hours", value=f"{sleep_hours:.1f} hrs")
        display_indicator_status(color, status, {
            "normal": "Sleep duration is within the normal range.",
            "warning": "Sleep duration is outside the recommended range. Monitor your sleep.",
            "critical": "Insufficient or excessive sleep duration. Review your sleep habits."
        })
    with col8:
        color, status = radiation_indicator(radiation)
        st.metric(label="Radiation Exposure", value=f"{radiation:.2f} mSv")
        display_indicator_status(color, status, {
            "normal": "Radiation exposure is within the normal range.",
            "warning": "Radiation exposure is slightly high. Monitor your exposure.",
            "critical": "High radiation exposure! Seek medical attention."
        })

if __name__ == "__main__":
    main() 