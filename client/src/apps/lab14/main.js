import Vue from 'vue'
import Lab14 from '../../views/Lab14.vue'
import store from '../../store'

import 'typeface-cantarell'
import 'tailwindcss/tailwind.css'
import axios from 'axios'

Vue.config.productionTip = false

Vue.prototype.$http = axios

// Initialise the store with our zone
store.commit('setZone', 'lab14')

new Vue({
  store,
  render: h => h(Lab14)
}).$mount('#app')
