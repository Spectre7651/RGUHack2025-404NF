let map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 57.118696610829296, lng: -2.1350145324081367 },
        zoom: 5
    });

    plotData('poi', POIData);
    plotData('pipe', PipeData);
    plotData('sub_asset', SubAssetData);
    plotData('surf_asset', SurfAssetData);
}

function plotData(category, data) {
    data.forEach((item, index) => {
        let position = getPosition(category, item);
        let marker = new google.maps.Marker({
            position: position,
            map: map,
            title: item.name || item.description
        });

        marker.addListener('click', () => {
            fetch(`get_info/${category}/${index}`)
                .then(response => response.json())
                .then(info => displayInfo(info));
        });
    });
}

function getPosition(category, item) {
    switch(category) {
        case 'poi':
        case 'sub_asset':
            return { lat: item.coordinates.coordinates.latitude, lng: item.coordinates.coordinates.longitude };
        case 'pipe':
            return { lat: item.start_coordinates.coordinates.latitude, lng: item.start_coordinates.coordinates.longitude };
        case 'surf_asset':
            return { lat: item.coordinates.latitude, lng: item.coordinates.longitude };
    }
}

function displayInfo(info) {
    let infoDiv = document.getElementById('info');
    infoDiv.innerHTML = `<pre>${JSON.stringify(info, null, 2)}</pre>`;
}

window.onload = initMap;
