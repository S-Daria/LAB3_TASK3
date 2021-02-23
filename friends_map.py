import folium
import pandas


def generate_map_with_csv():
    data = pandas.read_csv("friends_location.csv", error_bad_lines=False)
    lat = data['latitude']
    lon = data['longitude']
    map = folium.Map()
    fg = folium.FeatureGroup(name="Friends' map")

    name = data['name']
    place = data['place']

    for lt, ln, nm, pl in zip(lat, lon, name, place):
        fg.add_child(folium.Marker(location=[lt, ln],
        popup=f'{nm}, {pl}',
        icon=folium.Icon(color = "red")))

    map.add_child(fg)
    map.save('templates/friends_map.html')
