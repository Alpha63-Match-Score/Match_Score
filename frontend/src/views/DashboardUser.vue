<template>
  <div class="home-wrapper">
    <!-- Header with fade effect -->
    <div class="header-image"></div>
    <div class="header-overlay"></div>

    <div class="content-wrapper">
      <v-container>
        <!-- User Welcome Section -->
        <div class="welcome-card">
          <div class="welcome-background"></div>
          <div class="welcome-content">
            <v-icon icon="mdi-account-circle" size="48" class="welcome-icon"></v-icon>
            <h2 class="welcome-text">Welcome, {{ userEmail }}</h2>
          </div>
        </div>

        <!-- Request Buttons Section -->
        <div class="actions-card">
          <div class="actions-background"></div>
          <div class="actions-content">
            <h3 class="section-title">Available Actions</h3>
            <div class="actions-buttons">
              <v-btn
                class="action-btn"
                prepend-icon="mdi-shield-account"
                @click="openDirectorRequest"
              >
                Request Director Role
              </v-btn>
              <v-btn
                class="action-btn"
                prepend-icon="mdi-account-plus"
                @click="openPlayerLinkDialog"
              >
                Link Player Profile
              </v-btn>
            </div>
          </div>
        </div>

        <!-- Request History Section -->
        <div class="history-card">
          <div class="history-background"></div>
          <div class="history-content">
            <h3 class="section-title">Request History</h3>

            <!-- Loading state -->
            <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 200px">
              <v-progress-circular indeterminate color="#42DDF2FF"></v-progress-circular>
            </div>

            <!-- Error state -->
            <div v-else-if="error" class="error-message">
              {{ error }}
            </div>

            <!-- Request list -->
            <div v-else class="request-list">
              <div v-for="request in requests" :key="request.id" class="request-item">
                <div class="request-header">
                  <div class="request-type">
                    <v-icon
                      :icon="getRequestTypeIcon(request.request_type)"
                      class="request-icon"
                    ></v-icon>
                    {{ formatRequestType(request.request_type) }}
                  </div>
                  <div :class="['status-tag', `status-${request.status}`]">
                    {{ formatStatus(request.status) }}
                  </div>
                </div>

                <div class="request-details">
                  <div class="detail-item">
                    <v-icon icon="mdi-calendar" size="small" class="detail-icon"></v-icon>
                    {{ formatDate(request.request_date) }}
                  </div>
                  <div v-if="request.username" class="detail-item">
                    <v-icon icon="mdi-account" size="small" class="detail-icon"></v-icon>
                    Player: {{ request.username }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </v-container>
    </div>

    <!-- Player Link Dialog -->
    <v-dialog v-model="showPlayerLinkDialog" max-width="500">
      <v-card class="dialog-card">
        <div class="dialog-background"></div>
        <div class="dialog-content">
          <v-card-title>Link Player Profile</v-card-title>
          <v-card-text>
            <v-text-field
              v-model="playerUsername"
              label="Player Username"
              variant="outlined"
              :rules="[rules.required]"
            ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              class="cancel-btn"
              @click="showPlayerLinkDialog = false"
            >
              Cancel
            </v-btn>
            <v-btn
              class="submit-btn"
              @click="submitPlayerLink"
              :loading="isSubmitting"
            >
              Submit
            </v-btn>
          </v-card-actions>
        </div>
      </v-card>
    </v-dialog>

    <!-- Success Alert -->
    <v-snackbar
      v-model="showSuccessAlert"
      color="success"
      timeout="3000"
    >
      {{ successMessage }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { format } from 'date-fns'
import { API_URL } from '@/config'

const authStore = useAuthStore()
const userEmail = ref(authStore.userEmail)

// Data
interface Request {
  id: string
  email: string
  request_type: string
  status: string
  request_date: string
  response_date: string | null
  admin_id: string | null
  username: string | null
}

const requests = ref<Request[]>([])
const isLoading = ref(true)
const error = ref<string | null>(null)
const showPlayerLinkDialog = ref(false)
const playerUsername = ref('')
const isSubmitting = ref(false)
const showSuccessAlert = ref(false)
const successMessage = ref('')

const rules = {
  required: (v: string) => !!v || 'This field is required'
}

// Methods
const formatRequestType = (type: string): string => {
  return type.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

const formatStatus = (status: string): string => {
  return status.charAt(0).toUpperCase() + status.slice(1)
}

const formatDate = (date: string): string => {
  return format(new Date(date), 'dd MMM yyyy, HH:mm')
}

const getRequestTypeIcon = (type: string): string => {
  return type === 'promote user to director' ? 'mdi-shield-account' : 'mdi-account-plus'
}

const fetchRequests = async () => {
  try {
    isLoading.value = true
    error.value = null
    const response = await fetch(
      `${API_URL}/requests/?sort_by=desc&filter_by_current_user=true&offset=0`
    )
    if (!response.ok) throw new Error('Failed to fetch requests')
    const data = await response.json()
    requests.value = Array.isArray(data) ? data : (data.results || [])
  } catch (e) {
    console.error('Error fetching requests:', e)
    error.value = 'Failed to load request history. Please try again later.'
  } finally {
    isLoading.value = false
  }
}

const openDirectorRequest = async () => {
  try {
    isSubmitting.value = true
    const response = await fetch(`${API_URL}/requests/directors/${authStore.userEmail}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    if (!response.ok) throw new Error('Failed to submit request')

    successMessage.value = 'Director role request submitted successfully. An admin will review your request shortly.'
    showSuccessAlert.value = true
    fetchRequests() // Refresh the list
  } catch (e) {
    console.error('Error submitting director request:', e)
    error.value = 'Failed to submit request. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

const openPlayerLinkDialog = () => {
  playerUsername.value = ''
  showPlayerLinkDialog.value = true
}

const submitPlayerLink = async () => {
  if (!playerUsername.value) return

  try {
    isSubmitting.value = true
    const response = await fetch(`${API_URL}/requests/players/${playerUsername.value}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    if (!response.ok) throw new Error('Failed to submit request')

    showPlayerLinkDialog.value = false
    successMessage.value = 'Player link request submitted successfully. An admin will review your request shortly.'
    showSuccessAlert.value = true
    fetchRequests() // Refresh the list
  } catch (e) {
    console.error('Error submitting player link request:', e)
    error.value = 'Failed to submit request. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  fetchRequests()
})
</script>

<style scoped>
.header-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px;
  background-image: url('@/assets/top-image.png');
  background-size: cover;
  background-position: center;
  z-index: 1;
  opacity: 0.6;
}

.header-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px;
  background: linear-gradient(
    to bottom,
    rgba(23, 28, 38, 0) 0%,
    rgba(23, 28, 38, 0.8) 80%,
    rgba(23, 28, 38, 1) 100%
  );
  z-index: 2;
}

.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 250px;
  min-height: 100vh;
  width: 100vw !important;
}

.welcome-card,
.actions-card,
.history-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  margin-bottom: 24px;
  padding: 24px;
}

