import streamlit as st
import streamlit.components.v1 as com
from datetime import datetime, timedelta
import json
import geopandas as gpd
import pyproj
import plotly.graph_objs as go
import folium
from streamlit_folium import st_folium
import branca.colormap as cm
import pandas as pd
import base64

st.set_page_config(layout="wide")


with open('style.css') as f:
    st.markdown(f'<style> {f.read()} </style>', unsafe_allow_html=True)


# Stars added
st.markdown(""" 
    <div class = 'sky' id='sky_dawn'></div>
    <div class = 'sky' id='sky_noon'></div>
    <div class = 'sky' id='sky_dusk'></div>
    <div class = 'sky' id='sky_night'></div>
    <div class = 'sky' id='sky_stars'>
        <div class = 'star' style='left: 7vw; top: 64vh;'></div>
        <div class = 'star' style='left: 93vw; top: 42vh;'></div>
        <div class = 'star' style='left: 90vw; top: 38vh;'></div>
        <div class = 'star' style='left: 6vw; top: 16vh;'></div>
        <div class = 'star' style='left: 5vw; top: 21vh;'></div>
        <div class = 'star' style='left: 46vw; top: 80vh;'></div>
        <div class = 'star' style='left: 18vw; top: 40vh;'></div>
        <div class = 'star' style='left: 31vw; top: 3vh;'></div>
        <div class = 'star' style='left: 46vw; top: 10vh;'></div>
        <div class = 'star' style='left: 55vw; top: 19vh;'></div>
        <div class = 'star' style='left: 89vw; top: 5vh;'></div>
        <div class = 'star' style='left: 81vw; top: 33vh;'></div>
        <div class = 'star' style='left: 86vw; top: 28vh;'></div>
        <div class = 'star' style='left: 92vw; top: 78vh;'></div>
        <div class = 'star' style='left: 60vw; top: 9vh;'></div>
        <div class = 'star' style='left: 35vw; top: 19vh;'></div>
        <div class = 'star' style='left: 36vw; top: 74vh;'></div>
        <div class = 'star' style='left: 31vw; top: 34vh;'></div>
    </div>  
    <img src="https://i.ibb.co/z6CyNCn/Untitled.png" class="balloon"></div>
    <img src="https://i.ibb.co/gMD1qVj/cute-cloud.png" class="cloud"></div>
        """, unsafe_allow_html=True)


#To run: streamlit run main.py

#reading polygon data from geospatial
polygon = gpd.read_file(r"zones/taxi_zones.shp")

map_df = polygon
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

map_df = map_df.drop(columns=['Shape_Leng', 'Shape_Area', 'LocationID'])

#reading demand data from csv
pre_demand_data = pd.read_csv("transformed_preliminary_data.csv")

pre_demand_data = pre_demand_data.rename(columns={'Zone' : 'OBJECTID'})

def filter_day(prediction, day):
    demand_data = prediction.loc[pre_demand_data['Day'] == 1]
    demand_data = demand_data.drop(columns=['Month', 'Day', 'Year'])
    demand_data = demand_data.pivot(index = 'OBJECTID', columns='Hour', values = 'Total Demand')
    demand_data = demand_data.drop(columns = [24])
    demand_data.reset_index(inplace=True)
    demand_data = demand_data.rename(columns = { x : ("Hour " + str(x)) for x in range(24)})
    df = map_df.merge(demand_data, on="OBJECTID")
    return df



# demand_data = demand_data.rename(columns = {'index':'OBJECTID'})





#header = st.container()
# datatset = st.container()
# features = st.container()
# modelTraining = st.container()

#with header:
#    st.title("Demand Prediction Analysis")




