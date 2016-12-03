
var webpack = require('webpack');
var path = require('path');

var BUILD_DIR = path.resolve(__dirname, 'public');
var APP_DIR = path.resolve(__dirname, 'app');

var config = {
	entry: APP_DIR + '/index.jsx',
	module: {
		loaders: [
			{
				test: /.jsx?$/,
				loader: 'babel-loader',
				include: APP_DIR,
				exclude: /node_modules/,
				query: {
					presets: ['es2015', 'react']
				}
			}
		]
	},
    resolve: {
        modulesDirectories: ['public/js', 'node_modules']
    },
	output: {
		path: BUILD_DIR,
		filename: 'bundle.js'
	},
};

module.exports = config;