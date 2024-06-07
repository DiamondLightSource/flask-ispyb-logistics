import { createApp } from 'vue'
import Dewars from '../../views/Dewars.vue'
import { store } from '../../store'

import '@fontsource/cantarell'
import 'tailwindcss/tailwind.css'
import axios from 'axios'

import 'font-awesome/css/font-awesome.css'

// Initialise the store with our zone
store.commit('setZone', 'cage')

const app = createApp(Dewars)

app.use(store)
app.config.globalProperties.$http = axios

app.mount('#app')
