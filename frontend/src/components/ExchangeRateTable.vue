<template>
  <div>
    <table v-if="rates.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>From Currency</th>
          <th>To Currency</th>
          <th>Period</th>
          <th>Rate</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="rate in rates" :key="rate.id">
          <td>{{ rate.id }}</td>
          <td>{{ rate.from_currency }}</td>
          <td>{{ rate.to_currency }}</td>
          <td>{{ rate.period }}</td>
          <td>{{ formatRate(rate.rate) }}</td>
          <td>
            <div class="actions">
              <button class="btn btn-secondary btn-small" @click="handleEdit(rate)">
                Edit
              </button>
              <button class="btn btn-danger btn-small" @click="handleDelete(rate.id)">
                Delete
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else class="loading">No exchange rates found</div>
  </div>
</template>

<script setup lang="ts">
import type { ExchangeRate } from '../api/exchangeRatesApi'

interface Props {
  rates: ExchangeRate[]
}

defineProps<Props>()

const emit = defineEmits<{
  edit: [rate: ExchangeRate]
  delete: [id: number]
}>()

const formatRate = (rate: number): string => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 8
  }).format(rate)
}

const handleEdit = (rate: ExchangeRate) => {
  emit('edit', rate)
}

const handleDelete = (id: number) => {
  emit('delete', id)
}
</script>


