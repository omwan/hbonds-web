app.controller('controller', ['$scope', '$http', function ($scope, $http) {
    $scope.filters = [];
    $scope.columns = {};
    $scope.header = "";

    $scope.labels = {
        "source": "Source Organism",
        "expressionHost": "Expression Host",
        "averageBFactor": "Average B Factor",
        "residueCount": "Residue Count",
        "chainLength": "Chain Length",
        "refinementResolution": "Resolution"
    };

    $scope.isLoading = false;

    let numericals = ["averageBFactor", "residueCount", "chainLength", "refinementResolution"];

    $http.get("/api/categoricals/source?limit=100").then(function (response) {
        $scope.columns["source"] = response.data;
    });

    $http.get("/api/categoricals/expressionHost?limit=100").then(function (response) {
        $scope.columns["expressionHost"] = response.data;
    });

    $scope.addFilter = function (event) {
        $scope.filters.push({
            header: $scope.header,
            label: $scope.labels[$scope.header],
            filtered: false,
            numerical: numericals.indexOf($scope.header) >= 0
        });
    };

    $scope.deleteFilter = function(event, index) {
        $scope.filters.splice(index, 1);
    };

    $scope.submitForm = function (event) {
        console.log($scope.filters);
        $scope.isLoading = true;
        $http.post("/api/pdbfilter", $scope.filters).then(function (response) {
            $scope.filename = response.data.filename;
            $scope.isLoading = false;
        });
    };

    $scope.downloadFilter = function(event) {
        window.open("/api/filters/" + $scope.filename);
    };
}]);
