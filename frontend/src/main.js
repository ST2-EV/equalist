import { createApp } from 'vue'

import titleMixin from './components/mixins/titleMixin'
import piratepx from './components/mixins/piratepx'

import App from './App.vue'
import './registerServiceWorker'
import router from './router'

import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';


createApp(App).use(router).mixin(titleMixin).mixin(piratepx).use(VueSweetalert2).mount("#app")

