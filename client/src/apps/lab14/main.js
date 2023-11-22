import Vue from 'vue'
import Lab14 from '../../views/Lab14.vue'
import { store } from '../../store'

import '@fontsource/cantarell'
import 'tailwindcss/tailwind.css'
import axios from 'axios'

// Initialise the store with our zone
store.commit('setZone', 'lab14')

const app = createApp(App)

app.use(store)

app.mount('#app')
