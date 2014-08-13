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

    var heatmap_cfg = {
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
    };

    var heatmapLayer = new HeatmapOverlay(heatmap_cfg);
    $scope.map.addLayer(heatmapLayer);

    $http.get('/data/')
    .success(function(data, status, headers, config, statusText) {
        heatmapLayer.setData(data);
    });

    $scope.filters = {
        times: [
            {
                text: "Mañana (6:00 - 11:59)",
                value: 1,
                checked: true
            },{
                text: "Tarde (12:00 - 19:59)",
                value: 2,
                checked: true
            },{
                text: "Noche (20:00 - 5:59)",
                value: 3,
                checked: true
            }
        ],
        companies: [
            {
                text: "Claro",
                value: '0',
                checked: true
            },{
                text: "Entel",
                value: '1',
                checked: true
            },{
                text: "Movistar",
                value: '2',
                checked: true
            },{
                text: "Nextel",
                value: '3',
                checked: true
            },{
                text: "Virgin Mobile",
                value: '4',
                checked: true
            },{
                text: "VTR",
                value: '5',
                checked: true
            }
        ],
        networkTypes: [
            {
                text: "EDGE",
                value: 2,
                checked: true
            },{
                text: "GPRS",
                value: 1,
                checked: true
            },{
                text: "UMTS",
                value: 3,
                checked: true
            },{
                text: "HSPA",
                value: 10,
                checked: true
            },{
                text: "HSPA+",
                value: 15,
                checked: true
            },{
                text: "LTE",
                value: 13,
                checked: true
            },{
                text: "3G/HSDPA",
                value: 8,
                checked: true
            },{
                text: "HSUPA",
                value: 9,
                checked: true
            }
        ],
    };

    $scope.updateFilters = function(target) {
        //console.log($scope.filters.times);
        config = {}
        config.params = { data:$scope.filters }
        $http.get('/data/', config)
        .success(function(data, status, headers, config, statusText) {
            if(data.data.length == 0){
                heatmapLayer._heatmap.setData({data:[]});
            } else {
                heatmapLayer.setData(data);
            }
        })
        .error(function(data, status, headers, config) {
        });
    };
});

traza.controller('PanelController', function($rootScope, $scope, $http) {

});
