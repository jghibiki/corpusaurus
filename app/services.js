'use strict';

var corpServices = angular.module("corpServices", []);

corpServices.factory("file", ["$resource", function($resource){
    var fileService = {};

    fileService._xhr = $resource("api/files/:fileType", {}, {
        csv: { method: "POST", params: {fileType: "csv"},  isArray: false}
    });

    fileService.csv = function(data, callback){
        var response = this._xhr.csv(data, function(response){
            callback(response);
        });
    };

    return fileService;
}]);

