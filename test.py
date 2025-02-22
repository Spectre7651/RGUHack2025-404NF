# import gmplot
# apikey = '' # (your API key here)
# gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13, apikey=apikey)

# path = zip(*[
#     (37.773097, -122.471789),
#     (37.785920, -122.472693),
#     (37.787815, -122.472178),
#     (37.791430, -122.469763),
#     (37.792547, -122.469624),
#     (37.800724, -122.469460)
# ])

# gmap.plot(*path, edge_width=7, color='red')
# gmap.draw('map.html')

import requests
response = requests.get("https://elementz.rguhack.uk/pointsOfInterest")

print(response.json())
import json
import gmplot
apikey = '' # (your API key here)
gmap = gmplot.GoogleMapPlotter(57.118696610829296, -2.1350145324081367, 5, apikey=apikey)

resjson = response.json()
print(resjson[0]['name'])

lat = []
lon = []
i = 0
for ii in resjson:

    lat.append(resjson[i]['coordinates']['latitude'])
    lon.append(resjson[i]['coordinates']['longitude'])
    print(lat[i],lon[i])

    gmap.marker(lat[i], lon[i], precision=2, color='#FFD700')
    i += 1
#print(response.get('id'))
# path = zip(*[
#     response.json()
# ])


# #gmap.plot(*path, edge_width=7, color='red')
# gmap.plot(response.json())
gmap.draw('map.html')