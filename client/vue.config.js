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
    assetsDir: 'static',
    pages: {
      index: {
        // entry for the page
        entry: 'src/main.js',
        // the source template
        template: 'public/index.html',
        // output as dist/index.html
        filename: 'index.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'ISPyB Logistics App',
        // chunks to include on this page, by default includes
        // extracted common chunks and vendor chunks.
        chunks: ['chunk-vendors', 'chunk-common', 'index']
      },
      stores: {
        // entry for the page
        entry: 'src/apps/stores/main.js',
        // the source template
        template: 'public/index.html',
        // output as dist/index.html
        filename: 'stores.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'ISPyB Logistics Stores',
        // chunks to include on this page, by default includes
        // extracted common chunks and vendor chunks.
        chunks: ['chunk-vendors', 'chunk-common', 'stores']
      },
      ebic: {
        // entry for the page
        entry: 'src/apps/ebic/main.js',
        // the source template
        template: 'public/index.html',
        // output as dist/index.html
        filename: 'ebic.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'ISPyB Logistics EBIC',
        // chunks to include on this page, by default includes
        // extracted common chunks and vendor chunks.
        chunks: ['chunk-vendors', 'chunk-common', 'ebic']
      },
      zone4: {
        // entry for the page
        entry: 'src/apps/zone4/main.js',
        // the source template
        template: 'public/index.html',
        // output as dist/index.html
        filename: 'zone4.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'ISPyB Logistics Zone4',
        // chunks to include on this page, by default includes
        // extracted common chunks and vendor chunks.
        chunks: ['chunk-vendors', 'chunk-common', 'zone4']
      },
      zone6: {
        // entry for the page
        entry: 'src/apps/zone6/main.js',
        // the source template
        template: 'public/index.html',
        // output as dist/index.html
        filename: 'zone6.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'ISPyB Logistics Zone6',
        // chunks to include on this page, by default includes
        // extracted common chunks and vendor chunks.
        chunks: ['chunk-vendors', 'chunk-common', 'zone6']
      },
      lab14: {
        // entry for the page
        entry: 'src/apps/lab14/main.js',
        // the source template
        template: 'public/index.html',
        // output as dist/index.html
        filename: 'lab14.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'ISPyB Logistics Lab14',
        // chunks to include on this page, by default includes
        // extracted common chunks and vendor chunks.
        chunks: ['chunk-vendors', 'chunk-common', 'lab14']
      },
      cage: {
        entry: 'src/apps/cage/main.js',
        template: 'public/index.html',
        filename: 'cage.html',
        title: 'SLS Logistics',
        chunks: ['chunk-vendors', 'chunk-common', 'cage']
      }
    }
}
