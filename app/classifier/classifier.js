'use strict';

angular.module('corpusaurus.classifier', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/classifier', {
    templateUrl: 'classifier/classifier.html',
    controller: 'ClassifierCtrl'
  });
}])

.controller('ClassifierCtrl', [function() {

}]);
