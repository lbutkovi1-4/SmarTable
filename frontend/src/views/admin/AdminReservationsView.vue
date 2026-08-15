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