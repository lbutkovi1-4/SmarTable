<template>
  <div class="register-container">
    <div class="register-box">
      <h1>🍽 SmartTable</h1>
      <h2>Registracija</h2>

      <form @submit.prevent="onSubmit">
        <label>Ime i prezime</label>
        <input v-model="fullName" type="text" placeholder="Ana Anić" required />

        <label>Email</label>
        <input v-model="email" type="email" placeholder="ime@email.com" required />

        <label>Lozinka</label>
        <input v-model="password" type="password" placeholder="min. 6 znakova" required minlength="6" />

        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="success" class="success">{{ success }}</p>

        <button type="submit">Registriraj se</button>
      </form>

      <p>Već imaš račun? <router-link to="/login">Prijavi se</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const fullName = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const router = useRouter()

function onSubmit() {
  if (!fullName.value || !email.value || password.value.length < 6) {
    error.value = 'Molimo ispunite sva polja ispravno.'
    return
  }
  success.value = 'Račun je kreiran! Preusmjeravam na prijavu...'
  setTimeout(() => router.push('/login'), 1500)
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #faf7f2;
}
.register-box {
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
.success { color: green; font-size: 13px; }
p { margin-top: 16px; font-size: 13px; text-align: center; }
a { color: #8c4a2f; }
</style>