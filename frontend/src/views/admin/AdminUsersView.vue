<template>
  <div class="page">
    <NavBar />
    <div class="container">
      <h1>Upravljanje korisnicima</h1>

      <table>
        <thead>
          <tr>
            <th>Ime</th>
            <th>Email</th>
            <th>Uloga</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.name }}</td>
            <td>{{ u.email }}</td>
            <td>
              <select :value="u.role" @change="changeRole(u, $event.target.value)">
                <option value="user">Korisnik</option>
                <option value="admin">Administrator</option>
              </select>
            </td>
            <td>
              <span class="badge" :class="u.active ? 'active' : 'inactive'">
                {{ u.active ? 'Aktivan' : 'Deaktiviran' }}
              </span>
            </td>
            <td>
              <button @click="toggleActive(u)" :class="u.active ? 'deactivate-btn' : 'activate-btn'">
                {{ u.active ? 'Deaktiviraj' : 'Aktiviraj' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NavBar from '../../components/NavBar.vue'

const users = ref([
  { id: 1, name: 'Administrator', email: 'admin@smarttable.com', role: 'admin', active: true },
  { id: 2, name: 'Ana Anić', email: 'ana@email.com', role: 'user', active: true },
  { id: 3, name: 'Ivan Ivić', email: 'ivan@email.com', role: 'user', active: true },
  { id: 4, name: 'Maja Majić', email: 'maja@email.com', role: 'user', active: false },
])

function changeRole(u, role) {
  u.role = role
}

function toggleActive(u) {
  u.active = !u.active
}
</script>

<style scoped>
.page { min-height: 100vh; background: #faf7f2; }
.container { max-width: 900px; margin: 0 auto; padding: 24px; }
h1 { color: #8c4a2f; }
table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #eee; font-size: 14px; }
th { color: #888; font-size: 12px; text-transform: uppercase; }
.badge { padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; }
.badge.active { background: #e3f0e2; color: #4f7a52; }
.badge.inactive { background: #f6e2dd; color: #b3432f; }
select { padding: 6px 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px; cursor: pointer; }
button { padding: 6px 14px; border: none; border-radius: 8px; cursor: pointer; font-size: 13px; }
.deactivate-btn { background: #b3432f; color: white; }
.activate-btn { background: #4f7a52; color: white; }
</style>