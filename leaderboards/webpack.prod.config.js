var path = require('path');
var glob = require('fast-glob');
var Merge = require('webpack-merge');
var BaseConfig = require('./webpack.base.config.js');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
var PurifyCSSPlugin = require('purifycss-webpack');
var cssnano = require('cssnano');
var buildPath = path.resolve('./static/bundles/production/');

module.exports = function(env){
    return Merge(BaseConfig, {
        output: {
            path: buildPath,
        },

        //Render source-map file for final build
        devtool: 'source-map',

        plugins: [
            // removes a lot of debugging code in libraries like React
            new webpack.DefinePlugin({
                'process.env': {
                  'NODE_ENV': JSON.stringify('production')
                }
            }),
            //Minify JS bundle
            new webpack.optimize.UglifyJsPlugin({
              minimize: true,
              compress: {
                //supresses warnings, usually from module minification
                warnings: false
              }
            }),
            // Remove unused CSS by looking for usage in .html templates (could include .js files or any others)
            new PurifyCSSPlugin({
                paths: glob.sync('*/templates{,*,*/*}/*.html'),
                purifyOptions: {
                    whitelist: ['aos-init', 'aos-animate', 'icon-*'],
                }
            }),
            // Minify CSS bundle
            new OptimizeCSSAssetsPlugin({
              cssProcessor: cssnano,
              cssProcessorOptions: {
                discardComments: {
                    removeAll: true
                },
                safe: true
              },
              canPrint: false,
            }),
            new BundleTracker({filename: './webpack-prod-stats.json'}),
        ]
    })
}