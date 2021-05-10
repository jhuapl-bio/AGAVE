import Vue from 'vue'
import App from './App.vue'
import router from './router'
// import store from './store'   // In the future, we might want to use the store

import Buefy from 'buefy'

import { BootstrapVue } from 'bootstrap-vue'
Vue.use(BootstrapVue)
import * as d3 from 'd3'
// Vue.use(d3)

require('@/assets/custom.scss')
Vue.use(Buefy)

Vue.config.productionTip = false

new Vue({
  router,
  // store,
  render: h => h(App)
}).$mount('#app')
