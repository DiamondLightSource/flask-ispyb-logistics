import Vue from 'vue'
import Stores from '../../views/Stores.vue'
import store from '../../store'

import 'fontsource-cantarell/latin.css'
import 'tailwindcss/tailwind.css'
import axios from 'axios'

Vue.config.productionTip = false

Vue.prototype.$http = axios

new Vue({
  store,
  render: h => h(Stores)
}).$mount('#app')
