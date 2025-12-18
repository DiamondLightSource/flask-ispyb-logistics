import { createApp } from 'vue'
import Dewars from '../../views/Dewars.vue'
import { store } from '../../store.js'

import '@fontsource/cantarell'
import '@/assets/tailwind.css'

import 'font-awesome/css/font-awesome.css'

// Initialise the store with our zone
store.commit('setZone', 'cage')

const app = createApp(Dewars)

app.use(store)

app.mount('#app')
