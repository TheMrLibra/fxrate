import { ref, computed } from 'vue'
import { authApi, type User, type LoginRequest, type RegisterRequest } from '../api/authApi'
import router from '../router'

const token = ref<string | null>(localStorage.getItem('token'))
const user = ref<User | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

export function useAuth() {
  const isAuthenticated = computed(() => !!token.value)

  const setToken = (newToken: string | null) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  const setUser = (newUser: User | null) => {
    user.value = newUser
  }

  const login = async (credentials: LoginRequest) => {
    loading.value = true
    error.value = null
    try {
      const response = await authApi.login(credentials)
      setToken(response.access_token)
      await fetchUser()
      router.push('/exchange-rates')
      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const register = async (data: RegisterRequest) => {
    loading.value = true
    error.value = null
    try {
      const newUser = await authApi.register(data)
      // Auto-login after registration
      await login({ username: data.username, password: data.password })
      return newUser
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Registration failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    router.push('/login')
  }

  const fetchUser = async () => {
    if (!token.value) return
    
    try {
      const currentUser = await authApi.getCurrentUser()
      setUser(currentUser)
    } catch (err) {
      // Token might be invalid, clear it
      setToken(null)
      setUser(null)
    }
  }

  // Initialize user if token exists
  if (token.value) {
    fetchUser()
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUser
  }
}


