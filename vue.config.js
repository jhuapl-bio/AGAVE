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
  }
}
