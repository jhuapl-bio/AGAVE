const path = require('path');
module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
    ? '/BARDA/'
    : '/',
  css: {
    loaderOptions: {
      sass: {
        prependData: `
            @import "@/assets/scss/custom.scss";
            `
      }
    }
  },
  chainWebpack: config => {
    config.module
      .rule("csv")
      .test(/\.(csv|tsv|txt)$/)
      .use("csv-loader")
      .loader("csv-loader")
      .options({
        dynamicTyping: true,
        header: true,
        skipEmptyLines: true
      })
      .end();
  }, 
  configureWebpack: {
    resolve: {
      alias: {
        lib: path.resolve(__dirname, 'public/lib')
      }
    } 
  }
}
