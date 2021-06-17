import Vue from 'vue'
import App from './App.vue'
import router from './router'
// import store from './store'   // In the future, we might want to use the store

import Buefy from 'buefy'
import '@mdi/font/css/materialdesignicons.css'

import { BootstrapVue } from 'bootstrap-vue'


require('@/assets/scss/custom.scss')
Vue.use(Buefy)
Vue.use(BootstrapVue)
Vue.config.productionTip = false

new Vue({
  router,
  // store,
  render: h => h(App)
}).$mount('#app')
