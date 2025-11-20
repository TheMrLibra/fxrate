<template>
  <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #ddd;">
    <h3>{{ rate ? 'Edit Exchange Rate' : 'Create New Exchange Rate' }}</h3>
    
    <form @submit.prevent="handleSubmit">
      <div class="form-row">
        <div class="form-group">
          <label for="from_currency">From Currency</label>
          <input
            id="from_currency"
            v-model="formData.from_currency"
            type="text"
            maxlength="3"
            required
            placeholder="e.g., CZK"
            style="text-transform: uppercase"
          />
        </div>
        
        <div class="form-group">
          <label for="to_currency">To Currency</label>
          <input
            id="to_currency"
            v-model="formData.to_currency"
            type="text"
            maxlength="3"
            required
            placeholder="e.g., EUR"
            style="text-transform: uppercase"
          />
        </div>
        
        <div class="form-group">
          <label for="period">Period</label>
          <input
            id="period"
            v-model="formData.period"
            type="text"
            required
            placeholder="e.g., 2025-01"
          />
        </div>
        
        <div class="form-group">
          <label for="rate">Rate</label>
          <input
            id="rate"
            v-model.number="formData.rate"
            type="number"
            step="0.00000001"
            min="0.00000001"
            required
            placeholder="e.g., 0.0405"
          />
        </div>
      </div>
      
      <div style="display: flex; gap: 1rem; margin-top: 1rem;">
        <button type="submit" class="btn btn-primary">
          {{ rate ? 'Update' : 'Create' }}
        </button>
        <button type="button" class="btn btn-secondary" @click="handleCancel">
          Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import type { ExchangeRate, ExchangeRateCreate, ExchangeRateUpdate } from '../api/exchangeRatesApi'

interface Props {
  rate?: ExchangeRate | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  save: [data: ExchangeRateCreate | ExchangeRateUpdate]
  cancel: []
}>()

const formData = reactive({
  from_currency: '',
  to_currency: '',
  period: '',
  rate: 0
})

watch(() => props.rate, (newRate: ExchangeRate | null | undefined) => {
  if (newRate) {
    formData.from_currency = newRate.from_currency
    formData.to_currency = newRate.to_currency
    formData.period = newRate.period
    formData.rate = newRate.rate
  } else {
    formData.from_currency = ''
    formData.to_currency = ''
    formData.period = ''
    formData.rate = 0
  }
}, { immediate: true })

const handleSubmit = () => {
  if (props.rate) {
    // Update: only send changed fields
    const updateData: ExchangeRateUpdate = {}
    if (formData.from_currency !== props.rate.from_currency) {
      updateData.from_currency = formData.from_currency.toUpperCase()
    }
    if (formData.to_currency !== props.rate.to_currency) {
      updateData.to_currency = formData.to_currency.toUpperCase()
    }
    if (formData.period !== props.rate.period) {
      updateData.period = formData.period
    }
    if (formData.rate !== props.rate.rate) {
      updateData.rate = formData.rate
    }
    emit('save', updateData)
  } else {
    // Create: send all fields
    const createData: ExchangeRateCreate = {
      from_currency: formData.from_currency.toUpperCase(),
      to_currency: formData.to_currency.toUpperCase(),
      period: formData.period,
      rate: formData.rate
    }
    emit('save', createData)
  }
}

const handleCancel = () => {
  emit('cancel')
}
</script>

