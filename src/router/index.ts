import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import DataView from '@/views/DataView.vue'
import AboutView from '@/views/AboutView.vue'

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
