'use strict';

angular.module('corpusaurus.classifier', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/classifier', {
    templateUrl: 'classifier/classifier.html',
    controller: 'ClassifierCtrl'
  });
}])

.controller('ClassifierCtrl', ["$scope", function($scope) {
    $scope.currentTweet = "trump...."; 

    $scope.markExample = function(){
        alert("example");
    }

    $scope.markNotExample = function(){
        alert("nonexample");
    }

    $scope.markUnkown = function(){
        alert("unkown");
    }
}]);
