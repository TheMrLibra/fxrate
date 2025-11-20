import { createRouter, createWebHistory } from 'vue-router'
import ExchangeRatesView from './views/ExchangeRatesView.vue'
import ConversionView from './views/ConversionView.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/exchange-rates'
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView
    },
    {
      path: '/exchange-rates',
      name: 'ExchangeRates',
      component: ExchangeRatesView,
      meta: { requiresAuth: true }
    },
    {
      path: '/convert',
      name: 'Convert',
      component: ConversionView,
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !token) {
    next('/login')
  } else if (token && (to.path === '/login' || to.path === '/register')) {
    next('/exchange-rates')
  } else {
    next()
  }
})

export default router

