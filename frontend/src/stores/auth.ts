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

  const login = async (credentials: LoginCredentials): Promise<boolean> => {
    try {
      // Convert credentials to FormData as required by OAuth2PasswordRequestForm
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

      // Store the token and email
      setToken(data.access_token)
      userEmail.value = credentials.username // Store the email used to login

      await router.push('/')

      return true
    } catch (error) {
      console.error('Login error:', error)
      setToken(null)
      userEmail.value = null
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
      // Even if you don't have a logout endpoint, we should still clear local state
      setToken(null)
      userEmail.value = null
      await router.push('/login')
      return true
    } catch (error) {
      console.error('Logout failed:', error)
      return false
    }
  }

  return {
    token,
    userEmail,
    isAuthenticated,
    login,
    register,
    logout
  }
})
