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
            <h2 class="welcome-text">Welcome, {{ userEmail }}</h2>
          </div>
        </div>

        <v-row class="dashboard-row">
          <!-- Player Profile Column -->
          <v-col cols="12" md="6">
              <div class="player-card">
                <div class="player-background"></div>
                <div class="player-content">
                  <!-- Top Section with Avatar and Main Info -->
                  <div class="player-main-info">
                    <!-- Avatar Section -->
                    <div class="avatar-section">
                      <v-avatar size="150" class="player-avatar" @click="openAvatarUpload">
                        <v-img v-if="player?.avatar" :src="player.avatar" alt="Player avatar"></v-img>
                        <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="80"></v-icon>
                      </v-avatar>
                    </div>

                    <!-- Player Info -->
                    <div class="info-section">
                      <div class="info-row">
                        <div class="username">{{ player?.username }}</div>
                        <v-icon
                          icon="mdi-pencil"
                          class="edit-icon"
                          @click="openEdit('username')"
                        ></v-icon>
                      </div>

                      <div class="info-row">
                        <div class="full-name">
                          {{ player?.first_name }} {{ player?.last_name }}
                          <v-icon
                            icon="mdi-pencil"
                            class="edit-icon"
                            @click="openEdit('name')"
                          ></v-icon>
                        </div>
                      </div>

                      <div class="info-row">
                        <div class="country">
                          <v-icon icon="mdi-earth" class="info-icon"></v-icon>
                          {{ player?.country }}
                        </div>
                        <v-icon
                          icon="mdi-pencil"
                          class="edit-icon"
                          @click="openEdit('country')"
                        ></v-icon>
                      </div>

                      <div class="info-row">
                        <div class="team">
                          <v-icon icon="mdi-account-group" class="info-icon"></v-icon>
                          {{ player?.team_name }}
                        </div>
                        <v-icon
                          icon="mdi-pencil"
                          class="edit-icon"
                          @click="openEdit('team')"
                        ></v-icon>
                      </div>
                    </div>
                  </div>

                  <!-- Bottom Section with Stats and Tournament -->
                  <div class="player-stats-section">
                    <!-- Stats Section -->
                    <div class="stats-container">
                      <div class="stats-header">My stats</div>
                      <div class="progress-wrapper">
                        <v-progress-linear
                          :model-value="parseInt(player?.game_win_ratio)"
                          color="#42DDF2FF"
                          height="8"
                          rounded
                          class="progress-bar"
                        ></v-progress-linear>
                        <span class="win-ratio">{{ player?.game_win_ratio }}</span>
                      </div>
                    </div>

                    <!-- Tournament Section -->
                    <div v-if="player?.current_tournament_title" class="tournament-container">
                      <div class="tournament-header">Current tournament</div>
                      <div class="tournament-name">
                        <v-icon icon="mdi-trophy" class="tournament-icon"></v-icon>
                        {{ player.current_tournament_title }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            <!-- Edit Dialog -->
            <v-dialog v-model="showEditDialog" max-width="500">
            <v-card class="edit-dialog">
              <v-card-title>{{ editDialogTitle }}</v-card-title>
              <v-card-text>
                <v-alert
                  v-if="editError"
                  type="error"
                  variant="tonal"
                  class="mb-4"
                >
                  {{ editError }}
                </v-alert>

                <!-- Username Edit -->
                <v-text-field
                  v-if="editField === 'username'"
                  v-model="editValue"
                  label="Username"
                  variant="outlined"
                ></v-text-field>

                <!-- Name Edit -->
                <div v-if="editField === 'name'" class="d-flex gap-2">
                  <v-text-field
                    v-model="editFirstName"
                    label="First Name"
                    variant="outlined"
                  ></v-text-field>
                  <v-text-field
                    v-model="editLastName"
                    label="Last Name"
                    variant="outlined"
                  ></v-text-field>
                </div>

                <!-- Country Edit -->
                <v-text-field
                  v-if="editField === 'country'"
                  v-model="editValue"
                  label="Country"
                  variant="outlined"
                ></v-text-field>

                <!-- Team Edit -->
                <div v-if="editField === 'team'">
                  <v-select
                    v-model="editValue"
                    :items="teams"
                    :loading="isLoadingTeams"
                    item-title="name"
                    item-value="name"
                    label="Select Team"
                    variant="outlined"
                    :error-messages="teamsError"
                    :disabled="isLoadingTeams"
                    clearable
                  >
                    <template v-slot:prepend>
                      <v-icon icon="mdi-account-group" color="#42DDF2FF"></v-icon>
                    </template>
                  </v-select>
                  <div v-if="teamsError" class="text-caption error-text mt-2">
                    {{ teamsError }}
                  </div>
                </div>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="error" @click="closeEditDialog">Cancel</v-btn>
                <v-btn color="primary" @click="saveEdit" :loading="isSaving">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

            <!-- Avatar Upload Dialog -->
            <v-dialog v-model="showAvatarDialog" max-width="500">
              <v-card class="edit-dialog">
                <v-card-title>Update Avatar</v-card-title>
                <v-card-text>
                  <v-alert
                    v-if="avatarError"
                    type="error"
                    variant="tonal"
                    class="mb-4"
                  >
                    {{ avatarError }}
                  </v-alert>

                  <v-file-input
                    v-model="avatarFile"
                    accept="image/*"
                    label="Choose avatar"
                    prepend-icon="mdi-camera"
                    variant="outlined"
                    @change="handleAvatarPreview"
                  ></v-file-input>

                  <div v-if="avatarPreview" class="avatar-preview">
                    <img :src="avatarPreview" alt="Avatar preview" />
                  </div>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="error" @click="closeAvatarDialog">Cancel</v-btn>
                  <v-btn
                    color="primary"
                    @click="uploadAvatar"
                    :loading="isUploading"
                    :disabled="!avatarFile"
                  >
                    Upload
                  </v-btn>
                </v-card-actions>
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
          </v-col>


        <!-- Request History Section -->
          <v-col cols="12" md="6">
            <div class="history-card">
          <div class="history-background"></div>
          <div class="history-content">
            <h3 class="section-title">Request History</h3>

            <!-- Loading state -->
            <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 200px">
              <v-progress-circular indeterminate color="#42DDF2FF"></v-progress-circular>
            </div>

            <!-- Error state -->
            <div v-else-if="requestHistoryError" class="error-message">
              {{ requestHistoryError }}
            </div>

            <!-- Request list -->
            <div v-else-if="requests.length > 0" class="request-list">
              <div v-for="request in requests" :key="request.request_date" class="request-item">
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

                <!-- Player Link Dialog -->
                <v-dialog v-model="showPlayerLinkDialog" max-width="500">
                  <v-card class="dialog-card">
                    <div class="dialog-background"></div>
                    <div class="dialog-content">
                      <v-card-title class="dialog-title">
                        <span>Link Player Profile</span>
                      </v-card-title>
                      <v-card-text>
                        <v-text-field
                          v-model="playerUsername"
                          label="Player Username"
                          variant="outlined"
                          :rules="[rules.required]"
                          class="player-username-input"
                        ></v-text-field>

                        <!-- Display Error for Player Link -->
                        <div v-if="playerLinkError" class="error-message">
                          {{ playerLinkError }}
                        </div>
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

            <!-- Empty state -->
            <div v-else class="error-message">
              No requests found. Start by submitting a new request!
            </div>
          </div>
        </div>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { API_URL } from '@/config'
import { format } from 'date-fns'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const userEmail = ref(authStore.userEmail)


interface Player {
  id: string
  username: string
  first_name: string
  last_name: string
  country: string
  user_email: string
  team_name: string
  avatar: string | null
  game_win_ratio: string
  current_tournament_title: string | null
}

interface Team {
  id: string
  name: string
}

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

// State
const teams = ref<Team[]>([])
const isLoadingTeams = ref(false)
const teamsError = ref('')
const requests = ref<Request[]>([])
const requestHistoryError = ref<string | null>(null) // Scoped error for Request History
const playerLinkError = ref<string | null>(null) // Scoped error for Player Link Dialog
const showPlayerLinkDialog = ref(false)
const playerUsername = ref('')
const isSubmitting = ref(false)

const player = ref<Player | null>(null)
const isLoading = ref(true)
const error = ref<string | null>(null)

// Edit Dialog State
const showEditDialog = ref(false)
const editField = ref('')
const editValue = ref('')
const editFirstName = ref('')
const editLastName = ref('')
const editError = ref('')
const isSaving = ref(false)

// Avatar Dialog State
const showAvatarDialog = ref(false)
const avatarFile = ref<File | null>(null)
const avatarPreview = ref<string | null>(null)
const avatarError = ref('')
const isUploading = ref(false)

// Success Alert State
const showSuccessAlert = ref(false)
const successMessage = ref('')

// Computed
const editDialogTitle = computed(() => {
  const titles: Record<string, string> = {
    username: 'Edit Username',
    name: 'Edit Name',
    country: 'Edit Country',
    team: 'Edit Team Name'
  }
  return titles[editField.value] || 'Edit Profile'
})

// Methods


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

const fetchTeams = async () => {
  try {
    isLoadingTeams.value = true
    teamsError.value = ''

    const response = await fetch(`${API_URL}/teams`, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })

    if (!response.ok) {
      const errorMessage = await extractErrorMessage(response)
      throw new Error(errorMessage)
    }

    const data = await response.json()
    teams.value = data
  } catch (e) {
    console.error('Error fetching teams:', e)
    teamsError.value = e.message || 'Failed to load teams'
  } finally {
    isLoadingTeams.value = false
  }
}

