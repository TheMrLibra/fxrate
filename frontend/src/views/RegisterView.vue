<template>
  <div class="register-container">
    <div class="card" style="max-width: 400px; margin: 2rem auto;">
      <h2>Register</h2>
      
      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            minlength="3"
            placeholder="Choose a username"
            autocomplete="username"
          />
        </div>
        
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            placeholder="Enter your email"
            autocomplete="email"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            minlength="6"
            placeholder="Choose a password"
            autocomplete="new-password"
          />
        </div>
        
        <button type="submit" class="btn btn-primary" :disabled="loading" style="width: 100%;">
          {{ loading ? 'Registering...' : 'Register' }}
        </button>
      </form>

      <div style="margin-top: 1rem; text-align: center;">
        <p>Already have an account? <router-link to="/login">Login here</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useAuth } from '../composables/useAuth'

const { register, loading, error } = useAuth()

const form = reactive({
  username: '',
  email: '',
  password: ''
})

const handleRegister = async () => {
  try {
    await register(form)
  } catch (err) {
    // Error is handled by useAuth composable
  }
}
</script>

<style scoped>
.register-container {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

