//controller for angular app
app.controller('controller', ['$scope', '$http', function ($scope, $http) {
    $scope.filters = [];
    $scope.columns = {};
    $scope.header = "";
    $scope.isLoading = false;
    $scope.labels = {
        "Type": "Bond Type",
        "cb.cb": "cb.cb",
        "sc_.exp_avg": "sc_.exp_avg",
        "hb_energy": "Bond Energy",
        "residue": "Contains Residue",
        "expressionHost": "Expression Host",
        "source": "Source Organism",
        "refinementResolution": "Resolution",
        "averageBFactor": "Average B Factor",
        "chainLength": "Chain Length",
        "ligandId": "Ligand ID",
        "hetId": "Het ID",
        "residueCount": "Residue Count"
    };

    let numericals = ["averageBFactor", "residueCount", "chainLength",
        "refinementResolution", "cb.cb", "sc_.exp_avg", "hb_energy"];
    let categorical_apis = ["source", "expressionHost", "hetId"];
    let categorical_statics = ["residue", "Type"];

    //initalization function to populate categorical dropdowns
    var _init = function () {
        if (!window.sessionStorage.getItem("columns")) {
            categorical_apis.forEach(function (cat) {
                $http.get("/api/categoricals/" + cat + "?limit=100").then(function (response) {
                    $scope.columns[cat] = response.data;
                    if (cat === "hetId") {
                        $scope.columns["ligandId"] = response.data.map(function (val) {
                            return {
                                "header": "ligandId",
                                "value": val["value"]
                            }
                        });
                    }
                });
            });

            categorical_statics.forEach(function (cat) {
                $http.get("/static/" + cat + ".json").then(function (response) {
                    $scope.columns[cat] = response.data;
                });
            });
        } else {
            $scope.columns = JSON.parse(window.sessionStorage.getItem("columns"));
            $scope.filters = JSON.parse(window.sessionStorage.getItem("filters"));
            $scope.filename = window.sessionStorage.getItem("filename");
        }
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
            return f["numerical"] &&
                (!("comparedValue" in f) || f["comparedValue"] === "");
        }).length > 0;
        return $scope.filters.length === 0 || emptyFilters;
    };

    //post form to server
    $scope.submitForm = function (event) {
        $scope.isLoading = true;
        $http.post("/api/pdbfilter", $scope.filters).then(function (response) {
            $scope.filename = response.data.filename;
            $scope.isLoading = false;
            window.sessionStorage.setItem("filters", JSON.stringify($scope.filters));
            window.sessionStorage.setItem("filename", $scope.filename);
            if (!window.sessionStorage.getItem("columns")) {
                window.sessionStorage.setItem("columns", JSON.stringify($scope.columns));
            }
        }).finally(function (response) {
            $scope.isLoading = false;
        });
    };

    //retrieve generated file from server + download in browser
    $scope.downloadFilter = function (event) {
        window.open("/api/filters/" + $scope.filename);
    };

    _init();
}]);