.welcome-content,
.actions-content,
.history-content {
  position: relative;
  z-index: 2;
}

.welcome-icon {
  color: #42DDF2FF !important;
  margin-bottom: 16px;
}

.welcome-text {
  color: #42DDF2FF;
  font-size: 1.8rem;
  text-align: center;
  margin: 0;
}

.section-title {
  color: #42DDF2FF;
  font-size: 1.4rem;
  margin-bottom: 24px;
  text-align: center;
}

.actions-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.action-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  font-weight: bold;
  padding: 20px 32px !important;
}

.action-btn:hover {
  background: #FED854FF !important;
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.3);
}

.request-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.request-item {
  background: rgba(45, 55, 75, 0.8);
  border: 1px solid rgba(8, 87, 144, 0.2);
  border-radius: 10px;
  padding: 16px;
  transition: all 0.2s;
}

.request-item:hover {
  background: rgb(45, 55, 75);
  border-color: #42DDF2FF;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(8, 117, 176, 0.2);
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.request-type {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-weight: 500;
}

.request-icon {
  color: #42DDF2FF !important;
}

.status-tag {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.9rem;
}

.status-pending {
  background: rgba(254, 216, 84, 0.1);
  color: #FED854FF;
  border: 1px solid rgba(254, 216, 84, 0.3);
}

.status-accepted {
  background: rgba(0, 255, 157, 0.1);
  color: #00ff9d;
  border: 1px solid rgba(0, 255, 157, 0.3);
}

.status-rejected {
  background: rgba(255, 99, 99, 0.1);
  color: #ff6363;
  border: 1px solid rgba(255, 99, 99, 0.3);
}

.request-details {
  display: flex;
  gap: 24px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.detail-icon {
  color: #42DDF2FF !important;
}

.dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
}

.dialog-content {
  padding: 24px;
}

:deep(.v-text-field) {
  margin-top: 24px;
}

.cancel-btn {
  color: #42DDF2FF !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  margin-left: 16px;
}

.error-message {
  text-align: center;
  color: #ff6363;
  padding: 16px;
}
</style>
