def create_map():
    #Imports

    import requests
    import json
    import gmplot

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
        POIName.append(element['description']) 

    #Plot POI's
    for point in range(len(POILat)):
        gmap.marker(POILat[point], POILon[point], title=POIName[point], precision=2, color='#FFD700')


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
        gmap.marker(SubAssetLat[point],SubAssetLon[point], title=SubAssetName[point], precision=2, color="purple")


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
        SurfAssetWeather.append(([asset['weather']['wind_speed']],[asset['weather']['wave_height']],[asset['weather']['temperature']]))

    for point in range(len(SurfAssetName)):
        gmap.marker(SurfAssetLat[point],SurfAssetLon[point], title=SurfAssetName[point], precision=2, color="blue")
    gmap.draw('map.html')