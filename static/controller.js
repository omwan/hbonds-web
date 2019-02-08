app.controller('controller', ['$scope', '$http', function ($scope, $http) {

    $http.get("/api/hello").then(function(response) {
        $scope.hello = response.data.text;
    });
}]);