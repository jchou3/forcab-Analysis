import streamlit as st
import json
import geopandas as gpd
import pyproj
import plotly.graph_objs as go
import folium
from streamlit_folium import st_folium
import branca.colormap as cm
import pandas as pd

# reading polygon data from geospatial
polygon = gpd.read_file(r"zones/taxi_zones.shp")

map_df = polygon
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

map_df = map_df.drop(columns=['Shape_Leng', 'Shape_Area', 'LocationID'])

#reading demand data from csv
pre_demand_data = pd.read_csv("final_predictions.csv")
pre_demand_data = pre_demand_data.drop(columns=['Total Demand'])
pre_demand_data = pre_demand_data.rename(columns={'Predictions': 'Total Demand'})


for i in range(1, 31):
    demand_data = pre_demand_data.rename(columns={'Zone' : 'OBJECTID'})
    demand_data = demand_data.loc[demand_data['Day'] == i]
    demand_data = demand_data.drop(columns=['Month', 'Day', 'Year'])
    # demand_data['Total Demand'] = demand_data['Total Demand'].fillna(0)

    demand_data = demand_data.pivot_table(index = 'OBJECTID', columns='Hour', values = 'Total Demand')

    # demand_data = demand_data.drop(columns = [24])
    demand_data.reset_index(inplace=True)
    demand_data = demand_data.rename(columns = { x : ("Hour " + str(x)) for x in range(24)})
    df = map_df.merge(demand_data, on="OBJECTID")
    name = "geo/day" + str(i) + ".geojson"
    df.to_file(name, driver="GeoJSON") 





# polygon = gpd.read_file(r"zones/taxi_zones.shp")

# map_df = polygon
# map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

# map_df = map_df.drop(columns=['Shape_Leng', 'Shape_Area', 'LocationID'])

# #reading demand data from csv
# pre_demand_data = pd.read_csv("final_predictions.csv")
# pre_demand_data = pre_demand_data.drop(columns=['Total Demand'])

# pre_demand_data = pre_demand_data.rename(columns = {'0' : 'Total Demand'})
# pre_demand_data = pre_demand_data.rename(columns={'Zone' : 'OBJECTID'})

# # geojson file names for each day
# geos = [""]
# for i in range(1, 31):
#     name = "geo/day" + str(i) + ".geojson"
#     geos.append(name)




# def filter_day(prediction, day):
#     demand_data = prediction.loc[pre_demand_data['Day'] == day]
#     demand_data = demand_data.drop(columns=['Month', 'Day', 'Year'])
#     # demand_data['Total Demand'] = demand_data['Total Demand'].fillna(0)
#     print(demand_data.head(5))
#     demand_data = demand_data.pivot(index = 'OBJECTID', columns='Hour', values = 'Total Demand')
#     # demand_data = demand_data.fillna(0)
#     demand_data = demand_data.drop(columns = [24])
#     demand_data.reset_index(inplace=True)
#     demand_data = demand_data.rename(columns = { x : ("Hour " + str(x)) for x in range(24)})
#     df = map_df.merge(demand_data, on="OBJECTID")
#     return df


# df = filter_day(pre_demand_data, 3)

# day = 3
# hour = "Hour 12"



# choro = folium.Choropleth(
#     geo_data = geos[day],
#     data = df, #we can change this to a list to show depending on hour
#     columns = ['OBJECTID', hour],
#     key_on='feature.properties.OBJECTID',
#     line_opacity=0.2,
#     fill_opacity = 0.7,
#     fill_color = 'YlOrRd',
#     highlight = True
# )



# map = folium.Map(location=[40.7, -73.850], zoom_start=11, min_zoom= 9, tiles='CartoDB positron')

# choro.geojson.add_to(map)
# choro.geojson.add_child(
#     folium.features.GeoJsonTooltip(
#         fields=['zone', hour],
#         aliases=['Zone: ','Expected Demand: '],
#         style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
#     )
# )


# st_map = st_folium(map, width=1500, height=400)







# demand_data = demand_data.rename(columns = {'index':'OBJECTID'})





#convert df to json
# 


# hour = 'Hour 18'


# choro = folium.Choropleth(
#     geo_data = geos[2],
#     data = days[2],
#     columns = ['OBJECTID', hour],
#     key_on='feature.properties.OBJECTID',
#     line_opacity=0.2,
#     fill_opacity = 0.7,
#     fill_color = 'BuPu',
#     highlight = True
# )



# map = folium.Map(location=[40.7, -73.70], zoom_start=10, tiles='CartoDB positron')

# choro.geojson.add_to(map)
# choro.geojson.add_child(
#     folium.features.GeoJsonTooltip(
#         fields=['zone', hour],
#         aliases=['Zone: ','Expected Demand: '],
#         style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
#     )
# )

# st_map = st_folium(map, width=1000, height=500)
