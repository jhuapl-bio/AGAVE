import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import DataView from '@/views/DataView.vue'
import AboutView from '@/views/AboutView.vue'
//https://github.com/bbachi/vuejs-nodejs-typescript-example usage of code borrowed short term from for immediate testing
// as well as https://github.com/jhuapl-bio/Basestack/blob/main/client/src
Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Data',
    component: DataView
  },
  {
    path: '/about',
    name: 'About',
    component: AboutView
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
