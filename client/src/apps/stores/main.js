import { createApp } from 'vue'
import Stores from '../../views/Stores.vue'
import { store } from '../../store.js'

import '@fontsource/cantarell'
import '@/assets/tailwind.css'

const app = createApp(Stores)

app.use(store)

app.mount('#app')
