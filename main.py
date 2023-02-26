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

# st.markdown(f""" 
#     <div class='sky_phase sky_dawn'></div>
#     <div class='sky_phase sky_noon'></div>
#     <div class='sky_phase sky_dusk'></div>
#     <div class='sky_phase sky_night'>
#         <div id='sky_stars'></div>    
#     </div>
#         """, unsafe_allow_html=True)

#To run: streamlit run main.py

#reading polygon data from geospatial
polygon = gpd.read_file(r"zones/taxi_zones.shp")

map_df = polygon
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

map_df = map_df.drop(columns=['Shape_Leng', 'Shape_Area', 'LocationID'])

#reading demand data from csv
demand_data = pd.read_csv("transformed_preliminary_data.csv")

demand_data = demand_data.rename(columns={'Zone' : 'OBJECTID'})
demand_data = demand_data.loc[demand_data['Day'] == 1]
demand_data = demand_data.drop(columns=['Month', 'Day', 'Year'])

demand_data = demand_data.pivot(index = 'OBJECTID', columns='Hour', values = 'Total Demand')
demand_data = demand_data.drop(columns = [24])
demand_data.reset_index(inplace=True)
demand_data = demand_data.rename(columns = { x : ("Hour " + str(x)) for x in range(24)})

# demand_data = demand_data.rename(columns = {'index':'OBJECTID'})

df = map_df.merge(demand_data, on="OBJECTID")



#header = st.container()
# datatset = st.container()
# features = st.container()
# modelTraining = st.container()

#with header:
#    st.title("Demand Prediction Analysis")
title_html = """<p class='floating'>Demand Prediction Analysis</p>"""
st.markdown(title_html, unsafe_allow_html=True)


#Integrating HTML & CSS

# com.html("""
#     <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
#     <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
#     <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
#     <div id="accordion">
#         <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
#           <div class="card-body">
#             Collapsible Group Item #2 content
#           </div>
#         </div>
#       </div>
#     </div>
#     """,
#     height=600)



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


time_to_int = {'12:00 AM' : "Hour 0", '01:00 AM' : "Hour 1", '02:00 AM' : "Hour 2", '03:00 AM' : "Hour 3", '04:00 AM' : "Hour 4", '05:00 AM' : "Hour 5" , '06:00 AM' : "Hour 6", '07:00 AM': "Hour 7", '08:00 AM' : "Hour 8", '09:00 AM' : "Hour 9", '10:00 AM' : "Hour 10", '11:00 AM' : "Hour 11", '12:00 PM' : "Hour 12", '01:00 PM' : "Hour 13", '02:00 PM' : "Hour 14", '03:00 PM' : "Hour 15", '04:00 PM' : "Hour 16", '05:00 PM' : "Hour 17",'06:00 PM' : "Hour 18", '07:00 PM' : "Hour 19",'08:00 PM' : "Hour 20", '09:00 PM' : "Hour 21", '10:00 PM' : "Hour 22", '11:00 PM' : "Hour 23"}
hour = time_to_int[formatted_time]

#time_options = ["1:00","2:00","3:00","4:00","5:00","6:00","7:00","8:00","9:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00", "0:00"]
time_options = ["12:00 AM","01:00 AM","02:00 AM","03:00 AM","04:00 AM","05:00 AM","06:00 AM","07:00 AM","08:00 AM","09:00 AM","10:00 AM","11:00 AM","12:00 PM","01:00 PM","02:00 PM","03:00 PM","04:00 PM","05:00 PM","06:00 PM","07:00 PM","08:00 PM","09:00 PM","10:00 PM", "11:00 PM"]


selected_time = st.select_slider(
    " ",
    value=formatted_time,
    options=time_options,
)


hour = time_to_int[selected_time]


choro = folium.Choropleth(
    geo_data = "df.geojson",
    data = df, #we can change this to a list to show depending on hour
    columns = ['OBJECTID', hour],
    key_on='feature.properties.OBJECTID',
    line_opacity=0.2,
    fill_opacity = 0.7,
    fill_color = 'BuPu',
    highlight = True
)



map = folium.Map(location=[40.7, -73.90], zoom_start=11, tiles='CartoDB positron')

choro.geojson.add_to(map)
choro.geojson.add_child(
    folium.features.GeoJsonTooltip(
        fields=['zone', hour],
        aliases=['Zone: ','Expected Demand: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)

st_map = st_folium(map, width=1500, height=400)









