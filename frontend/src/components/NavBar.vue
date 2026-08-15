<template>
  <nav class="navbar">
    <div class="brand">🍽 SmarTable</div>
    <div class="links">
      <router-link to="/dashboard">Rezerviraj</router-link>
      <router-link to="/reservations">Moje rezervacije</router-link>
      <template v-if="isAdmin">
        <router-link to="/admin/tables">Stolovi</router-link>
        <router-link to="/admin/reservations">Sve rezervacije</router-link>
        <router-link to="/admin/users">Korisnici</router-link>
      </template>
    </div>
    <div class="user">
      <span>{{ userName }}</span>
      <button @click="logout">Odjava</button>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const user = computed(() => JSON.parse(localStorage.getItem('smartable_user') || '{}'))
const isAdmin = computed(() => user.value.role === 'admin')
const userName = computed(() => user.value.email || '')

function logout() {
  localStorage.removeItem('smartable_token')
  localStorage.removeItem('smartable_user')
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  background: #6e3a24;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.brand {
  color: white;
  font-size: 20px;
  font-weight: bold;
}
.links a {
  color: #f5ead9;
  text-decoration: none;
  margin-right: 18px;
  font-size: 14px;
}
.links a.router-link-active {
  color: #c9974c;
  font-weight: 700;
}
.user {
  display: flex;
  align-items: center;
  gap: 12px;
}
.user span {
  color: #f5ead9;
  font-size: 13px;
}
button {
  background: transparent;
  color: #f5ead9;
  border: 1px solid #f5ead9;
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
}
button:hover {
  background: rgba(255,255,255,0.1);
}
</style>