app.controller('controller', ['$scope', '$http', function ($scope, $http) {
    $scope.submissionForm = {};

    $http.get("/api/categoricals/source?limit=100").then(function (response) {
        $scope.sources = response.data;
    });

    $http.get("/api/categoricals/expressionHost?limit=100").then(function (response) {
        $scope.hosts = response.data;
    });

    $scope.submitForm = function(event) {
        console.log(event);
        console.log($scope.submissionForm);

        $http.post("/api/pdbfilter", $scope.submissionForm).then(function(response) {
            console.log(response.data);
        });
    };
}]);