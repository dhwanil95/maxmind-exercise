const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack');
module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ]
})

module.exports = {
  configureWebpack: {
    plugins: [
      // Work around for Buffer is undefined:
      // https://github.com/webpack/changelog-v5/issues/10
      new webpack.ProvidePlugin({
        Buffer: ['buffer', 'Buffer'],
      })
    
    ],
    resolve: {
      fallback: {
        "https": require.resolve("https-browserify"),
        "http": require.resolve("stream-http"),
        "fs": false,
        "buffer": require.resolve("buffer")
        //"buffer": require.resolve("buffer/").Buffer
      }
    }
  }
}
