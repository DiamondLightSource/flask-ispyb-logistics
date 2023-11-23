import { createApp } from 'vue'
import Stores from '../../views/Stores.vue'
import { store } from '../../store'

import '@fontsource/cantarell'
import 'tailwindcss/tailwind.css'
import axios from 'axios'

const app = createApp(Stores)

app.use(store)
app.use(axios)

app.mount('#app')