const fetchRequests = async () => {
  try {
    isLoading.value = true;
    requestHistoryError.value = null;

    const response = await fetch(
      `${API_URL}/requests/me?offset=0&limit=10`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch requests');
    }

    const data = await response.json();

    requests.value = [...data];

  } catch (e) {
    console.error('Error fetching requests:', e);
    requestHistoryError.value = e.message || 'Failed to load request history. Please try again later.';
  } finally {
    isLoading.value = false;
  }
};

const submitPlayerLink = async () => {
  if (!playerUsername.value) {
    playerLinkError.value = 'Player username is required.';
    return;
  }

  try {
    isSubmitting.value = true;
    playerLinkError.value = null;

    const existingRequest = requests.value.some(
      (request) => request.request_type === 'link player profile' && request.username === playerUsername.value && request.status === 'pending'
    );

    if (existingRequest) {
      playerLinkError.value = 'You already have a pending request.';
      return;
    }

    const response = await fetch(`${API_URL}/requests/players/${playerUsername.value}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      },
    });

    if (response.status === 404) {
      playerLinkError.value = `Player with username "${playerUsername.value}" was not found.`;
      return;
    }

    if (!response.ok) throw new Error('Failed to submit request');

    showPlayerLinkDialog.value = false;
    successMessage.value = 'Player link request submitted successfully. An admin will review your request shortly.';
    showSuccessAlert.value = true;
    fetchRequests();
  } catch (e) {
    console.error('Error submitting player link request:', e);
    playerLinkError.value = 'Failed to submit request. Please try again.';
  } finally {
    isSubmitting.value = false;
  }
};

const fetchPlayer = async () => {
  try {
    isLoading.value = true
    error.value = null
    const response = await fetch(`${API_URL}/players/users`, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    if (!response.ok) throw new Error('Failed to fetch player details')
    player.value = await response.json()
  } catch (e) {
    console.error('Error fetching player:', e)
    error.value = 'Failed to load player details'
  } finally {
    isLoading.value = false
  }
}

const openEdit = async (field: string) => {
  editField.value = field
  editError.value = ''

  if (field === 'name') {
    editFirstName.value = player.value?.first_name || ''
    editLastName.value = player.value?.last_name || ''
  } else {
    editValue.value = player.value?.[field as keyof Player]?.toString() || ''
  }

  if (field === 'team') {
    await fetchTeams()
  }

  showEditDialog.value = true
}

const closeEditDialog = () => {
  showEditDialog.value = false
  editField.value = ''
  editValue.value = ''
  editFirstName.value = ''
  editLastName.value = ''
  editError.value = ''
}

const extractErrorMessage = async (response: Response) => {
  try {
    const responseClone = response.clone()
    const text = await responseClone.text()
    const data = JSON.parse(text)

    // За FastAPI validation errors
    if (data.detail && Array.isArray(data.detail) && data.detail.length > 0) {
      return data.detail[0].msg
    }

    // За HTTP exceptions
    if (data.detail && typeof data.detail === 'string') {
      return data.detail
    }

    return 'An error occurred'
  } catch (e) {
    console.error('Error extracting message:', e)
    return 'An error occurred'
  }
}


const saveEdit = async () => {
  if (!player.value) return

  try {
    isSaving.value = true
    editError.value = ''

    let params = new URLSearchParams()

if (editField.value === 'name') {
      params.append('first_name', editFirstName.value)
      params.append('last_name', editLastName.value)
    } else if (editField.value === 'team') {
      params.append('team_name', editValue.value)
    } else {
      params.append(editField.value, editValue.value)
    }

    console.log('Sending params:', params.toString())

    const response = await fetch(
      `${API_URL}/players/${player.value.id}?${params.toString()}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
        // Премахнахме body: JSON.stringify({ 'avatar': '' })
      }
    )

    console.log('Response status:', response.status)

    const responseData = await response.json()
    console.log('Response data:', responseData)

    if (!response.ok) {
      editError.value = responseData.detail || responseData.message || 'Failed to update profile'
      throw new Error(editError.value)
    }

    await fetchPlayer()
    showEditDialog.value = false
    successMessage.value = 'Profile updated successfully'
    showSuccessAlert.value = true

  } catch (e) {
    console.error('Full error object:', e)
    if (!editError.value) {
      editError.value = 'Failed to update profile. Please try again.'
    }
  } finally {
    isSaving.value = false
  }
}

