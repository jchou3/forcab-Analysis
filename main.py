import streamlit as st
from datetime import datetime, timedelta

#header = st.container()
# datatset = st.container()
# features = st.container()
# modelTraining = st.container()

#with header:
#    st.title("Demand Prediction Analysis")

st.markdown("<h1 style='text-align: center; color: grey;'>Demand Prediction Analysis</h1>", unsafe_allow_html=True)

# Define start and end times
#start_time = datetime(2023, 1, 1, 0, 0, 0)
#end_time = datetime(2023, 1, 2, 0, 0, 0)
current_time = datetime.now()
#rounded_time = current_time + timedelta(hours=1) - timedelta(minutes=current_time.minute, seconds=current_time.second)
if current_time.minute == 00:
    rounded_time = current_time
elif current_time.minute >= 30:
    rounded_time = current_time + timedelta(hours=1) - timedelta(minutes=current_time.minute, seconds=current_time.second)
else:
    rounded_time = current_time - timedelta(minutes=current_time.minute)

    

formatted_time = rounded_time.strftime("%H:%M %p")

if(int(formatted_time[0:2]) > 12):
    print(int(formatted_time[0:2]))
    current_num = int(formatted_time[0:2]) - 12
    formatted_time = str(current_num) + formatted_time[2:]
elif (int(formatted_time[0:2]) == 0):
    formatted_time = "12:00 AM"


#time_options = ["1:00","2:00","3:00","4:00","5:00","6:00","7:00","8:00","9:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00", "0:00"]
time_options = ["12:00 AM","1:00 AM","2:00 AM","3:00 AM","4:00 AM","5:00 AM","6:00 AM","7:00 AM","8:00 AM","9:00 AM","10:00 AM","11:00 AM","12:00 PM","1:00 PM","2:00 PM","3:00 PM","4:00 PM","5:00 PM","6:00 PM","7:00 PM","8:00 PM","9:00 PM","10:00 PM", "11:00 PM"]


selected_time = st.select_slider(
    "Time:",
    value=formatted_time,
    options=time_options,
)

# Display selected time
st.write("Selected time:", selected_time)


