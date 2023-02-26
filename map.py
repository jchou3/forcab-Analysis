import streamlit as st
import json
import geopandas as gpd
import pyproj
import plotly.graph_objs as go
import folium
from streamlit_folium import st_folium
import branca.colormap as cm
import pandas as pd

#reading polygon data from geospatial
polygon = gpd.read_file(r"zones\taxi_zones.shp")

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



#convert df to json
# df.to_file("df.geojson", driver="GeoJSON") 


hour = 'Hour 12'

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



map = folium.Map(location=[40.7, -73.70], zoom_start=10, tiles='CartoDB positron')

choro.geojson.add_to(map)
choro.geojson.add_child(
    folium.features.GeoJsonTooltip(
        fields=['zone', hour],
        aliases=['Zone: ','Expected Demand: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)

st_map = st_folium(map, width=1000, height=500)
