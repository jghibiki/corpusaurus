'use strict';

angular.module('corpusaurus.editor', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/editor', {
    templateUrl: 'editor/editor.html',
    controller: 'EditorCtrl'
  });
}])

.controller('EditorCtrl', ["$scope", "file", function($scope, file) {

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


    $scope.downloadXLS = function(){

        var send_data = {
            data: $scope.data,
            headers: $scope.headers
        };

        console.log(send_data);

        file.xls(send_data, function(response){
            download(response.data, "data.xls", "application/vnd.ms-excel");
        });
    }
}]);
