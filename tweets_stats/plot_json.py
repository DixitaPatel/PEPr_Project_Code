import json
import folium
import pandas as pd
import matplotlib.pylab as plt

from geopy.geocoders import Nominatim

geocode_data_file = "geocodes_data.json"

def plot_line_chart(filename):
    with open(filename) as f:
        data = json.load(f)

    print(type(data))

    required_data = {}
    for k, v in data.items():
        if "26-16" <= k <= "27-10":
            key1 = "0" + k.split("-")[0] if len(k.split("-")[0]) < 2 else k.split("-")[0]
            key2 = "0" + k.split("-")[1] if len(k.split("-")[1]) < 2 else k.split("-")[1]
            key = float(key1) + float(key2)/24.0
            print(k, " converted to ", key, " value", v)
            required_data[float(key)] = v

    lists = sorted(required_data.items())
    x, y = zip(*lists)
    plt.plot(x, y)
    plt.xticks(rotation=90)
    plt.show()

def convert_location_to_geocodes(filename):
    geolocator = Nominatim(user_agent="pepr_geocode_getter")

    with open(filename) as f:
        locations = json.load(f)

    latitudes = []
    longitudes = []
    names = []
    values = []

    for k, v in locations.items():
        location = geolocator.geocode(k)

        # print(location)
        # print(location.latitude, ", ", location.longitude, ", ", location.address, ", ", v)
        try:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
            names.append(location.address)
            values.append(v)
        except Exception as e:
            print(e)

    geocodes_data = {
        'lat': latitudes,
        'lon': longitudes,
        'name': names,
        'value': values
    }

    outfile = open(geocode_data_file, 'w')
    json.dump(geocodes_data, outfile)

    # return [latitudes, longitudes, names, values]

def plot_bubble_chart(geocode_data_file):

    with open(geocode_data_file) as f:
        geocodes_data = json.load(f)
    # [latitudes, longitudes, names, values] = geocodes_data

    # Make a data frame with dots to show on the map
    data = pd.DataFrame(geocodes_data)
    print(data)

    # Make an empty map
    m = folium.Map(location=[37.7837304, -97.4458825], tiles="Mapbox Bright", zoom_start=5)
    m.save('test.html')

    # folium.Circle(
    #     radius=100,
    #     location=[45.5244, -122.6699],
    #     popup='The Waterfront',
    #     color='crimson',
    #     fill=False,
    # ).add_to(m)

    # I can add marker one by one on the map
    for i in range(0, 20):
        folium.Circle(
            location=[float(data.iloc[i]['lat']), float(data.iloc[i]['lon'])],
            popup=str(data.iloc[i]['name']),
            radius=int(data.iloc[i]['value']) * 100,
            color='crimson',
            fill=True,
        ).add_to(m)

    # Save it as html
    m.save('mymap.html')


def plot_charts():

    # line_chart_inputfile = 'stats/date_count.json'
    # plot_line_chart(line_chart_inputfile)
    # print('plotted line chart')


    # bubble_chart_inputfile = 'stats/location_count.json'
    # convert_location_to_geocodes(bubble_chart_inputfile)
    # print('geocode_data_file is ready!')

    plot_bubble_chart(geocode_data_file)
    print('plotted bubble chart')


if __name__ == '__main__':
    plot_charts()
