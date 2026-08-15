<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const user = computed(() => JSON.parse(localStorage.getItem('smartable_user') || '{}'))
const isAdmin = computed(() => user.value.role === 'admin')
const userName = computed(() => user.value.email || '')

function logout() {
  localStorage.removeItem('smartable_token')
  localStorage.removeItem('smartable_user')
  router.push('/login')
}
</script>