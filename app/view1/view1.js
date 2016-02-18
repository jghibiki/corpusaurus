'use strict';

angular.module('myApp.view1', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view1', {
    templateUrl: 'view1/view1.html',
    controller: 'View1Ctrl'
  });
}])

.controller('View1Ctrl', ["$scope", "file", function($scope, file) {

    $scope.headers = [];
    $scope.data = [];
    $scope.newCol = "";

    $scope.addCol = function(){
        $scope.headers.push($scope.newCol);
        $scope.newCol = "";

        for(var row_id in $scope.data){
            $scope.data[row_id].push("")
        }
    }

    $scope.addRow = function(){
        var row = [];
        for(var col in $scope.headers){
            row.push(""); 
        }
        $scope.data.push(row);
    }
    
    $scope.downloadCSV = function(){

        var send_data = {
            data: $scope.data,
            headers: $scope.headers
        };


        console.log(send_data);

        file.csv(send_data, function(response){
            download(response.data, "data.csv", "text/csv");
        });
    }
}]);
