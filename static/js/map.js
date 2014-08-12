var traza = angular.module('traza', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

traza.controller('MapController', function($rootScope, $scope, $http) {

    $scope.map = L.mapbox.map('map', 'traza.j760in07', {
        zoomControl: true,
        zoomControlPosition: 'top-left',
        center: [-33.43782061488737, -70.65045297145844],
        zoom: 12,
        detectRetina: true
    })
    .locate({setView : true, maxZoom: 14});

    var heatmapLayer = new HeatmapOverlay({
        // radius should be small ONLY if scaleRadius is true (or small radius is intended)
        "radius": 0.004,
        "maxOpacity": .9,
        "minOpacity": .08,
        // scales the radius based on map zoom
        "scaleRadius": true,
        // if set to false the heatmap uses the global maximum for colorization
        // if activated: uses the data maximum within the current map boundaries
        //   (there will always be a red spot with useLocalExtremas true)
        "useLocalExtrema": true,
        // which field name in your data represents the latitude - default "lat"
        latField: 'lat',
        // which field name in your data represents the longitude - default "lng"
        lngField: 'lng',
        // which field name in your data represents the data value - default "value"
        valueField: 'val'
    });

    $scope.map.addLayer(heatmapLayer);

    $http.get('/data/')
    .success(function(data, status, headers, config, statusText) {
        heatmapLayer.setData(data);
    });
});

traza.controller('PanelController', function($rootScope, $scope, $http) {
    $scope.filters = {
        times: [
            {
                text: "Mañana (6:00 - 11:59)",
                checked: true
            },
            {
                text: "Tarde (12:00 - 19:59)",
                checked: true
            },
            {
                text: "Noche (20:00 - 5:59)",
                checked: true
            }
        ],
        companies: [
            {
                text: "Claro",
                id: 1,
                checked: true
            },
            {
                text: "Entel",
                id: 2,
                checked: true
            },
            {
                text: "Movistar",
                id: 3,
                checked: true
            },
            {
                text: "Nextel",
                id: 4,
                checked: true
            },
            {
                text: "Virgin Mobile",
                id: 5,
                checked: true
            },
            {
                text: "VTR",
                id: 6,
                checked: true
            }
        ],
        networkTypes: [
            {
                text: "EDGE",
                id: null,
                checked: true
            },
            {
                text: "GPRS",
                id: null,
                checked: true
            },
            {
                text: "3G",
                id: null,
                checked: true
            },
            {
                text: "3.5G",
                id: null,
                checked: true
            },
            {
                text: "4G LTE",
                id: null,
                checked: true
            }
        ],
    };

    $scope.updateFilters = function(target) {
        
    };
});
