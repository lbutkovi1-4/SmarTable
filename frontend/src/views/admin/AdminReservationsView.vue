<template>
  <div class="page">
    <NavBar />
    <div class="container">
      <h1>Sve rezervacije</h1>

      <div v-if="loading" class="empty">Učitavanje...</div>
      <div v-else-if="reservations.length === 0" class="empty">Nema rezervacija.</div>

      <table v-else>
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
            <td>{{ r.user.full_name }}<br/><span style="color:#888;font-size:12px;">{{ r.user.email }}</span></td>
            <td>{{ r.table.name }}</td>
            <td>{{ formatDate(r.reservation_date) }}</td>
            <td>{{ r.guests_count }}</td>
            <td><span class="badge" :class="r.status">{{ statusLabel(r.status) }}</span></td>
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
import { ref, onMounted } from 'vue'
import NavBar from '../../components/NavBar.vue'
import api from '../../api.js'

const reservations = ref([])
const loading = ref(true)

function formatDate(iso) {
  return new Date(iso).toLocaleString('hr-HR', { dateStyle: 'medium', timeStyle: 'short' })
}

function statusLabel(s) {
  return { confirmed: 'Potvrđeno', pending: 'Na čekanju', cancelled: 'Otkazano' }[s] || s
}

async function load() {
  loading.value = true
  const { data } = await api.get('/reservations/')
  reservations.value = data
  loading.value = false
}

async function changeStatus(r, newStatus) {
  await api.patch(`/reservations/${r.id}/status`, { status: newStatus })
  await load()
}

onMounted(load)
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
select { padding: 6px 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px; }
.empty { text-align: center; padding: 40px; color: #888; }
</style>