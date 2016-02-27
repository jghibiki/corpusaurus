'use strict';

angular.module('corpusaurus.version', [
  'corpusaurus.version.interpolate-filter',
  'corpusaurus.version.version-directive'
])

.value('version', '0.2');
