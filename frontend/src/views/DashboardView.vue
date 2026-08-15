<template>
  <div class="dashboard">
    <NavBar />
    <div class="container">
      <h1>Pronađi stol</h1>

      <div class="search-box">
        <div class="search-grid">
          <div>
            <label>Datum i vrijeme</label>
            <input v-model="date" type="datetime-local" required />
          </div>
          <div>
            <label>Broj osoba</label>
            <input v-model.number="guests" type="number" min="1" max="20" />
          </div>
          <div>
            <button @click="search">Pretraži</button>
          </div>
        </div>
        <p v-if="error" class="error">{{ error }}</p>
      </div>

      <div v-if="searched">
        <h2>Dostupni stolovi</h2>
        <div v-if="tables.length === 0" class="empty">
          Nema slobodnih stolova za odabrani termin.
        </div>
        <div class="tables-grid">
          <div class="table-card" v-for="t in tables" :key="t.id">
            <h3>{{ t.name }}</h3>
            <p>Kapacitet: {{ t.capacity }} osoba</p>
            <p class="desc">{{ t.description }}</p>
            <button @click="reserve(t)">Rezerviraj</button>
          </div>
        </div>
      </div>

      <p v-if="successMsg" class="success">{{ successMsg }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NavBar from '../components/NavBar.vue'
import api from '../api.js'

const date = ref('')
const guests = ref(2)
const tables = ref([])
const searched = ref(false)
const successMsg = ref('')
const error = ref('')

async function search() {
  error.value = ''
  successMsg.value = ''
  if (!date.value) {
    error.value = 'Odaberi datum i vrijeme.'
    return
  }
  try {
    const { data } = await api.get('/reservations/availability', {
      params: { date: date.value, guests_count: guests.value, duration_minutes: 90 }
    })
    tables.value = data
    searched.value = true
  } catch (e) {
    error.value = e.response?.data?.detail || 'Greška pri pretrazi.'
  }
}

async function reserve(table) {
  error.value = ''
  successMsg.value = ''
  try {
    await api.post('/reservations/', {
      table_id: table.id,
      reservation_date: date.value,
      duration_minutes: 90,
      guests_count: guests.value
    })
    successMsg.value = `Rezervacija za "${table.name}" uspješno kreirana!`
    await search()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Greška pri rezervaciji.'
  }
}
</script>

<style scoped>
.dashboard { min-height: 100vh; background: #faf7f2; }
.container { max-width: 900px; margin: 0 auto; padding: 24px; }
h1 { color: #8c4a2f; }
.search-box { background: white; padding: 24px; border-radius: 12px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.search-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; align-items: end; }
label { display: block; font-size: 13px; font-weight: 600; color: #666; margin-bottom: 4px; }
input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; box-sizing: border-box; }
button { width: 100%; padding: 10px; background: #8c4a2f; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; }
button:hover { background: #6e3a24; }
.tables-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
.table-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.table-card h3 { color: #8c4a2f; margin: 0 0 8px; }
.table-card p { margin: 0 0 8px; font-size: 14px; color: #444; }
.desc { color: #888 !important; font-size: 13px !important; }
.table-card button { margin-top: 12px; }
.empty { color: #888; padding: 20px; text-align: center; }
.error { color: red; font-size: 13px; margin-top: 8px; }
.success { color: green; font-weight: 600; margin-top: 16px; }
</style>