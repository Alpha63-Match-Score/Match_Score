// stores/auth.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { API_URL } from '@/config'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)
  const isAuthenticated = ref(!!token.value)

  const logout = async () => {
    try {
      const response = await fetch(`${API_URL}/auth/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token.value}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        token.value = null
        user.value = null
        isAuthenticated.value = false

        localStorage.removeItem('token')

        await router.push('/login')

        return true
      }

      return false
    } catch (error) {
      console.error('Logout failed:', error)
      return false
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    logout
  }
})
