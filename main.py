import streamlit as st
from datetime import datetime, timedelta
import json
import geopandas as gpd
import pyproj
import plotly.graph_objs as go

#To run: streamlit run main.py

header = st.container()
# datatset = st.container()
# features = st.container()
# modelTraining = st.container()

with header:
    st.title("Demand Prediction Analysis")

# Define start and end times
start_time = datetime(2023, 1, 1, 0, 0, 0)
end_time = datetime(2023, 1, 2, 0, 0, 0)

# Create slider
selected_time = st.slider(
    "Select a time range",
    min_value=start_time,
    max_value=end_time,
    step=timedelta(minutes=60),
    format="HH:mm"
)

# Display selected time
st.write("Selected time:", (selected_time+timedelta(hours=24)).strftime("%I:%M %p"))
