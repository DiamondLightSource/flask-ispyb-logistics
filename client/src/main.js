import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'


import 'bulma/css/bulma.css'
import axios from 'axios'

Vue.config.productionTip = false

Vue.prototype.$http = axios

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
