<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import api from '../api.js'

const date = ref('')
const guests = ref(2)
const tables = ref([])
const searched = ref(false)
const successMsg = ref('')
const error = ref('')
const router = useRouter()

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