import { createApp } from 'vue'
import Lab14 from '../../views/Lab14.vue'
import { store } from '../../store.js'

import '@fontsource/cantarell'
import '@/assets/tailwind.css'

// Initialise the store with our zone
store.commit('setZone', 'lab14')

const app = createApp(Lab14)

app.use(store)

app.mount('#app')
