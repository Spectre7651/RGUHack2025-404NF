from flask import Flask, render_template, jsonify
import requests
import json
import gmplot

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/templates/Ness.html')
def templates():
    return render_template("Ness.html")
    #Setup Google Map
apikey = '' #No api key needed for dev
gmap = gmplot.GoogleMapPlotter(57.118696610829296, -2.1350145324081367, 5, apikey=apikey)

#Get points of interest
POIResponse = requests.get("https://elementz.rguhack.uk/pointsOfInterest")
POILat = []
POILon = []
POIName = []
POIDesc = []
for element in POIResponse.json():
    POILat.append(element['coordinates']['latitude'])
    POILon.append(element['coordinates']['longitude'])
    POIName.append(element['name'])
    POIDesc.append(element['description']) 

#Plot POI's
for point in range(len(POILat)):
    gmap.marker(POILat[point], POILon[point], title=POIName[point], label='i', info_window=f"""<html><h2>{POIName[point]}</h2>
            <br> Description: {POIDesc[point]}</h4></html>""" , precision=2, color='#FFD700')


#Get pipelines
PipeResponse = requests.get("https://elementz.rguhack.uk/subseaPipelines")
PipeStartLat = []
PipeStartLon = []
PipeEndLat = []
PipeEndLon = []
PipeName = []
PipeDepth = [[],[]]
PipeHealth = []
PipePressure = []
PipeTemp = []
PipeFlowRate = []
PipeMaintenanceInfo = [[],[]]
PipeAlerts = []
PipeAnomalies = []

for pipe in PipeResponse.json():
    PipeStartLat.append(pipe['start_coordinates']['coordinates']['latitude'])
    PipeStartLon.append(pipe['start_coordinates']['coordinates']['longitude'])
    PipeEndLat.append(pipe['end_coordinates']['coordinates']['latitude'])
    PipeEndLon.append(pipe['end_coordinates']['coordinates']['longitude'])
    PipeName.append(pipe['name'])
    PipeDepth[0].append(pipe['start_coordinates']['depth'])
    PipeDepth[1].append(pipe['end_coordinates']['depth'])
    PipeHealth.append(pipe['health'])
    PipePressure.append(pipe['pressure'])
    PipeTemp.append(pipe['temperature'])
    PipeFlowRate.append(pipe['flow_rate'])
    PipeMaintenanceInfo[0].append(pipe['last_inspection'])
    PipeMaintenanceInfo[1].append(pipe['next_maintenance'])
    PipeAlerts.append(pipe['alerts'][0])
    PipeAnomalies.append(pipe['open_anomaly_count'])

#Plot pipelines
for point in range(len(PipeName)):
    #print(PipeDepth[0][point])
    path = zip(*[
        (PipeStartLat[point],PipeStartLon[point]),
        (PipeEndLat[point],PipeEndLon[point])
    ])
    gmap.plot(*path, edge_width=4, color="lightgrey")

#Get subsea assets
SubAssetResult = requests.get("https://elementz.rguhack.uk/subseaAssets")
SubAssetLat = []
SubAssetLon = []
SubAssetDepth = []
SubAssetName = []
SubAssetHealth = []
SubAssetPressure = []
SubAssetTemp = []
SubAssetFlowRate = []
SubAssetMaintenanceInfo = [[],[]]
SubAssetAlerts = []
SubConnectedAssets = []
SubAssetAnomalies = []
SubAssetWorkpacks = []

for asset in SubAssetResult.json():
    SubAssetLat.append(asset['coordinates']['coordinates']['latitude'])
    SubAssetLon.append(asset['coordinates']['coordinates']['longitude'])
    SubAssetDepth.append(asset['coordinates']['depth'])
    SubAssetName.append(asset['name'])
    SubAssetHealth.append(asset['health'])
    SubAssetPressure.append(asset['pressure'])
    SubAssetTemp.append(asset['temperature'])
    SubAssetFlowRate.append(asset['flow_rate'])
    SubAssetMaintenanceInfo[0].append(asset['last_inspection'])
    SubAssetMaintenanceInfo[1].append(asset['next_maintenance'])
    SubAssetAlerts.append([])  
    tempalerts = []
    for alert in range(5):
        try:
            tempalerts.append(asset['alerts'][alert])
            SubAssetAlerts.append(tempalerts)   
        except IndexError:
            break 
    tempconnassets = []
    for connasset in range(5):
        try:
            tempconnassets.append(asset['connected_assets'][connasset])
            SubConnectedAssets.append(tempconnassets)   
        except IndexError:
            break 
    SubAssetAnomalies.append(asset['open_anomaly_count'])
    SubAssetWorkpacks.append(asset['workpacks_at_site_count'])
