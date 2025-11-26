import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://fx-api.adamlibra.cz'

export interface ExchangeRate {
  id: number
  from_currency: string
  to_currency: string
  period: string
  rate: number
}

export interface ExchangeRateCreate {
  from_currency: string
  to_currency: string
  period: string
  rate: number
}

export interface ExchangeRateUpdate {
  from_currency?: string
  to_currency?: string
  period?: string
  rate?: number
}

export interface ExchangeRateFilter {
  from_currency?: string
  to_currency?: string
  period?: string
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const exchangeRatesApi = {
  async list(filters?: ExchangeRateFilter): Promise<ExchangeRate[]> {
    const params = new URLSearchParams()
    if (filters?.from_currency) params.append('from_currency', filters.from_currency)
    if (filters?.to_currency) params.append('to_currency', filters.to_currency)
    if (filters?.period) params.append('period', filters.period)
    
    const response = await api.get<ExchangeRate[]>('/exchange-rates', { params })
    return response.data
  },

  async getById(id: number): Promise<ExchangeRate> {
    const response = await api.get<ExchangeRate>(`/exchange-rates/${id}`)
    return response.data
  },

  async create(data: ExchangeRateCreate): Promise<ExchangeRate> {
    const response = await api.post<ExchangeRate>('/exchange-rates', data)
    return response.data
  },

  async update(id: number, data: ExchangeRateUpdate): Promise<ExchangeRate> {
    const response = await api.put<ExchangeRate>(`/exchange-rates/${id}`, data)
    return response.data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/exchange-rates/${id}`)
  }
}

