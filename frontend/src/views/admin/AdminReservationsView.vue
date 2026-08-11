<template>
  <div class="page">
    <NavBar />
    <div class="container">
      <h1>Sve rezervacije</h1>

      <table>
        <thead>
          <tr>
            <th>Gost</th>
            <th>Stol</th>
            <th>Datum / vrijeme</th>
            <th>Osoba</th>
            <th>Status</th>
            <th>Promijeni status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in reservations" :key="r.id">
            <td>{{ r.user }}</td>
            <td>{{ r.table }}</td>
            <td>{{ r.date }}</td>
            <td>{{ r.guests }}</td>
            <td>
              <span class="badge" :class="r.status">
                {{ statusLabel(r.status) }}
              </span>
            </td>
            <td>
              <select :value="r.status" @change="changeStatus(r, $event.target.value)">
                <option value="pending">Na čekanju</option>
                <option value="confirmed">Potvrđeno</option>
                <option value="cancelled">Otkazano</option>
              </select>
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

const reservations = ref([
  { id: 1, user: 'ana@email.com', table: 'Stol 1', date: '06.04.2026. 14:00', guests: 2, status: 'confirmed' },
  { id: 2, user: 'ivan@email.com', table: 'Stol 3', date: '10.04.2026. 19:00', guests: 4, status: 'pending' },
  { id: 3, user: 'maja@email.com', table: 'Stol 2', date: '12.04.2026. 20:00', guests: 3, status: 'cancelled' },
])

function statusLabel(s) {
  return { confirmed: 'Potvrđeno', pending: 'Na čekanju', cancelled: 'Otkazano' }[s] || s
}

function changeStatus(r, newStatus) {
  r.status = newStatus
}
</script>

<style scoped>
.page { min-height: 100vh; background: #faf7f2; }
.container { max-width: 1000px; margin: 0 auto; padding: 24px; }
h1 { color: #8c4a2f; }
table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #eee; font-size: 14px; }
th { color: #888; font-size: 12px; text-transform: uppercase; }
.badge { padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; }
.badge.confirmed { background: #e3f0e2; color: #4f7a52; }
.badge.cancelled { background: #f6e2dd; color: #b3432f; }
.badge.pending { background: #fbf0d9; color: #9a7424; }
select { padding: 6px 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px; cursor: pointer; }
</style>