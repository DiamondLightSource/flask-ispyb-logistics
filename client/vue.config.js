module.exports = {
    devServer: {
      proxy: {
        '^/api': {
          target: 'http://localhost:8008',
          ws: true,
          changeOrigin: true
        }
      },
    },
    assetsDir: 'static'
}