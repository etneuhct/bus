var Merge = require('webpack-merge');
var BaseConfig = require('./webpack.base.config');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');


module.exports = function(env){
  return Merge(BaseConfig, {
      output: {
          publicPath: 'http://localhost:3000/assets/bundles/'
      },
        //Server Configuration options
      devServer:{
        publicPath: 'http://localhost:3000/assets/bundles/',  //Relative directory for base of server
        hot: true,        //Live-reload
        inline: true,
        port: 3000,        //Port Number
        headers: {'Access-Control-Allow-Origin': '*'}
      },

      devtool: 'eval',

      plugins: [
        //Enables Hot Modules Replacement
        new webpack.HotModuleReplacementPlugin(),
        //Allows error warnings but does not stop compiling. Will remove when eslint is added
        new webpack.NoEmitOnErrorsPlugin(),
        new BundleTracker({filename: './webpack-stats.json'}),
      ],
  })
}