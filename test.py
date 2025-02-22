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
c

#print(response.json())
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

response2 = requests.get("https://elementz.rguhack.uk/subseaPipelines")
resjson2 = response2.json()
print(response2.json())
spipelat = []
spipelon = []
epipelat = []
epipelon = []
#print(resjson2[1]['end_coordinates']['coordinates']['latitude'])
for pipeii in response2.json():
    # Extract latitude and longitude
    spipelat.append(pipeii['start_coordinates']['coordinates']['latitude'])
    spipelon.append(pipeii['start_coordinates']['coordinates']['longitude'])
    epipelat.append(pipeii['end_coordinates']['coordinates']['latitude'])
    epipelon.append(pipeii['end_coordinates']['coordinates']['longitude'])

print(spipelat[2] , spipelon[2], epipelat[2] , epipelon[2])
#print(response.get('id'))
pp = 0
for p in spipelat:
    path = zip(*[
        (spipelat[pp],spipelon[pp]),
        (epipelat[pp],epipelon[pp])
    ])
    gmap.plot(*path, edge_width=4, color='red')
    pp = pp + 1
    print(pp)

subseaAssetResult = requests.get("https://elementz.rguhack.uk/subseaAssets")
subseaAssetsLat = []
subseaAssetsLon = []

for asset in subseaAssetResult.json():
    subseaAssetsLat.append(asset['coordinates']['coordinates']['latitude'])
    subseaAssetsLon.append(asset['coordinates']['coordinates']['longitude'])
for point in range(len(subseaAssetsLon)):    
    gmap.marker(subseaAssetsLat[point], subseaAssetsLon[point], precision=2, color='blue')

surfAssetResult = requests.get("https://elementz.rguhack.uk/surfVessels")
surfAssetsLat = []
surfAssetsLon = []

for asset in surfAssetResult.json():
    surfAssetsLat.append(asset['coordinates']['latitude'])
    surfAssetsLon.append(asset['coordinates']['longitude'])

for point in range(len(surfAssetsLon)):    
    gmap.marker(surfAssetsLat[point], surfAssetsLon[point], precision=2, color='pink')
gmap.draw('map.html')