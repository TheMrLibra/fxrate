<template>
  <div>
    <div class="card">
      <h2>Currency Conversion</h2>
      
      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>

      <form @submit.prevent="handleConvert">
        <div class="form-row">
          <div class="form-group">
            <label for="amount">Amount</label>
            <input
              id="amount"
              v-model.number="form.amount"
              type="number"
              step="0.01"
              min="0.01"
              required
              placeholder="Enter amount"
            />
          </div>
          
          <div class="form-group">
            <label for="from_currency">From Currency</label>
            <input
              id="from_currency"
              v-model="form.from_currency"
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
              v-model="form.to_currency"
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
              v-model="form.period"
              type="text"
              required
              placeholder="e.g., 2025-01"
            />
          </div>
        </div>
        
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Converting...' : 'Convert' }}
        </button>
      </form>

      <div v-if="result" class="result-card">
        <h3>Conversion Result</h3>
        <div class="result-item">
          <span>From Currency:</span>
          <span>{{ result.from_currency }}</span>
        </div>
        <div class="result-item">
          <span>To Currency:</span>
          <span>{{ result.to_currency }}</span>
        </div>
        <div class="result-item">
          <span>Period:</span>
          <span>{{ result.period }}</span>
        </div>
        <div class="result-item">
          <span>Original Amount:</span>
          <span>{{ formatNumber(result.original_amount) }} {{ result.from_currency }}</span>
        </div>
        <div class="result-item">
          <span>Exchange Rate:</span>
          <span>{{ formatNumber(result.rate) }}</span>
        </div>
        <div class="result-item">
          <span>Converted Amount:</span>
          <span>{{ formatNumber(result.converted_amount) }} {{ result.to_currency }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { conversionApi, type ConversionResult } from '../api/conversionApi'

const form = reactive({
  amount: 0 as number,
  from_currency: '',
  to_currency: '',
  period: ''
})

const result = ref<ConversionResult | null>(null)
const loading = ref(false)
const error = ref('')

const formatNumber = (num: number): string => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 8
  }).format(num)
}

const handleConvert = async () => {
  if (form.amount <= 0) {
    error.value = 'Amount must be greater than 0'
    return
  }
  
  loading.value = true
  error.value = ''
  result.value = null
  
  try {
    result.value = await conversionApi.convert(
      form.amount,
      form.from_currency.toUpperCase(),
      form.to_currency.toUpperCase(),
      form.period
    )
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to convert currency'
  } finally {
    loading.value = false
  }
}
</script>

