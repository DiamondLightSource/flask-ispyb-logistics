import Vue from 'vue'
import Dewars from '../../views/Dewars.vue'
import { store } from '../../store'

import '@fontsource/cantarell'
import 'tailwindcss/tailwind.css'
import axios from 'axios'

// Initialise the store with our zone
store.commit('setZone', 'ebic')

const app = createApp(App)

app.use(store)

app.mount('#app')
