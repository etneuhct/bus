var fs = require('fs');
var path = require('path');
var config = require(path.resolve(__dirname, 'config.json'));

var APP_DIRS = config["django_apps"].map(function(app){
    return path.resolve(__dirname, app, 'static');
});
console.log(APP_DIRS);
var ASSETS_DIRS = [
    path.resolve(__dirname, 'src', 'frameworks', 'static'),
    path.resolve(__dirname, 'src', '{{project_name}}', 'static'),
];
ASSETS_DIRS = APP_DIRS.concat(ASSETS_DIRS);

module.exports = function(assetPaths){
    if (!ASSETS_DIRS[0]){
        throw('No directory in ASSETS_DIRS to resolve entries from.')
    }
    var resolvedEntries = [];
    assetPaths.map(function(asset){
        var resolvedPath = path.resolve(ASSETS_DIRS[0], asset);
        var isAssetFound = false;
        for (var i=0; i<ASSETS_DIRS.length; i++){
            if (fs.existsSync(resolvedPath)){
                isAssetFound = true;
                break
            }
            if (ASSETS_DIRS[i+1]){
                resolvedPath = path.resolve(ASSETS_DIRS[i+1], asset);
            }
        }

        if (isAssetFound){
            resolvedEntries.push(resolvedPath);
        }
    });
    return resolvedEntries;
}
