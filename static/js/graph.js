var graph = angular.module('graph', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

graph.controller('GraphController', function($rootScope, $scope, $http) {

    $http.get('/data/')
    .success(function(data, status, headers, config, statusText) {
        // heatmapLayer.setData(data);
    });

    $scope.filters = {
        times: [
            {
                text: "Mañana (6:00 - 11:59)",
                value: 6,
                checked: true
            },{
                text: "Tarde (12:00 - 19:59)",
                value: 12,
                checked: true
            },{
                text: "Noche (20:00 - 5:59)",
                value: 20,
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
        config = {}
        config.params = { data:$scope.filters }
        $http.get('/data/', config)
        .success(function(data, status, headers, config, statusText) {
            heatmapLayer.setData(data);
        })
        .error(function(data, status, headers, config) {
          console.log(data);
        });
        console.log(target);
    };
});

graph.controller('PanelController', function($rootScope, $scope, $http) {

});
