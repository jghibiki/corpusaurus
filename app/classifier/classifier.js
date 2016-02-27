'use strict';

angular.module('corpusaurus.classifier', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/classifier', {
    templateUrl: 'classifier/classifier.html',
    controller: 'ClassifierCtrl'
  });
}])

.controller('ClassifierCtrl', ["$scope", "$http", function($scope, $http) {
    $scope.loading = true;
    $scope.elementsToClassify = "<Loading...>";
    $scope.start = null;
    $scope.stop = null;
    $scope.progress = null;
    $scope.total = null;
    $scope.initialized = false;
    $scope.done = false;

    $scope.tweet = null;

    $scope.markExample = function(){
        classifyTweet("example");
    }

    $scope.markNotExample = function(){
        classifyTweet("nonexample");
    }

    $scope.markUnkown = function(){
        classifyTweet("unknown");
    }

    $scope.initialize = function(){
        $scope.loading = true;
        $scope.progress = 0;
        $scope.total = $scope.stop - $scope.start + 1;
        $http.post('api/classification/range/' + $scope.start + "/" + $scope.stop + "/")
        .then(getNext, function(resp){
            console.log(resp);
            alert("error");
        });
    }

    $http.get('api/classification/element/count/')
    .then(function(resp){
        $scope.elementsToClassify = resp.data.result; 
        $scope.loading = false;
    }, function(resp){
        console.log(resp);
        alert("Error"); 
    });

    function getNext(){
        if($scope.progress !== $scope.total){
            $http.get('api/classification/element/')
            .then(function(resp){
                $scope.progress = $scope.progress + 1;
                $scope.tweet = resp.data.result
                    .replace("&amp;", "&")
                    .replace(/https:\/\/t.co\/[A-Za-z-0-9]+/gi, "<URL> ");
                $scope.initialized = true;
                $scope.loading = false;
            }, function(resp){
                console.log(resp);
                alert("error");
            });
        }
        else{
            $scope.done = true;
        }
    }

    function classifyTweet(classification){
        $scope.loading = true;
        $http.post('api/classification/element/classify/' + classification + "/")
        .then(getNext, function(resp){
            console.log(resp);
            alert("error");
        });
    }


}]);
