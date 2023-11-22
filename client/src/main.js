import { createApp } from 'vue'
import App from './App.vue'
import { store } from './store'

import '@fontsource/cantarell'
import 'tailwindcss/tailwind.css'
import axios from 'axios'

import 'font-awesome/css/font-awesome.css'

const app = createApp(App)

app.use(store)

app.mount('#app')
