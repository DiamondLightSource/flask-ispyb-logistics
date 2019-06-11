import Vue from 'vue'
import Stores from '../../views/Stores.vue'
import store from '../../store'

import 'bulma/css/bulma.css'
import axios from 'axios'

Vue.config.productionTip = false

Vue.prototype.$http = axios

new Vue({
  store,
  render: h => h(Stores)
}).$mount('#app')
