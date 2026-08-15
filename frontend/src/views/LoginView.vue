<template>
  <div class="login-container">
    <div class="login-box">
      <h1>🍽 SmarTable</h1>
      <h2>Prijava</h2>

      <form @submit.prevent="onSubmit">
        <label>Email</label>
        <input v-model="email" type="email" placeholder="ime@email.com" required />

        <label>Lozinka</label>
        <input v-model="password" type="password" placeholder="••••••••" required />

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Prijava...' : 'Prijavi se' }}
        </button>
      </form>

      <p>Nemaš račun? <router-link to="/register">Registriraj se</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api.js'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

async function onSubmit() {
  error.value = ''
  loading.value = true
  try {
    const { data } = await api.post('/auth/login', {
      email: email.value,
      password: password.value
    })
    localStorage.setItem('smartable_token', data.access_token)
    localStorage.setItem('smartable_user', JSON.stringify(data.user))
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Pogrešan email ili lozinka.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #faf7f2;
}
.login-box {
  background: white;
  padding: 40px;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}
h1 { color: #8c4a2f; margin-bottom: 4px; }
h2 { color: #444; margin-bottom: 24px; }
label { display: block; font-size: 13px; font-weight: 600; color: #666; margin-bottom: 4px; }
input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 16px; font-size: 14px; box-sizing: border-box; }
button { width: 100%; padding: 12px; background: #8c4a2f; color: white; border: none; border-radius: 8px; font-size: 15px; cursor: pointer; }
button:hover { background: #6e3a24; }
.error { color: red; font-size: 13px; }
p { margin-top: 16px; font-size: 13px; text-align: center; }
a { color: #8c4a2f; }
</style>