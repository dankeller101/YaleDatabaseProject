
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
		// loaders: [
		// 	{
		
		// 		exclude: /node_modules/,
		// 		include: APP_DIR,
		// 		loader: 'babel',
		// 		query: {
	 //        presets:['react']
	 //      }
		// 	}
		]
	},
	output: {
		path: BUILD_DIR,
		filename: 'bundle.js'
	},
};

module.exports = config;