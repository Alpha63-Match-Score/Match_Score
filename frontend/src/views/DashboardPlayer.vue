<template>
  <div class="dashboard-wrapper">
    <HeaderSection />

    <div class="content-wrapper">
      <v-container>
        <!-- Director Welcome Section -->
        <DashboardWelcome :userRole="player?.username" />

        <v-row class="dashboard-row">
          <!-- Player Profile Column -->
          <v-col cols="12" md="6">
            <PlayerCard
              :player="player"
              @edit="openEdit"
              @avatar-upload="openAvatarUpload"
            />
            <EditDialog
              v-model="showEditDialog"
              :player="player"
              :edit-field="editField"
              :edit-value="editValue"
              :edit-first-name="editFirstName"
              :edit-last-name="editLastName"
              @update:modelValue="showEditDialog = $event"
              @update:editValue="editValue = $event"
              @update:editFirstName="editFirstName = $event"
              @update:editLastName="editLastName = $event"
              @profile-updated="handleProfileUpdated"
            />
            <AvatarUploadDialog
              v-model="showAvatarDialog"
              :player="player"
              @avatar-updated="handleAvatarUpdated"
            />

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
                  You have not submitted any requests.
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
import HeaderSection from "@/components/HeaderSection.vue";
import DashboardWelcome from "@/components/DashboardWelcome.vue";
import PlayerCard from "@/components/PlayerCard.vue";
import EditDialog from "@/components/dialogs/EditDialog.vue";
import AddPlayerDialog from "@/components/dialogs/AddPlayerDialog.vue";
import AvatarUploadDialog from "@/components/dialogs/AvatarUploadDialog.vue";

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

// Add error refs
const usernameError = ref('')
const firstNameError = ref('')
const lastNameError = ref('')
const countryError = ref('')

// Add clear errors function
const clearErrors = () => {
  usernameError.value = ''
  firstNameError.value = ''
  lastNameError.value = ''
  countryError.value = ''
}

// Methods


const rules = {
  required: (v: string) => !!v || 'This field is required',
  username: [
    (value) => !!value || 'Username is required',
    (value) => value.length >= 5 || 'Username must be at least 5 characters',
    (value) => value.length <= 15 || 'Username must not exceed 15 characters',
    (value) => /^[a-zA-Z0-9_-]+$/.test(value) || 'Username can only contain letters, numbers, underscores, or dashes',
  ],
  firstName: [
    (value) => !!value || 'First name is required',
    (value) => value.length >= 2 || 'First name must be at least 2 characters',
    (value) => value.length <= 25 || 'First name must not exceed 25 characters',
    (value) => /^[a-zA-Z]+(?:[-a-zA-Z]+)?$/.test(value) || 'Invalid first name format',
  ],
  lastName: [
    (value) => !!value || 'Last name is required',
    (value) => value.length >= 2 || 'Last name must be at least 2 characters',
    (value) => value.length <= 25 || 'Last name must not exceed 25 characters',
    (value) => /^[a-zA-Z]+(?:[-a-zA-Z]+)?$/.test(value) || 'Invalid last name format',
  ],
  country: [
    (value) => !!value || 'Country is required',
    (value) => value.length >= 2 || 'Country must be at least 2 characters',
    (value) => value.length <= 25 || 'Country must not exceed 25 characters',
    (value) => /^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$/.test(value) || 'Invalid country format',
  ],
}

const handleProfileUpdated = async () => {
  await fetchPlayer()
  showSuccessAlert.value = true
  successMessage.value = 'Profile updated successfully!'
}

