import { createApp } from 'vue'
import Stores from '../../views/Stores.vue'
import { store } from '../../store.js'

import '@fontsource/cantarell'
import '@/assets/tailwind.css'
import axios from 'axios'

const app = createApp(Stores)

app.use(store)
app.config.globalProperties.$http = axios

app.mount('#app')
