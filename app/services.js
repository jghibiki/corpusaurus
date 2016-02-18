'use strict';

var corpServices = angular.module("corpServices", []);

corpServices.factory("file", ["$resource", function($resource){
    var fileService = {};

    fileService._xhr = $resource("api/files/:fileType", {}, {
        csv: { method: "POST", params: {fileType: "csv"}, isArray: false},
        xls: { method: "POST", params: {fileType: "xls"}, isArray: false}
    });

    fileService.csv = function(data, callback){
        var response = this._xhr.csv(data, function(response){
            callback(response);
        });
    };

    fileService.xls = function(data, callback){
        var response = this._xhr.xls(data, function(response){
            callback(response);
        });
    };

    return fileService;
}]);

