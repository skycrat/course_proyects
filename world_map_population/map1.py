import folium
import pandas as pd

data = pd.read_csv(".venv\Mapping\Volcanoes.txt")
lat = list(data.LAT)
lon = list(data.LON)
elev = list(data.ELEV)

def color_producer(elevation, color = None):
    if elevation <1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[38.58,-99.09], zoom_start=6, tiles = "CartoDB positron")

fg = folium.FeatureGroup(name="My Map")

for lt, ln, el in zip(lat, lon, elev):

    fg.add_child(folium.Marker(location= [lt, ln], popup=str(el) +"m", icon= folium.Icon(color=color_producer(el))))

map.add_child(fg)
map.save("Map1.html")
