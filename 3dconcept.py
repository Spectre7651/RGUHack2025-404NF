#making the plot#if you are passing just one lat and lon, put it within "[]"
import plotly.graph_objects as pgo
import requests

SubAssetResult = requests.get("https://elementz.rguhack.uk/subseaAssets")
SubAssetLat = []
SubAssetLon = []
for asset in SubAssetResult.json():
    SubAssetLat.append(asset['coordinates']['coordinates']['latitude'])
    SubAssetLon.append(asset['coordinates']['coordinates']['longitude'])

map = pgo.Figure(pgo.Scattergeo(lat=SubAssetLat, lon=SubAssetLon))#editing the marker
map.update_traces(marker_size=20, line=dict(color='Red'), hoverinfo='name', name="Rig1")# this projection_type = 'orthographic is the projection which return 3d globe map'
map.update_geos(projection_type="orthographic")#layout, exporting html and showing the plot
map.update_layout(width= 800, height=800, margin={"r":0,"t":0,"l":0,"b":0})
map.write_html("3d_plot.html")
map.show()