<template>
  <div id="app">
    <header v-if="isAuthenticated">
      <div class="container">
        <h1>FX Rate Manager</h1>
        <nav>
          <router-link to="/exchange-rates">Exchange Rates</router-link>
          <router-link to="/convert">Convert Currency</router-link>
          <div style="margin-left: auto; display: flex; align-items: center; gap: 1rem;">
            <span v-if="user">Welcome, {{ user.username }}</span>
            <button class="btn btn-secondary btn-small" @click="handleLogout">Logout</button>
          </div>
        </nav>
      </div>
    </header>
    <main class="container">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuth } from './composables/useAuth'

const { user, isAuthenticated, logout } = useAuth()

const handleLogout = () => {
  logout()
}
</script>

