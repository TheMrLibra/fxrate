import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export interface ConversionResult {
  from_currency: string
  to_currency: string
  period: string
  original_amount: number
  rate: number
  converted_amount: number
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

export const conversionApi = {
  async convert(
    amount: number,
    from_currency: string,
    to_currency: string,
    period: string
  ): Promise<ConversionResult> {
    const params = new URLSearchParams({
      amount: amount.toString(),
      from_currency,
      to_currency,
      period
    })
    
    const response = await api.get<ConversionResult>('/conversion', { params })
    return response.data
  }
}

