//controller for angular app
app.controller('controller', ['$scope', '$http', function ($scope, $http) {
    $scope.filters = [];
    $scope.columns = {};
    $scope.header = "";
    $scope.isLoading = false;
    $scope.labels = {
        "source": "Source Organism",
        "expressionHost": "Expression Host",
        "averageBFactor": "Average B Factor",
        "residueCount": "Residue Count",
        "chainLength": "Chain Length",
        "refinementResolution": "Resolution",
        "residue": "Contains Residue",
        "Type": "Hydrogen Bond Type"
    };

    let numericals = ["averageBFactor", "residueCount", "chainLength", "refinementResolution"];

    //initalization function to populate categorical dropdowns
    var _init = function () {
        $http.get("/api/categoricals/source?limit=100").then(function (response) {
            $scope.columns["source"] = response.data;
        });

        $http.get("/api/categoricals/expressionHost?limit=100").then(function (response) {
            $scope.columns["expressionHost"] = response.data;
        });

        $http.get("/static/residues.json").then(function (response) {
            $scope.columns["residue"] = response.data;
        });

    };

    //add another filter to the model
    $scope.addFilter = function (event) {
        $scope.filters.push({
            header: $scope.header,
            label: $scope.labels[$scope.header],
            filtered: false,
            numerical: numericals.indexOf($scope.header) >= 0
        });
    };

    //delete a filter from the model
    $scope.deleteFilter = function (event, index) {
        $scope.filters.splice(index, 1);
    };

    //disable the submit button if there are no filters or there is a
    //numerical filter with an empty comparedValue field
    $scope.submitDisabled = function () {
        let emptyFilters = $scope.filters.filter(function (f) {
            return f["numerical"] && !("comparedValue" in f);
        }).length > 0;
        return $scope.filters.length === 0 || emptyFilters;
    };

    //post form to server
    $scope.submitForm = function (event) {
        $scope.isLoading = true;
        $http.post("/api/pdbfilter", $scope.filters).then(function (response) {
            $scope.filename = response.data.filename;
            $scope.isLoading = false;
        }).finally(function (response) {
            $scope.isLoading = false;
        });
        console.log($scope.filters);
    };

    //retrieve generated file from server + download in browser
    $scope.downloadFilter = function (event) {
        window.open("/api/filters/" + $scope.filename);
    };

    _init();
}]);
