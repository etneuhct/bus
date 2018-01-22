var path = require("path");
var fs = require('fs');
var webpack = require('webpack');
var glob = require('fast-glob');
var entries = require('./webpack-entries-dirs.js');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var buildPath = path.resolve(__dirname, './static/bundles/dev/');
var nodeModulesPath = path.resolve(__dirname, 'node_modules');

module.exports = {
  context: __dirname,

  entry: function(){
       var zero = [
			'bootstrap/css/bootstrap.css',
			'site/css/main.css',
			'bootstrap/js/bootstrap.js',
			'site/js/site.js'
       ];

       var entry = {
            zero: entries(zero),
       };
       console.log('Entry:', entry);
       return entry;
  }, // if using directories as `entry`, they should have a `index.js` file that require all the assets used.

  output: {
    filename: '[name].js',
    path: buildPath
  },

  devtool: 'eval',

  plugins: [
    new ExtractTextPlugin({
        filename: '[name].css',
        allChunks: true
    }),
	
	// feel free to get rid of the frameworks you don't use
    new webpack.ProvidePlugin({
        'glbl.jQuery': 'jquery',
        $: 'jquery',
        ko: 'knockout'
    })
  ],

  module: {
    //Loaders to interpret non-vanilla javascript code as well as most other extensions including images and text.
    rules: [
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract({
            loader: 'css-loader?importLoaders=1'
        })
      },
      {
        test: /fonts[\\\/].+\.(eot|ttf|otf|woff|woff2|svg)(?:\?v=\d+\.\d+\.\d+|[a-z0-9]+)?$/,
        use: {
            loader: 'url-loader',
            options: {
                // if size < 10kb use dataURL
                limit: 10000,
                name: 'fonts/[name].[ext]',
                publicPath: './',
            }
        },
      },
      { test: /\.json$/, loader: 'json' },
    ]
  },

  resolve: {
    alias: {
		// feel free to get rid of the frameworks you don't need.
        jquery: path.resolve(__dirname, './frameworks/static/js/jquery.min.js'),
        knockout: path.resolve(__dirname, './frameworks/static/js/knockout.min.js'),
        moment: path.resolve(__dirname, './frameworks/static/js/moment.min.js'),
    },
    modules: [
        'node_modules',
    ],
    extensions: ['.js', '.jsx', 'json']
  },
}