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


#These functions will return the color based on the value of the health indicators

colors = {"normal": "green", "warning": "orange", "critical": "red"}

def oxigen_saturation_indicator(value):
    if value >= 95:
        return colors["normal"]
    elif 90 <= value < 95:
        return colors["warning"]
    else:
        return colors["critical"]

def heart_rate_indicator(value):
    if 60 <= value <= 100:
        return colors["normal"]
    elif 50 <= value < 60 or 100 < value <= 110:
        return colors["warning"]
    else:
        return colors["critical"]

def pressure_indicator(systolic, diastolic):
    if systolic < 120 and diastolic < 80:
        return colors["normal"]
    elif (120 <= systolic < 130) and diastolic < 80:
        return colors["warning"]
    elif (130 <= systolic < 140) or (80 <= diastolic < 90):
        return colors["warning"]
    else:
        return colors["critical"]

def temperature_indicator(value):
    if 36.1 <= value <= 37.2:
        return colors["normal"]
    elif 37.3 <= value <= 38.0:
        return colors["warning"]
    else:
        return colors["critical"]

def hydration_indicator(value):
    if value >= 60:
        return colors["normal"]
    elif 50 <= value < 60:
        return colors["warning"]
    else:
        return colors["critical"]

def calories_indicator(value):
    if 2000 <= value <= 2500:
        return colors["normal"]
    elif 1500 <= value < 2000 or 2500 < value <= 3000:
        return colors["warning"]
    else:
        return colors["critical"]

def sleep_hours_indicator(value):
    if 7 <= value <= 9:
        return colors["normal"]
    elif 6 <= value < 7 or 9 < value <= 10:
        return colors["warning"]
    else:
        return colors["critical"]

def radiation_indicator(value):
    if value < 1.0:
        return colors["normal"]
    elif 1.0 <= value < 3.0:
        return colors["warning"]
    else:
        return colors["critical"]

#------------------------------------------------

#here we will create the main function to display the health indicators in a Streamlit application

def main():
    st.title("Health Monitoring App")
    st.divider()

    # Health Indicators Section
    st.header("Health Indicators")
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        st.metric(label="Oxigen saturation", value = spo2, delta_color=oxigen_saturation_indicator(spo2))
        st.markdown(
            f"<span style='color: {oxigen_saturation_indicator(spo2)};'>"
            f"Status: {oxigen_saturation_indicator(spo2).capitalize()}</span>",
            unsafe_allow_html=True
        )
        if spo2 < 90:
            st.error("Warning: Low oxygen saturation! Seek medical attention.")
        elif spo2 < 95 and spo2 >= 90:
            st.warning("Info: Oxygen saturation is slightly low. Monitor your health.")
        else:
            st.success("Oxygen saturation is within the normal range.")
    with col2:
        st.metric(label="Heart Rate", value = bpm, delta_color=heart_rate_indicator(bpm))
        st.markdown(
            f"<span style='color: {heart_rate_indicator(bpm)};'>"
            f"Status: {heart_rate_indicator(bpm).capitalize()}</span>",
            unsafe_allow_html=True
        )
        if bpm < 50 or bpm > 110:
            st.error("Warning: Abnormal heart rate! Seek medical attention.")
        elif (50 <= bpm < 60) or (100 < bpm <= 110):
            st.warning("Info: Heart rate is slightly abnormal. Monitor your health.")
        else:
            st.success("Heart rate is within the normal range.")
    with col3:
        # Simulated blood pressure values
        systolic = random.randint(90, 160)
        diastolic = random.randint(60, 100)
        st.metric(label="Blood Pressure", value=f"{systolic}/{diastolic}", delta_color=pressure_indicator(systolic, diastolic))
        st.markdown(
            f"<span style='color: {pressure_indicator(systolic, diastolic)};'>"
            f"Status: {pressure_indicator(systolic, diastolic).capitalize()}</span>",
            unsafe_allow_html=True
        )
        if systolic >= 140 or diastolic >= 90:
            st.error("Warning: High blood pressure! Seek medical attention.")
        elif (130 <= systolic < 140) or (80 <= diastolic < 90):
            st.warning("Info: Blood pressure is slightly high. Monitor your health.")
        elif (120 <= systolic < 130) and diastolic < 80:
            st.warning("Info: Blood pressure is slightly elevated. Monitor your health.")
        else:
            st.success("Blood pressure is within the normal range.")
    with col4:
        st.metric(label="Temperature", value = f"{temperature:.1f} °C", delta_color=temperature_indicator(temperature))
        st.markdown(
            f"<span style='color: {temperature_indicator(temperature)};'>"
            f"Status: {temperature_indicator(temperature).capitalize()}</span>",
            unsafe_allow_html=True
        )
        if temperature < 36.1 or temperature > 37.2:
            st.error("Warning: Abnormal body temperature! Seek medical attention.")
        elif 37.3 <= temperature <= 38.0:
            st.warning("Info: Body temperature is slightly elevated. Monitor your health.")
        else:
            st.success("Body temperature is within the normal range.")
    with col5:
        st.metric(label="Hydration Level", value = f"{hydration}%", delta_color=hydration_indicator(hydration))
        st.markdown(
            f"<span style='color: {hydration_indicator(hydration)};'>"
            f"Status: {hydration_indicator(hydration).capitalize()}</span>",
            unsafe_allow_html=True
        )
        if hydration < 20:
            st.error("Warning: Severe dehydration! Seek medical attention.")
        elif 20 <= hydration < 40:
            st.warning("Info: Dehydration detected. Increase water intake.")
        else:
            st.success("Hydration level is within the normal range.")
    with col6:
        st.metric(label="Calorie Intake", value = f"{calories} kcal", delta_color=calories_indicator(calories))
        st.markdown(
            f"<span style='color: {calories_indicator(calories)};'>"
            f"Status: {calories_indicator(calories).capitalize()}</span>",
            unsafe_allow_html=True
        )

    with col7:
        st.metric(label="Sleep Hours", value = f"{sleep_hours:.1f} hrs", delta_color=sleep_hours_indicator(sleep_hours))
        st.markdown(
            f"<span style='color: {sleep_hours_indicator(sleep_hours)};'>"
            f"Status: {sleep_hours_indicator(sleep_hours).capitalize()}</span>",
            unsafe_allow_html=True
        )
        if sleep_hours < 6:
            st.error("Warning: Insufficient sleep! Seek medical attention.")
        elif 6 <= sleep_hours < 7:
            st.warning("Info: Sleep duration is slightly low. Monitor your health.")
        else:
            st.success("Sleep duration is within the normal range.")
    with col8:
        st.metric(label="Radiation Exposure", value = f"{radiation:.2f} mSv", delta_color=radiation_indicator(radiation))
        st.markdown(
            f"<span style='color: {radiation_indicator(radiation)};'>"
            f"Status: {radiation_indicator(radiation).capitalize()}</span>",
            unsafe_allow_html=True
        )
        if radiation >= 3.0:
            st.error("Warning: High radiation exposure! Seek medical attention.") 
        elif 1.0 <= radiation < 3.0:
            st.warning("Info: Radiation exposure is slightly high. Monitor your health.")
        else:
            st.success("Radiation exposure is within the normal range.")  

if __name__ == "__main__":
    main() 