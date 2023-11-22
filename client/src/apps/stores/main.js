import Vue from 'vue'
import Stores from '../../views/Stores.vue'
import { store } from '../../store'

import '@fontsource/cantarell'
import 'tailwindcss/tailwind.css'
import axios from 'axios'

const app = createApp(App)

app.use(store)

app.mount('#app')
