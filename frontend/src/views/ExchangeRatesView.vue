<template>
  <div>
    <div class="card">
      <h2>Exchange Rates Management</h2>
      
      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>
      
      <div v-if="success" class="alert alert-success">
        {{ success }}
      </div>

      <div class="filters">
        <input
          v-model="filters.from_currency"
          type="text"
          placeholder="From Currency"
          @input="loadRates"
        />
        <input
          v-model="filters.to_currency"
          type="text"
          placeholder="To Currency"
          @input="loadRates"
        />
        <input
          v-model="filters.period"
          type="text"
          placeholder="Period (e.g., 2025-01)"
          @input="loadRates"
        />
        <button class="btn btn-secondary" @click="clearFilters">Clear Filters</button>
      </div>

      <button class="btn btn-primary" @click="showCreateForm">
        {{ editingId ? 'Cancel Edit' : 'Add New Rate' }}
      </button>

      <ExchangeRateForm
        v-if="showForm"
        :rate="editingRate"
        @save="handleSave"
        @cancel="handleCancel"
      />

      <div v-if="loading" class="loading">Loading...</div>
      
      <ExchangeRateTable
        v-else
        :rates="rates"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { exchangeRatesApi, type ExchangeRate, type ExchangeRateCreate, type ExchangeRateUpdate, type ExchangeRateFilter } from '../api/exchangeRatesApi'
import ExchangeRateForm from '../components/ExchangeRateForm.vue'
import ExchangeRateTable from '../components/ExchangeRateTable.vue'

const rates = ref<ExchangeRate[]>([])
const loading = ref(false)
const error = ref('')
const success = ref('')
const showForm = ref(false)
const editingId = ref<number | null>(null)
const editingRate = ref<ExchangeRate | null>(null)

const filters = ref<ExchangeRateFilter>({
  from_currency: '',
  to_currency: '',
  period: ''
})

const loadRates = async () => {
  loading.value = true
  error.value = ''
  try {
    const filterParams: ExchangeRateFilter = {}
    if (filters.value.from_currency) filterParams.from_currency = filters.value.from_currency
    if (filters.value.to_currency) filterParams.to_currency = filters.value.to_currency
    if (filters.value.period) filterParams.period = filters.value.period
    
    rates.value = await exchangeRatesApi.list(filterParams)
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load exchange rates'
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filters.value = { from_currency: '', to_currency: '', period: '' }
  loadRates()
}

const showCreateForm = () => {
  if (showForm.value && !editingId.value) {
    showForm.value = false
  } else {
    editingId.value = null
    editingRate.value = null
    showForm.value = true
  }
}

const handleEdit = (rate: ExchangeRate) => {
  editingId.value = rate.id
  editingRate.value = { ...rate }
  showForm.value = true
}

const handleCancel = () => {
  showForm.value = false
  editingId.value = null
  editingRate.value = null
}

const handleSave = async (data: ExchangeRateCreate | ExchangeRateUpdate) => {
  error.value = ''
  success.value = ''
  try {
    if (editingId.value) {
      await exchangeRatesApi.update(editingId.value, data as ExchangeRateUpdate)
      success.value = 'Exchange rate updated successfully'
    } else {
      await exchangeRatesApi.create(data as ExchangeRateCreate)
      success.value = 'Exchange rate created successfully'
    }
    showForm.value = false
    editingId.value = null
    editingRate.value = null
    await loadRates()
    setTimeout(() => {
      success.value = ''
    }, 3000)
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to save exchange rate'
  }
}

const handleDelete = async (id: number) => {
  if (!confirm('Are you sure you want to delete this exchange rate?')) {
    return
  }
  
  error.value = ''
  success.value = ''
  try {
    await exchangeRatesApi.delete(id)
    success.value = 'Exchange rate deleted successfully'
    await loadRates()
    setTimeout(() => {
      success.value = ''
    }, 3000)
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to delete exchange rate'
  }
}

onMounted(() => {
  loadRates()
})
</script>


