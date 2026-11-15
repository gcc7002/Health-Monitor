from datetime import datetime, timedelta

import streamlit as st

from storage import load_data

st.set_page_config(page_title="Health Timeline", layout="wide")

#Loading the data
df = load_data

st.title("Health Timeline")
st.caption("Timeline view will be available here. Use the app navigation to open Calendar.")

#Here's the code for the timeline, the idea is to show every action during 14 days, so astronauts could be able to check their routine and understand their situation
if df.empty:
    st.info("No data has been registered yet")
else:
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start = today - timedelta(days=13)

    recent=(
        df.loc[
            (df["timestamp"] >= start) & (df["timestamp"] <= now)
        ].sort_values("timestamp")
    )

    if recent.empty:
        st.info("No registered action")
    else:
        choice = st.selectbox("Which measure you want to view", option=)