#Plot Subsea Assets
for point in range(len(SubAssetName)):
    gmap.marker(SubAssetLat[point],SubAssetLon[point], title=SubAssetName[point], info_window=f"""<html><img src="https://th.bing.com/th/id/R.c5e045cba2f39843da6aa04a4d38eab4?rik=Yw7DWIqLARm9BA&riu=http%3a%2f%2fbrisktradeng.net%2fwp-content%2fuploads%2f2023%2f03%2fIMG-3077.jpg&ehk=itwRfFrixBukPJgYSSBORnN3gCyUWCAaDjVEUW%2fFH4s%3d&risl=&pid=ImgRaw&r=0"style="width:200px;height:200px;">
            <h2>{SubAssetName[point]}</h2>
            <h4><br> Depth: {SubAssetDepth[point]}m
            <br> Health: {SubAssetHealth[point]}
            <br> Pressure: {SubAssetPressure[point]} bar
            <br> Temperature: {SubAssetTemp[point]}&degC
            <br> FlowRate: {SubAssetFlowRate[point]}l/min
            <br> Last Insp: {SubAssetMaintenanceInfo[0][point]}
            <br> Next Maintainance: {SubAssetMaintenanceInfo[1][point]},
            <br> Alerts: {SubAssetAlerts[point]},
            <br> Connected Assets: {SubConnectedAssets[point]}
            <br> Anomalies: {SubAssetAnomalies[point]}
            <br> Workpacks: {SubAssetWorkpacks[point]}</h4></html>""" , precision=2, color="purple")


#Get Surface Assets
SurfAssetResult = requests.get("https://elementz.rguhack.uk/surfVessels")
SurfAssetLat = []  
SurfAssetLon = []
SurfAssetName = []
SurfAssetVesselType = []
SurfAssetHeading = []
SurfAssetSpeed = []
SurfAssetDest = []
SurfAssetETA = []
SurfAssetStatus = []
SurfAssetLastInspection = []
SurfAssetCrewCount = []
SurfAssetFuelLevel = []
SurfAssetWeather = [[],[],[]]

for asset in SurfAssetResult.json():
    SurfAssetLat.append(asset['coordinates']['latitude'])
    SurfAssetLon.append(asset['coordinates']['longitude'])
    SurfAssetName.append(asset['name'])
    SurfAssetVesselType.append(asset['vessel_type'])
    SurfAssetHeading.append(asset['heading'])
    SurfAssetSpeed.append(asset['speed'])
    SurfAssetDest.append(asset['destination'])
    SurfAssetETA.append(asset['eta'])
    SurfAssetStatus.append(asset['status'])
    SurfAssetLastInspection.append(asset['last_inspection'])
    SurfAssetCrewCount.append(asset['crew_count'])
    SurfAssetFuelLevel.append(asset['fuel_level'])
    SurfAssetWeather[0].append(asset['weather']['wind_speed'])
    SurfAssetWeather[1].append(asset['weather']['wave_height'])
    SurfAssetWeather[2].append(asset['weather']['temperature'])

for point in range(len(SurfAssetName)):
    gmap.marker(SurfAssetLat[point],SurfAssetLon[point], title=SurfAssetName[point], info_window=f"""
    <html><h2>{SurfAssetName[point]}</h2>
    <h4><br> Vessel Type: {SurfAssetVesselType[point]}
    <br> Heading: {SurfAssetHeading[point]} N
    <br> Speed: {SurfAssetSpeed[point]} knots
    <br> Destination: {SurfAssetDest[point]}
    <br> ETA: {SurfAssetETA[point]}
    <br> Status: {SurfAssetStatus[point]}
    <br> Last Inspection: {SurfAssetLastInspection[point]}
    <br> Crew Count: {SurfAssetCrewCount[point]}
    <br> Fuel Level: {SurfAssetFuelLevel[point]}%
    <br> Weather: <br>
    <ul>Wind Speed: {SurfAssetWeather[0][point]}mph </ul>
    <ul>Wave height:{SurfAssetWeather[1][point]}m</ul>
    <ul>temprature:{SurfAssetWeather[2][point]}&degC</ul>
    </h4></html>
    """, precision=2, color="blue")
gmap.draw('templates/map.html')


# import os

# def create_html_file(data, file_name, template_dir='templates'):
#     # Ensure the template directory exists
#     os.makedirs(template_dir, exist_ok=True)
    
#     # Create the HTML content
#     html_content = f"""
#     <div id="content">
#         <h1>{data['heading']}</h1>
#         <p>{data['content']}</p>
#     """
    
#     # Write the HTML content to a file
#     file_path = os.path.join(template_dir, f"{file_name}.html")
#     with open(file_path, 'w') as file:
#         file.write(html_content)
    
#     print(f"HTML file created at {file_path}")

#  # Example usage
# data = {
#     'title': 'Sample Page',
#     'heading': 'Welcome to the Sample Page',
#     'content': 'This is a sample HTML page generated using Python.'
#     }

# create_html_file(data, 'sample_page')

if __name__ == '__main__':
    app.run(debug=True)
