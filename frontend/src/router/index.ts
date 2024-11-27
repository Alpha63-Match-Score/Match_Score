import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/events',
      name: 'events',
      component: () => import('../views/TournamentList.vue'),
    },
    {
      path: '/matches',
      name: 'matches',
      component: () => import('../views/MatchList.vue'),
    },
    {
      path: '/teams',
      name: 'teams',
      component: () => import('../views/TeamList.vue'),
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  //    {
  //   path: '/dashboard-user',
  //   name: 'dashboard-user',
  //   component: () => import('../views/DashboardUser.vue'),
  // },
  // {
  //   path: '/dashboard-admin',
  //   name: 'dashboard-admin',
  //   component: () => import('../views/DashboardAdmin.vue'),
  // },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardAdmin.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LogIn.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue')
    }
  ],
})

export default router
