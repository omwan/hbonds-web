app.controller('controller', ['$scope', '$http', function ($scope, $http) {
    $scope.filters = [];

    $scope.columns = {};

    $scope.header = "";

    $http.get("/api/categoricals/source?limit=100").then(function (response) {
        $scope.columns["source"] = response.data;
    });

    $http.get("/api/categoricals/expressionHost?limit=100").then(function (response) {
        $scope.columns["expressionHost"] = response.data;
    });

    $scope.addFilter = function (event) {
        var label = "";
        if ($scope.header === "source") {
            label = "Source Organism";
        } else if ($scope.header === "expressionHost") {
            label = "Expression Host"
        }
        $scope.filters.push({header: $scope.header, label: label});
    };

    $scope.submitForm = function (event) {
        console.log($scope.filters);

        $http.post("/api/pdbfilter", $scope.filters).then(function (response) {
            console.log(response.data);
        });
    };
}]);