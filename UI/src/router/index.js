import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import App from '../App.vue'
import Statistics from '../components/Statistics.vue'
import MainLayout from '../layouts/MainLayout.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: App
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: Statistics
      },
      {
        path: '',
        redirect: '/dashboard'
      }
    ]
  },
  {
    path: '/dashboard',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegación para proteger rutas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('auth_token')
  
  if (to.meta.requiresAuth && !token) {
    // Si requiere autenticación y no hay token, redirigir a login
    next('/login')
  } else if (to.path === '/login' && token) {
    // Si ya está autenticado y va a login, redirigir a dashboard
    next('/')
  } else {
    next()
  }
})

export default router

