<template>
  <div class="login-container">
    <div class="card" style="max-width: 400px; margin: 2rem auto;">
      <h2>Login</h2>
      
      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            placeholder="Enter your username"
            autocomplete="username"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            placeholder="Enter your password"
            autocomplete="current-password"
          />
        </div>
        
        <button type="submit" class="btn btn-primary" :disabled="loading" style="width: 100%;">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <div style="margin-top: 1rem; text-align: center;">
        <p>Don't have an account? <router-link to="/register">Register here</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useAuth } from '../composables/useAuth'

const { login, loading, error } = useAuth()

const form = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  try {
    await login(form)
  } catch (err) {
    // Error is handled by useAuth composable
  }
}
</script>

<style scoped>
.login-container {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>