title_html = """<p class='floating'>forecab Analysis: </p>"""
st.markdown(title_html, unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    st.write("")

with col2:
    st.write("")

with col3:
    st.write("")

with col4:
   # dt, padding = st.columns([20,23])
    p_day = st.date_input(label = "date", label_visibility = "collapsed", 
                min_value = datetime(2023, 6, 1), 
                max_value = datetime(2023, 6, 30),
                value = datetime(2023, 6, 1))
    #padding.write("")

with col5:
    st.write("")

with col6:
    st.write("")
    
              
#p_day = st.date_input(label = "date", label_visibility = "collapsed", 
#             min_value = datetime(2023, 6, 1), 
#             max_value = datetime(2023, 6, 30),
#              value = datetime(2023, 6, 1))

df = filter_day(pre_demand_data, int(p_day.strftime("%d")))


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
    current_num = int(formatted_time[0:2]) - 12
    formatted_time = str(current_num) + formatted_time[2:]
elif (int(formatted_time[0:2]) == 0):
    formatted_time = "12:00 AM"


time_to_int = {'12:00 AM' : "Hour 0", '01:00 AM' : "Hour 1", '02:00 AM' : "Hour 2", '03:00 AM' : "Hour 3", '04:00 AM' : "Hour 4", '05:00 AM' : "Hour 5" , '06:00 AM' : "Hour 6", '07:00 AM': "Hour 7", '08:00 AM' : "Hour 8", '09:00 AM' : "Hour 9", '10:00 AM' : "Hour 10", '11:00 AM' : "Hour 11", '12:00 PM' : "Hour 12", '1:00 PM' : "Hour 13", '2:00 PM' : "Hour 14", '3:00 PM' : "Hour 15", '4:00 PM' : "Hour 16", '5:00 PM' : "Hour 17",'6:00 PM' : "Hour 18", '7:00 PM' : "Hour 19",'8:00 PM' : "Hour 20", '9:00 PM' : "Hour 21", '10:00 PM' : "Hour 22", '11:00 PM' : "Hour 23"}
hour = time_to_int[formatted_time]

#time_options = ["1:00","2:00","3:00","4:00","5:00","6:00","7:00","8:00","9:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00", "0:00"]
time_options = ["12:00 AM","01:00 AM","02:00 AM","03:00 AM","04:00 AM","05:00 AM","06:00 AM","07:00 AM","08:00 AM","09:00 AM","10:00 AM","11:00 AM","12:00 PM","1:00 PM","2:00 PM","3:00 PM","4:00 PM","5:00 PM","6:00 PM","7:00 PM","8:00 PM","9:00 PM","10:00 PM", "11:00 PM"]


selected_time = st.select_slider(
    " ",
    value=formatted_time,
    options=time_options,
)


hour = time_to_int[selected_time]


#If you want to add more in-between gradients, just follow this format
#If we have extra time: add stars to the 'nighttime', add clouds to the sky


night = """<style> #sky_night {
    opacity: 1;
}
    #sky_stars{
    opacity: 1;}
    #sky_dusk {
    opacity: 0;
}        
    #sky_noon {
    opacity: 0
}     
    #sky_dawn{
        opacity: 0;

}     
[data-testid="stAppViewContainer"] {
                    background: linear-gradient(
                        0deg,
                        rgb(1, 0, 10) 0%,
                        rgb(15, 6, 100) 100%
	                ); 
            </style>"""

dusk = """ <style> #sky_dusk {
    opacity: 1;}
    #sky_stars{
    opacity: 1;}
 #sky_night {
        opacity: 0;
}        
    #sky_noon {
        opacity: 0;
}     
    #sky_dawn{
        opacity: 0;

}     
[data-testid="stAppViewContainer"] {
                     background: linear-gradient(
                         0deg,
                        rgba(255, 32, 110, 1) 0%,
                         rgba(10, 0, 94, 1) 100%
                     );
                 }
}</style>"""

noon = """ <style>#sky_noon {
    opacity: 1;}
    #sky_stars{
    opacity: 0;}
 #sky_dusk {
        opacity: 0;

}        
    #sky_night {
        opacity: 0;

}     
    #sky_dawn{
        opacity: 0;

}     
[data-testid="stAppViewContainer"] {
                    background: linear-gradient(
                        0deg,
                        rgba(205, 237, 246, 1) 0%,
                        rgb(57, 175, 226) 100%
                    );

}</style>"""

dawn = """ <style>#sky_dawn {
    opacity: 1;}
    #sky_stars{
    opacity: 0;}
 #sky_dusk {
        opacity: 0;

}        
    #sky_noon {
        opacity: 0;

}     
    #sky_night{
        opacity: 0;

}     
[data-testid="stAppViewContainer"] {
                     background: linear-gradient(
                         0deg,
                         rgba(254, 215, 102, 1) 0%,
                         rgba(205, 237, 246, 1) 100%
 	                );
}</style>"""

nighttime = ['Hour 0', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23']
dawntime = ['Hour 4', 'Hour 5', 'Hour 6']
daytime = ['Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16']
dusktime = ['Hour 17', 'Hour 18', 'Hour 19']

if (hour in nighttime):
    bg = night
elif (hour in daytime):
    bg = noon  
elif (hour in dawntime):
    bg = dawn
else:
    bg = dusk

st.markdown(bg, unsafe_allow_html=True)

#geo[0] = ""
#geo[1] = "df.geojson"

choro = folium.Choropleth(
    geo_data = "df.geojson",
    data = df, #we can change this to a list to show depending on hour
    columns = ['OBJECTID', hour],
    key_on='feature.properties.OBJECTID',
    line_opacity=0.2,
    fill_opacity = 0.7,
    fill_color = 'YlOrRd',
    highlight = True
)



map = folium.Map(location=[40.7, -73.850], zoom_start=11, min_zoom= 9, tiles='CartoDB positron')

choro.geojson.add_to(map)
choro.geojson.add_child(
    folium.features.GeoJsonTooltip(
        fields=['zone', hour],
        aliases=['Zone: ','Expected Demand: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)


st_map = st_folium(map, width=1500, height=400)









