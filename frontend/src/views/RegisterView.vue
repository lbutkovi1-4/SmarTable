<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api.js'

const fullName = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)
const router = useRouter()

async function onSubmit() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await api.post('/auth/register', {
      full_name: fullName.value,
      email: email.value,
      password: password.value
    })
    success.value = 'Račun je kreiran! Preusmjeravam na prijavu...'
    setTimeout(() => router.push('/login'), 1500)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Greška pri registraciji.'
  } finally {
    loading.value = false
  }
}
</script>