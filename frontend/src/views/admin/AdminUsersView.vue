<script setup>
import { ref, onMounted } from 'vue'
import NavBar from '../../components/NavBar.vue'
import api from '../../api.js'

const users = ref([])
const loading = ref(true)

async function load() {
  loading.value = true
  const { data } = await api.get('/users/')
  users.value = data
  loading.value = false
}

async function changeRole(u, role) {
  await api.patch(`/users/${u.id}/role`, { role })
  await load()
}

async function toggleActive(u) {
  await api.patch(`/users/${u.id}/toggle-active`)
  await load()
}

onMounted(load)
</script>