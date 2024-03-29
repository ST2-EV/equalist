import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Callback from '../views/Callback.vue'
import Waiting from '../views/Waiting.vue'
import Join from '../views/Join.vue'
import Success from '../views/Success.vue'
import PageNotFound from '../views/PageNotFound.vue'
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/callback',
    name: 'Callback',
    component: Callback
  },
  {
    path: '/waiting-room',
    name: 'Waiting',
    component: Waiting
  },
  {
    path: '/j/:id',
    name: 'Join',
    component: Join
  },
  {
    path: '/success',
    name: 'Success',
    component: Success
  },
  {
    path:"/:catchAll(.*)",
    name: 'pageNotFound',
    component: PageNotFound
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
