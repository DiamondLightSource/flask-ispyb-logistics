import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Stores from './views/Stores.vue'
import Dewars from './views/Dewars.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/zone4',
      name: 'Zone4',
      component: Dewars,
      props: {zone: 'zone4'}
    },
    {
      path: '/zone6',
      name: 'Zone6',
      component: Dewars,
      props: {zone: 'zone6'}
    },
    {
      path: '/stores',
      name: 'Stores',
      component: Stores
    },
    {
      path: '/ebic',
      name: 'EBIC',
      component: Dewars,
      props: {zone: 'ebic'}
    }
  ]
})
