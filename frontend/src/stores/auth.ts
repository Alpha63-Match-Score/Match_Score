// stores/auth.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { API_URL } from '@/config'

interface LoginCredentials {
  username: string // email
  password: string
}

interface LoginResponse {
  access_token: string
  token_type: string
  role: string
}

interface RegisterCredentials {
  email: string
  password: string
}

interface RegisterResponse {
  email: string
  role: string
}

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const token = ref<string | null>(localStorage.getItem('token') || null)
  const userEmail = ref<string | null>(null)
  const userRole = ref<string | null>(null) // Add role to the state
  const isAuthenticated = ref(!!token.value)

  const setToken = (newToken: string | null) => {
    token.value = newToken
    isAuthenticated.value = !!newToken

    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  const setUserRole = (role: string | null) => {
    userRole.value = role
    if (role) {
      localStorage.setItem('userRole', role)
    } else {
      localStorage.removeItem('userRole')
    }
  }

  const login = async (credentials: LoginCredentials): Promise<boolean> => {
    try {
      const formData = new FormData()
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)

      const response = await fetch(`${API_URL}/users/login`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('Login failed')
      }

      const data: LoginResponse = await response.json()

      // Store the token, email, and role
      setToken(data.access_token)
      userEmail.value = credentials.username
      setUserRole(data.role)

      await router.push('/')

      return true
    } catch (error) {
      console.error('Login error:', error)
      setToken(null)
      userEmail.value = null
      setUserRole(null)
      return false
    }
  }

  const register = async (credentials: RegisterCredentials): Promise<boolean> => {
    try {
      const response = await fetch(`${API_URL}/users/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: credentials.email,
          password: credentials.password
        })
      })

      if (!response.ok) {
        throw new Error('Registration failed')
      }

      const data: RegisterResponse = await response.json()

      setUserRole(data.role)

      const loginSuccess = await login({
        username: credentials.email,
        password: credentials.password
      })

      if (!loginSuccess) {
        throw new Error('Auto-login after registration failed')
      }

      return true
    } catch (error) {
      console.error('Registration error:', error)
      return false
    }
  }

  const logout = async (): Promise<boolean> => {
    try {
      setToken(null)
      userEmail.value = null
      setUserRole(null) // Clear role on logout
      await router.push('/login')
      return true
    } catch (error) {
      console.error('Logout failed:', error)
      return false
    }
  }

  const fetchUserRole = async (): Promise<void> => {
    try {
      if (!token.value) {
        throw new Error('User is not authenticated')
      }

      const response = await fetch(`${API_URL}/users/role`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      })

      if (!response.ok) {
        throw new Error('Failed to fetch user role')
      }

      const data = await response.json()
      setUserRole(data.role) // Assume the API returns a `role` field
    } catch (error) {
      console.error('Error fetching user role:', error)
      setUserRole(null)
    }
  }

  return {
    token,
    userEmail,
    userRole, // Expose userRole to components
    isAuthenticated,
    login,
    register,
    logout,
    fetchUserRole // Expose method to fetch roles
  }
})
