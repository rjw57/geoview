(function(){

var MAP_PROJECTION = ol.proj.get(MAP_PROJECTION_CODE);
if(!MAP_PROJECTION) {
    console.log('Map projection invalid, falling back to lat/lng');
    MAP_PROJECTION = ol.proj.get('EPSG:4326');
}

// Create main map
var map = new ol.Map({
    target: 'map',
    view: new ol.View({
        center: ol.proj.transform([1.0, 52.0], 'EPSG:4326', MAP_PROJECTION),
        zoom: 4,
        projection: MAP_PROJECTION,
    }),
});
console.log('created map:', map);

// Add zoom control
map.addControl(new ol.control.ZoomToExtent());

// The "datasetUrls" variable is created dynamically. Use it to fire off a
// request for our data layers.
Object.getOwnPropertyNames(datasetUrls).forEach(function(name) {
    var url = datasetUrls[name];

    var source = new ol.source.GeoJSON({
        projection: MAP_PROJECTION,
        url: url,
    });

    var layer = new ol.layer.Vector({
        source: source,
    });

    map.addLayer(layer);
});

})();
