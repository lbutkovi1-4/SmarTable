<template>
  <div class="page">
    <NavBar />
    <div class="container">
      <h1>Upravljanje stolovima</h1>

      <div class="form-box">
        <h3>{{ editingId ? 'Uredi stol' : 'Dodaj novi stol' }}</h3>
        <div class="form-grid">
          <div>
            <label>Naziv</label>
            <input v-model="form.name" placeholder="Stol 1" />
          </div>
          <div>
            <label>Kapacitet</label>
            <input v-model.number="form.capacity" type="number" min="1" />
          </div>
          <div>
            <label>Opis</label>
            <input v-model="form.description" placeholder="terasa, kraj prozora..." />
          </div>
          <div>
            <label>&nbsp;</label>
            <button @click="save">{{ editingId ? 'Spremi' : 'Dodaj' }}</button>
          </div>
        </div>
        <button v-if="editingId" class="cancel-btn" @click="resetForm">Odustani</button>
        <p v-if="error" class="error">{{ error }}</p>
      </div>

      <div v-if="loading" class="empty">Učitavanje...</div>
      <div class="tables-grid" v-else>
        <div class="table-card" v-for="t in tables" :key="t.id">
          <h3>{{ t.name }}</h3>
          <p>Kapacitet: {{ t.capacity }} osoba</p>
          <p class="desc">{{ t.description }}</p>
          <div class="actions">
            <button class="edit-btn" @click="edit(t)">Uredi</button>
            <button class="delete-btn" @click="remove(t)">Obriši</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavBar from '../../components/NavBar.vue'
import api from '../../api.js'

const tables = ref([])
const loading = ref(true)
const error = ref('')
const editingId = ref(null)
const form = ref({ name: '', capacity: 2, description: '' })

async function load() {
  loading.value = true
  const { data } = await api.get('/tables/')
  tables.value = data
  loading.value = false
}

function resetForm() {
  editingId.value = null
  form.value = { name: '', capacity: 2, description: '' }
}

function edit(t) {
  editingId.value = t.id
  form.value = { name: t.name, capacity: t.capacity, description: t.description || '' }
}

async function save() {
  error.value = ''
  try {
    if (editingId.value) {
      await api.put(`/tables/${editingId.value}`, form.value)
    } else {
      await api.post('/tables/', form.value)
    }
    resetForm()
    await load()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Greška pri spremanju.'
  }
}

async function remove(t) {
  if (!confirm(`Obrisati stol "${t.name}"?`)) return
  await api.delete(`/tables/${t.id}`)
  await load()
}

onMounted(load)
</script>

<style scoped>
.page { min-height: 100vh; background: #faf7f2; }
.container { max-width: 900px; margin: 0 auto; padding: 24px; }
h1 { color: #8c4a2f; }
.form-box { background: white; padding: 24px; border-radius: 12px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.form-grid { display: grid; grid-template-columns: 1fr 1fr 2fr 1fr; gap: 16px; align-items: end; }
label { display: block; font-size: 13px; font-weight: 600; color: #666; margin-bottom: 4px; }
input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; box-sizing: border-box; }
button { width: 100%; padding: 10px; background: #8c4a2f; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; }
button:hover { background: #6e3a24; }
.cancel-btn { margin-top: 12px; width: auto; padding: 8px 16px; background: transparent; color: #8c4a2f; border: 1px solid #8c4a2f; }
.tables-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
.table-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.table-card h3 { color: #8c4a2f; margin: 0 0 8px; }
.table-card p { margin: 0 0 8px; font-size: 14px; color: #444; }
.desc { color: #888 !important; font-size: 13px !important; }
.actions { display: flex; gap: 8px; margin-top: 12px; }
.edit-btn { background: transparent; color: #8c4a2f; border: 1px solid #8c4a2f; }
.delete-btn { background: #b3432f; }
.error { color: red; font-size: 13px; margin-top: 8px; }
.empty { text-align: center; padding: 40px; color: #888; }
</style>