const openAvatarUpload = () => {
  avatarFile.value = null
  avatarPreview.value = null
  avatarError.value = ''
  showAvatarDialog.value = true
}

const closeAvatarDialog = () => {
  showAvatarDialog.value = false
  avatarFile.value = null
  avatarPreview.value = null
  avatarError.value = ''
}

const handleAvatarPreview = (file: File) => {
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    avatarPreview.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
}

const uploadAvatar = async () => {
  if (!player.value || !avatarFile.value) return

  try {
    isUploading.value = true
    avatarError.value = ''

    const formData = new FormData()
    formData.append('avatar', avatarFile.value)

    const response = await fetch(`${API_URL}/players/${player.value.id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      },
      body: formData
    })

    if (!response.ok) {
      avatarError.value = await extractErrorMessage(response)
      throw new Error(avatarError.value)
    }

    await fetchPlayer()
    showAvatarDialog.value = false
    successMessage.value = 'Avatar updated successfully'
    showSuccessAlert.value = true
  } catch (e) {
    console.error('Upload error:', e)
    if (!avatarError.value) {
      avatarError.value = 'Failed to upload avatar'
    }
  } finally {
    isUploading.value = false
  }
}

onMounted(() => {
  fetchRequests()
  fetchPlayer()
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

/*:deep(.v-field__input:-webkit-autofill) {*/
/*  -webkit-box-shadow: 0 0 0 30px rgba(45, 55, 75, 0.8) inset !important;*/
/*  -webkit-text-fill-color: white !important;*/
/*}*/

.header-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px;
  background: linear-gradient(
    to bottom,
    rgba(23, 28, 38, 0) 0%,
    rgba(23, 28, 38, 0.8) 30%,
    rgba(23, 28, 38, 1) 60%
  );
  z-index: 2;
}

.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 50px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100vw !important;
  margin-bottom: 100px;
}

.welcome-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
  margin-bottom: 24px;
  padding: 24px;
  width: 55%;
  margin-left: auto;
  margin-right: auto;
}

.welcome-content,
.actions-content,
.history-content {
  position: relative;
  z-index: 2;
}

.dialog-title {
  color: #42ddf2; /* Customize the title color */
  font-weight: bold;
  font-size: 1.25rem;
  text-align: center;
}

.player-username-input {
  margin-top: 16px;
}

.error-message {
  color: #fed854; /* Error text color */
  font-size: 0.9rem;
  margin-top: 8px;
  text-align: center;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 14px;
}

:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

:deep(.v-field--variant-outlined.v-field--error) {
  border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline) {
  color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline__start),
:deep(.v-field--error .v-field__outline__end),
:deep(.v-field--error .v-field__outline__notch) {
  border-color: #fed854 !important;
}

:deep(.v-alert) {
  background-color: rgba(254, 216, 84, 0.1) !important;
  color: #fed854 !important;
  border-color: #fed854 !important;
}

:deep(.v-alert__close-button) {
  color: #fed854 !important;
}

:deep(.v-alert__prepend) {
  color: #fed854 !important;
}

:deep(.v-alert__content) {
  color: #fed854 !important;
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
  text-align: center; /* Centers the text horizontally */
  display: flex; /* Enables Flexbox for vertical alignment */
  align-items: center; /* Centers the text vertically */
  justify-content: center; /* Ensures content is centered horizontally */
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
  color: #fed854;
  padding: 16px;
}

.dashboard-row {
  width: 90%;
  margin-left: auto;
  margin-right: auto;
}

.player-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  margin-bottom: 24px;
  padding: 24px;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  min-height: 500px;
}



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
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  min-height: 500px;
}

.player-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-position: center;
  background-size: cover;
  opacity: 0.1;
  z-index: 1;
}

.player-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: 32px;
}

.player-main-info {
  display: flex;
  gap: 32px;
}

.avatar-section {
  flex-shrink: 0;
}

.player-avatar {
  border: 3px solid #42DDF2FF;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.player-avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 0 20px rgba(66, 221, 242, 0.4);
}


.info-section {
  flex-grow: 1
}

.info-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  color: #42DDF2FF;
  font-size: 1.8rem;
  font-weight: 500;
  text-shadow: 0 0 10px rgba(66, 221, 242, 0.3);
}

.full-name {
  color: white;
  font-size: 1.4rem;
}

.country, .team {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-icon {
  color: #42DDF2FF !important;
}

.edit-icon {
  color: #42DDF2FF;
  opacity: 0.7;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-icon:hover {
  opacity: 1;
  transform: scale(1.1);
}

.player-stats-section {
  margin-top: auto;
  padding-top: 24px;
  border-top: 1px solid rgba(66, 221, 242, 0.2);
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-container, .tournament-container {
  background: rgba(45, 55, 75, 0.5);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(66, 221, 242, 0.3);
}

.stats-header, .tournament-header {
  color: #42DDF2FF;
  font-size: 1.1rem;
  margin-bottom: 12px;
  font-weight: 500;
}

.progress-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  flex-grow: 1;
}

.win-ratio {
  color: #42ddf2;
  font-size: 1.1rem;
  min-width: 45px;
  font-weight: 500;
}

.tournament-name {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #FED854FF;
  font-size: 1.1rem;
}

.tournament-icon {
  color: #FED854FF !important;
}

/* Edit Dialog Styling */
.edit-dialog {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
}

:deep(.v-card-title) {
  color: #42DDF2FF !important;
  font-size: 1.4rem;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(66, 221, 242, 0.2);
}

:deep(.v-card-text) {
  padding: 24px;
}

:deep(.v-field) {
  border-color: rgba(66, 221, 242, 0.3) !important;
}

:deep(.v-field:hover) {
  border-color: #42ddf2 !important;
}

:deep(.v-field.v-field--focused) {
  border-color: #42ddf2 !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.v-field__input) {
  color: white !important;
}

:deep(.v-text-field input) {
  color: white !important;
}

:deep(.v-field__outline) {
  color: rgba(66, 221, 242, 0.3) !important;
}

:deep(.v-icon) {
  color: rgba(255, 255, 255, 0.7) !important;
}

/* File Input Styling */
:deep(.v-file-input) {
  margin-top: 16px;
}

.avatar-preview {
  margin-top: 16px;
  text-align: center;
}

.avatar-preview img {
  max-width: 200px;
  border-radius: 50%;
  border: 2px solid #42DDF2FF;
}

/* Alert Styling */
:deep(.v-alert) {
  background-color: rgba(254, 216, 84, 0.1) !important;
  color: #fed854 !important;
  border-color: #fed854 !important;
}

:deep(.v-alert__close-button) {
  color: #fed854 !important;
}

:deep(.v-alert__prepend) {
  color: #fed854 !important;
}

:deep(.v-card-actions) {
  padding: 16px 24px;
  border-top: 1px solid rgba(66, 221, 242, 0.2);
}

:deep(.v-btn) {
  text-transform: none !important;
}

:deep(.v-btn.v-btn--variant-flat) {
  background: #42DDF2FF !important;
  color: #171c26 !important;
}

:deep(.v-btn.v-btn--variant-flat:hover) {
  background: #FED854FF !important;
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.3);
}

:deep(.v-btn.error) {
  background: transparent !important;
  color: #42DDF2FF !important;
  border: 1px solid #42DDF2FF;
}

:deep(.v-btn.error:hover) {
  background: rgba(66, 221, 242, 0.1) !important;
}

:deep(.v-btn.primary) {
  background: #42DDF2FF !important;
  color: #171c26 !important;
}

:deep(.v-btn.primary:hover) {
  background: #FED854FF !important;
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.3);
}

</style>
