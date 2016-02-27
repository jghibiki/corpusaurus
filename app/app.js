'use strict';

// Declare app level module which depends on views, and components
angular.module('corpusaurus', [
  'ngRoute',
  'ngResource',
  'corpServices',
  'corpusaurus.editor',
  'corpusaurus.classifier',
  'corpusaurus.version'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/classifier'});
}]);
