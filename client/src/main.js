import { createApp } from 'vue'
import App from './App.vue'
import { store } from './store.js'

import '@fontsource/cantarell'
import '@/assets/tailwind.css'

import 'font-awesome/css/font-awesome.css'

const app = createApp(App)

app.use(store)

app.mount('#app')
