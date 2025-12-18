import { createApp } from 'vue'
import Dewars from '../../views/Dewars.vue'
import { store } from '../../store'

import '@fontsource/cantarell'
import '@/assets/tailwind.css'
import axios from 'axios'

// Initialise the store with our zone
store.commit('setZone', 'zone6')

const app = createApp(Dewars)

app.use(store)
app.config.globalProperties.$http = axios

app.mount('#app')
