<template>
  <div class="page">
    <NavBar />
    <div class="container">
      <h1>Moje rezervacije</h1>

      <div v-if="reservations.length === 0" class="empty">
        Nemaš još nijednu rezervaciju.
        <router-link to="/dashboard">Rezerviraj stol</router-link>
      </div>

      <table v-else>
        <thead>
          <tr>
            <th>Stol</th>
            <th>Datum / vrijeme</th>
            <th>Broj osoba</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in reservations" :key="r.id">
            <td>{{ r.table }}</td>
            <td>{{ r.date }}</td>
            <td>{{ r.guests }}</td>
            <td>
              <span class="badge" :class="r.status">
                {{ statusLabel(r.status) }}
              </span>
            </td>
            <td>
              <button
                v-if="r.status !== 'cancelled'"
                class="cancel-btn"
                @click="cancel(r)"
              >
                Otkaži
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
import NavBar from '../components/NavBar.vue'

const reservations = ref([
  { id: 1, table: 'Stol 1', date: '06.04.2026. 14:00', guests: 2, status: 'confirmed' },
  { id: 2, table: 'Stol 3', date: '10.04.2026. 19:00', guests: 4, status: 'confirmed' },
])

function statusLabel(s) {
  return { confirmed: 'Potvrđeno', pending: 'Na čekanju', cancelled: 'Otkazano' }[s] || s
}

function cancel(r) {
  r.status = 'cancelled'
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
.badge.confirmed { background: #e3f0e2; color: #4f7a52; }
.badge.cancelled { background: #f6e2dd; color: #b3432f; }
.badge.pending { background: #fbf0d9; color: #9a7424; }
.cancel-btn { background: #b3432f; color: white; border: none; padding: 6px 14px; border-radius: 8px; cursor: pointer; font-size: 13px; }
.cancel-btn:hover { background: #8c3324; }
.empty { text-align: center; padding: 40px; color: #888; }
.empty a { color: #8c4a2f; margin-left: 6px; }
</style>