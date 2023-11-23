import { createApp } from 'vue'
import Dewars from '../../views/Dewars.vue'
import { store } from '../../store'

import '@fontsource/cantarell'
import 'tailwindcss/tailwind.css'
import axios from 'axios'

// Initialise the store with our zone
store.commit('setZone', 'ebic')

const app = createApp(Dewars)

app.use(store)
app.config.globalProperties.$http = axios

app.mount('#app')