const handleAvatarUpdated = async () => {
  await fetchPlayer()
  showSuccessAlert.value = true
  successMessage.value = 'Avatar updated successfully!'
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

const hasValidChanges = computed(() => {
  if (!player.value || usernameError.value || firstNameError.value || lastNameError.value || countryError.value) {
    return false;
  }

  if (editField.value === 'username') {
    return editValue.value !== player.value.username &&
           rules.username.every(rule => rule(editValue.value) === true);
  }

  if (editField.value === 'name') {
    return (editFirstName.value !== player.value.first_name || editLastName.value !== player.value.last_name) &&
           rules.firstName.every(rule => rule(editFirstName.value) === true) &&
           rules.lastName.every(rule => rule(editLastName.value) === true);
  }

  if (editField.value === 'country') {
    return editValue.value !== player.value.country &&
           rules.country.every(rule => rule(editValue.value) === true);
  }

  if (editField.value === 'team') {
    return editValue.value !== player.value.team_name;
  }

  return false;
});

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
    teams.value = data.map(team => ({
      name: team.name,
    }))
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
  console.log('Opening edit dialog with field:', field)
  editField.value = field
  editError.value = ''

  if (field === 'name') {
    editFirstName.value = player.value?.first_name || ''
    editLastName.value = player.value?.last_name || ''
    console.log('Setting name values:', {
      first: editFirstName.value,
      last: editLastName.value
    })
  } else if (field === 'team') {
    editValue.value = player.value?.team_name || ''
    await fetchTeams()
    console.log('Setting team value:', editValue.value)
  } else {
    editValue.value = player.value?.[field as keyof Player]?.toString() || ''
    console.log('Setting field value:', editValue.value)
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
  clearErrors()
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
  clearErrors()
  if (!player.value) return

  try {
    isSaving.value = true
    editError.value = ''
    if (editField.value === 'username') {
      if (!rules.username.every(rule => rule(editValue.value) === true)) {
        usernameError.value = 'Invalid username format'
        return
      }
    } else if (editField.value === 'name') {
      if (!rules.firstName.every(rule => rule(editFirstName.value) === true)) {
        firstNameError.value = 'Invalid first name format'
        return
      }
      if (!rules.lastName.every(rule => rule(editLastName.value) === true)) {
        lastNameError.value = 'Invalid last name format'
        return
      }
    } else if (editField.value === 'country') {
      if (!rules.country.every(rule => rule(editValue.value) === true)) {
        countryError.value = 'Invalid country format'
        return
      }
    }

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
  console.log('Opening avatar upload dialog')
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
.dashboard-wrapper {
  min-height: 100vh;
  position: relative;
}

.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 100px;
  min-height: 100vh;
  width: 100vw;
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

.dialog-actions {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: -32px;
}

.cancel-btn {
  background: transparent !important;
  color: #42DDF2FF !important;
  border: 2px solid #42DDF2FF !important;
  border-radius: 50px !important;
  padding: 0 24px !important;
  height: 40px !important;
  text-transform: none !important;
}

.cancel-btn:hover {
  background: rgba(66, 221, 242, 0.1) !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  border-radius: 50px !important;
  padding: 0 24px !important;
  height: 40px !important;
  text-transform: none !important;
}

.submit-btn:hover {
  background: #FED854FF !important;
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.3);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: rgba(66, 221, 242, 0.5) !important;
}

:deep(.v-btn) {
  text-transform: none !important;
  padding: 0 24px !important;
  height: 40px !important;
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


:deep(.teams-menu) {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 1px solid rgba(66, 221, 242, 0.3);
  max-height: 300px !important;
  overflow-y: auto;
}

:deep(.teams-menu::-webkit-scrollbar) {
  width: 8px;
}

:deep(.teams-menu::-webkit-scrollbar-track) {
  background: transparent;
}

:deep(.teams-menu::-webkit-scrollbar-thumb) {
  background: rgba(66, 221, 242, 0.3);
  border-radius: 4px;
}

:deep(.teams-menu::-webkit-scrollbar-thumb:hover) {
  background: rgba(66, 221, 242, 0.5);
}

:deep(.v-select__selection) {
  color: white !important;
  opacity: 1 !important;
}

:deep(.v-select .v-field__input) {
  min-height: 56px !important;
  opacity: 1 !important;
  color: white !important;
}

:deep(.v-select .v-field) {
  background: transparent !important;
}

/* Update error message styling */
:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
  display: block !important;
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


:deep(.teams-menu) {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 1px solid rgba(66, 221, 242, 0.3);
  max-height: 300px !important;
  overflow-y: auto;
}

:deep(.teams-menu::-webkit-scrollbar) {
  width: 8px;
}

:deep(.teams-menu::-webkit-scrollbar-track) {
  background: transparent;
}

:deep(.teams-menu::-webkit-scrollbar-thumb) {
  background: rgba(66, 221, 242, 0.3);
  border-radius: 4px;
}

:deep(.teams-menu::-webkit-scrollbar-thumb:hover) {
  background: rgba(66, 221, 242, 0.5);
}

:deep(.v-select__selection) {
  color: white !important;
  opacity: 1 !important;
}

:deep(.v-select .v-field__input) {
  min-height: 56px !important;
  opacity: 1 !important;
  color: white !important;
}

:deep(.v-select .v-field) {
  background: transparent !important;
}

/* Update error message styling */
:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
  display: block !important;
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

.dialog-actions {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: -32px;
}

.cancel-btn {
  background: transparent !important;
  color: #42DDF2FF !important;
  border: 2px solid #42DDF2FF !important;
  border-radius: 50px !important;
  padding: 0 24px !important;
  height: 40px !important;
  text-transform: none !important;
}

.cancel-btn:hover {
  background: rgba(66, 221, 242, 0.1) !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  border-radius: 50px !important;
  padding: 0 24px !important;
  height: 40px !important;
  text-transform: none !important;
}

.submit-btn:hover {
  background: #FED854FF !important;
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.3);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: rgba(66, 221, 242, 0.5) !important;
}

:deep(.v-btn) {
  text-transform: none !important;
  padding: 0 24px !important;
  height: 40px !important;
}
</style>
