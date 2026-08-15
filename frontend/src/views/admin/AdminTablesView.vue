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