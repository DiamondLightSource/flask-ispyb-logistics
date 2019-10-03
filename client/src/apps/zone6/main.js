import Vue from 'vue'
import Dewars from '../../views/Dewars.vue'
import store from '../../store'

import 'typeface-cantarell'
import 'tailwindcss/tailwind.css'
import axios from 'axios'

Vue.config.productionTip = false

Vue.prototype.$http = axios

// Initialise the store with our zone
store.commit('setZone', 'zone6')

new Vue({
  store,
  render: h => h(Dewars)
}).$mount('#app')
