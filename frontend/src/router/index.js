import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import ReservationsView from '../views/ReservationsView.vue'
import AdminTablesView from '../views/admin/AdminTablesView.vue'
import AdminReservationsView from '../views/admin/AdminReservationsView.vue'
import AdminUsersView from '../views/admin/AdminUsersView.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/dashboard', name: 'dashboard', component: DashboardView },
  { path: '/reservations', name: 'reservations', component: ReservationsView },
  { path: '/admin/tables', name: 'admin-tables', component: AdminTablesView, meta: { requiresAdmin: true } },
  { path: '/admin/reservations', name: 'admin-reservations', component: AdminReservationsView, meta: { requiresAdmin: true } },
  { path: '/admin/users', name: 'admin-users', component: AdminUsersView, meta: { requiresAdmin: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const token = localStorage.getItem('smartable_token')
  const user = JSON.parse(localStorage.getItem('smartable_user') || '{}')
  
  if (to.meta.requiresAuth && !token) {
    return { name: 'login' }
  }
  if (to.meta.requiresAdmin && user.role !== 'admin') {
    return { name: 'dashboard' }
  }
})

export default router