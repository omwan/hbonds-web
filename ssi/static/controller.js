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

    //set ligand ID values from het ID values
    let _setLigands = function (response) {
        $scope.columns["ligandId"] = response.data.map(function (val) {
            return {
                "header": "ligandId",
                "value": val["value"]
            }
        });
    };

    //retrieve filters + filename/count from cache if they exist
    let _setScopeFromCache = function () {
        if (window.sessionStorage.getItem("filters")) {
            $scope.filters = JSON.parse(window.sessionStorage.getItem("filters"));
        }
        if (window.sessionStorage.getItem("filename")) {
            $scope.filename = window.sessionStorage.getItem("filename");
        }
        if (window.sessionStorage.getItem("count")) {
            $scope.count = window.sessionStorage.getItem("count");
        }
        if (window.sessionStorage.getItem("query")) {
            $scope.query = window.sessionStorage.getItem("query");
        }
    };

    //initalization function to populate categorical dropdowns
    let _init = function () {
        categorical_apis.forEach(function (cat) {
            $http.get("/api/categoricals/" + cat + "?limit=100").then(function (response) {
                $scope.columns[cat] = response.data;
                if (cat === "hetId") {
                    _setLigands(response);
                }
            });
        });

        categorical_statics.forEach(function (cat) {
            $http.get("/static/" + cat + ".json").then(function (response) {
                $scope.columns[cat] = response.data;
            });
        });

        _setScopeFromCache();
    };

    //add another filter to the model
    $scope.addFilter = function (event) {
        let newFilter = {
            header: $scope.header,
            label: $scope.labels[$scope.header],
            filtered: false,
            numerical: numericals.indexOf($scope.header) >= 0,
            bool: "and"
        };

        if (!newFilter["numerical"]) {
            newFilter["name"] = $scope.columns[newFilter["header"]][0].value
        } else {
            newFilter["comparator"] = "<";
        }
        $scope.filters.push(newFilter);
        $scope.cacheFilters();
    };

    //delete a filter from the model
    $scope.deleteFilter = function (event, index) {
        $scope.filters.splice(index, 1);
        $scope.cacheFilters();
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
            $scope.count = response.data.count;
            $scope.query = response.data.query;
            $scope.isLoading = false;
            window.sessionStorage.setItem("filters", JSON.stringify($scope.filters));
            window.sessionStorage.setItem("filename", $scope.filename);
            window.sessionStorage.setItem("count", $scope.count);
            window.sessionStorage.setItem("query", $scope.query);
            window.location.href = "?file=" + response.data.filename;
        }).finally(function (response) {
            $scope.isLoading = false;
        });
    };

    //save filters to cache
    $scope.cacheFilters = function () {
        window.sessionStorage.setItem("filters", JSON.stringify($scope.filters));
    };

    //retrieve generated file from server + download in browser
    $scope.downloadFilter = function (event) {
        window.open("/api/filters/" + $scope.filename);
    };

    //delete filters from cache + delete generated files from server
    $scope.clearFilters = function (event) {
        $scope.isLoading = true;
        $http.delete("/api/filters/" + $scope.filename).then(function (response) {
            $scope.filters = [];
            $scope.filename = "";
            window.sessionStorage.clear();
            window.location.href = "/";
        }).finally(function (response) {
            $scope.isLoading = false;
        });
    };

    _init();
}]);
