const path = require('path');

module.exports = {
  entry: './src/index.js', // Entry point of your application
  output: {
    path: path.resolve(__dirname, 'static'), // Output directory
    filename: 'bundle.js' // Name of the output bundle
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader', // Transpiles JavaScript using Babel
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'] // Presets for ES6/React
          }
        }
      },
      {
        test: /\.css$/, // Handles CSS files
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx'] // File extensions to resolve
  }
};
