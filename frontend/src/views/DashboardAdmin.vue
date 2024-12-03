<template>
  <div class="home-wrapper">
    <!-- Header with fade effect -->
    <div class="header-image"></div>
    <div class="header-overlay"></div>

    <div class="content-wrapper">
      <v-container>
        <!-- Admin Welcome Section -->
        <div class="welcome-card">
          <div class="welcome-background"></div>
          <div class="welcome-content">
            <h2 class="welcome-text">Welcome, Admin </h2> <!-- {{ adminEmail }} can be added -->
          </div>
        </div>

        <!-- Action Buttons Section -->
        <div class="actions-card">
          <div class="actions-background"></div>
          <div class="actions-content">
            <h3 class="section-title">Admin Actions</h3>
            <div class="actions-buttons">
              <v-btn
                class="action-btn"
                prepend-icon="mdi-tournament"
                @click="openAddTournamentDialog"
              >
                Add Tournament
              </v-btn>
              <v-btn
                class="action-btn"
                prepend-icon="mdi-account-group"
                @click="openAddTeamDialog"
              >
                Add Team
              </v-btn>
              <v-btn
                class="action-btn"
                prepend-icon="mdi-account-edit"
                @click="openUpdatePlayerDialog"
              >
                Update Player
              </v-btn>
            </div>

            <!-- Display Error for Admin Actions -->
            <div v-if="actionsError" class="error-message">
              {{ actionsError }}
            </div>
          </div>
        </div>

        <!-- Requests Management Section -->
        <div class="history-card">
          <div class="history-background"></div>
          <div class="history-content">
            <h3 class="section-title">Manage Requests</h3>

            <!-- Filter Options -->
            <div class="filter-options">
              <v-select
                v-model="filterStatus"
                :items="statusOptions"
                label="Filter by Status"
                class="filter-select"
                dense
                :style="{ background: 'transparent', color: '#ffffff', borderColor: '#42DDF2FF' }"
              ></v-select>
              <v-btn
                class="filter-btn"
                @click="fetchRequests"
                :loading="isLoading"
              >
                Apply Filter
              </v-btn>
            </div>

            <!-- Loading state -->
            <div
              v-if="isLoading"
              class="d-flex justify-center align-center"
              style="height: 200px"
            >
              <v-progress-circular indeterminate color="#42DDF2FF"></v-progress-circular>
            </div>

            <!-- Error state -->
            <div v-else-if="requestHistoryError" class="error-message">
              {{ requestHistoryError }}
            </div>

            <!-- Request list -->
            <div v-else-if="requests.length > 0" class="request-list">
              <div
                v-for="request in requests"
                :key="request.id"
                class="request-item"
              >
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
                    <v-icon
                      icon="mdi-calendar"
                      size="small"
                      class="detail-icon"
                    ></v-icon>
                    {{ formatDate(request.request_date) }}
                  </div>
                  <div class="detail-item">
                    <v-icon
                      icon="mdi-email"
                      size="small"
                      class="detail-icon"
                    ></v-icon>
                    User Email: {{ request.email }}
                  </div>
                  <div v-if="request.username" class="detail-item">
                    <v-icon
                      icon="mdi-account"
                      size="small"
                      class="detail-icon"
                    ></v-icon>
                    Player: {{ request.username }}
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="request-actions">
                  <v-btn
                    class="approve-btn"
                    @click="approveRequest(request.id)"
                    :disabled="request.status !== 'pending'"
                  >
                    Approve
                  </v-btn>
                  <v-btn
                    class="reject-btn"
                    @click="rejectRequest(request.id)"
                    :disabled="request.status !== 'pending'"
                  >
                    Reject
                  </v-btn>
                </div>
              </div>
            </div>

            <!-- Empty state -->
            <div v-else class="error-message">
              No requests found.
            </div>
          </div>
        </div>

        <!-- Create Tournament Dialog -->
        <v-dialog v-model="showAddTournamentDialog" max-width="500">
          <v-card class="dialog-card">
            <div class="dialog-content">
              <v-card-title class="dialog-title">
                <span>{{ currentStep === 1 ? 'Tournament Details' : 'Select Teams' }}</span>
              </v-card-title>

              <v-card-text>
                <!-- Error Alert -->
                <v-alert
                  v-if="tournamentError"
                  type="error"
                  variant="tonal"
                  closable
                  class="mb-4"
                >
                  {{ tournamentError }}
                </v-alert>

                <!-- Step 1: Tournament Details -->
                <v-form v-if="currentStep === 1" ref="form">
                  <!-- Title Field -->
                  <v-text-field
                    v-model="tournamentTitle"
                    label="Tournament Title"
                    variant="outlined"
                    :rules="[rules.required, rules.minLength]"
                  ></v-text-field>

                  <!-- Format Selection -->
                  <v-select
                    v-model="tournamentFormat"
                    :items="formattedFormatOptions"
                    label="Tournament Format"
                    variant="outlined"
                    :rules="[rules.required]"
                    class="format-select"
                  ></v-select>

                  <!-- Date Selection -->
                  <v-text-field
                    v-model="tournamentStartDate"
                    label="Start Date"
                    type="datetime-local"
                    variant="outlined"
                    :rules="[rules.required]"
                  ></v-text-field>

                  <!-- Prize Pool -->
                  <v-text-field
                    v-model="tournamentPrizePool"
                    label="Prize Pool (Kitty Kibbles)"
                    variant="outlined"
                    type="number"
                    :rules="[rules.required, rules.minPrize]"
                  ></v-text-field>
                </v-form>

                <!-- Step 2: Team Selection -->
                <v-form v-else ref="teamForm">
                  <div class="team-slot" v-for="index in getMaxTeams" :key="index">
                    <div class="d-flex gap-2 align-center">
                      <!-- Normal autocomplete for existing teams -->
                      <v-autocomplete
                        v-if="!isCustomTeam[index - 1]"
                        v-model="selectedTeams[index - 1]"
                        :items="getAvailableTeamsForSlot(index - 1)"
                        item-title="name"
                        item-value="id"
                        :label="`Team ${index}`"
                        variant="outlined"
                        :loading="loadingTeams"
                        clearable
                        class="custom-autocomplete"
                        :rules="getTeamRules(index - 1)"
                      >
                        <template v-slot:item="{ props, item }">
                          <v-list-item
                            v-bind="props"
                            :title="item.raw.name"
                            class="team-list-item"
                          ></v-list-item>
                        </template>
                      </v-autocomplete>

                      <!-- Custom team input -->
                      <v-text-field
                        v-else
                        v-model="customTeamNames[index - 1]"
                        :label="`Custom Team ${index}`"
                        variant="outlined"
                        :rules="getTeamRules(index - 1)"
                      ></v-text-field>

                      <!-- Toggle button -->
                      <v-btn
                        icon
                        class="custom-toggle-btn"
                        @click="toggleCustomTeam(index - 1)"
                        :title="isCustomTeam[index - 1] ? 'Switch to existing teams' : 'Add custom team'"
                        variant="outlined"
                      >
                        <v-icon size="20">
                          {{ isCustomTeam[index - 1] ? 'mdi-format-list-bulleted' : 'mdi-plus' }}
                        </v-icon>
                      </v-btn>
                    </div>
                  </div>
                </v-form>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn class="cancel-btn" @click="handleCancel">
                  Cancel
                </v-btn>
                <v-btn
                  v-if="currentStep === 1"
                  class="next-btn"
                  @click="handleNext"
                  :disabled="!canProceedToTeams"
                >
                  Next
                </v-btn>
                <v-btn
                  v-else
                  class="submit-btn"
                  @click="submitTournament"
                  :loading="isSubmitting"
                  :disabled="!canSubmit"
                >
                  Create Tournament
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-dialog>

        <!-- Add Team Dialog -->
        <v-dialog v-model="showAddTeamDialog" max-width="500">
          <v-card class="dialog-card">
            <div class="dialog-content">
              <v-card-title class="dialog-title">
                <span>Add New Team</span>
              </v-card-title>
              <v-card-text>
                <v-text-field
                  v-model="teamName"
                  label="Team Name"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>

                <v-file-input
                  v-model="teamLogo"
                  label="Team Logo"
                  variant="outlined"
                  accept="image/*"
                  prepend-icon="mdi-camera"
                  :show-size="true"
                  class="mt-4"
                  :rules="[]"
                >
                  <template v-slot:selection="{ fileNames }">
                    <template v-for="fileName in fileNames" :key="fileName">
                      {{ fileName }}
                    </template>
                  </template>
                </v-file-input>

                <div v-if="teamError" class="error-message">
                  {{ teamError }}
                </div>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn class="cancel-btn" @click="showAddTeamDialog = false">
                  Cancel
                </v-btn>
                <v-btn
                  class="submit-btn"
                  @click="submitAddTeam"
                  :loading="isSubmitting"
                >
                  Create Team
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-dialog>

        <!-- Update Player Dialog -->
        <v-dialog v-model="showUpdatePlayerDialog" max-width="500">
          <v-card class="dialog-card">
            <div class="dialog-content">
              <v-card-title class="dialog-title">
                <span>Update Player</span>
              </v-card-title>
              <v-card-text>
                <!-- Username Check Step -->
                <div v-if="!selectedPlayer">
                  <v-text-field
                    v-model="playerUsername"
                    label="Player Username"
                    variant="outlined"
                    :rules="[rules.required]"
                  ></v-text-field>
                  <v-btn
                    class="check-player-btn mt-4 action-btn"
                    block
                    @click="checkPlayer"
                    :loading="isCheckingPlayer"
                  >
                    Next
                  </v-btn>
                </div>

                <!-- Player Update Form -->
                <div v-else>
                  <div class="player-status mb-4 text-center">
                    <v-chip
                      :color="selectedPlayer.user_email ? 'error' : 'success'"
                      class="status-chip"
                    >
                      {{ selectedPlayer.user_email ? 'Linked to User' : 'Available for Update' }}
                    </v-chip>
                  </div>

                  <template v-if="!selectedPlayer.user_email">
                    <div class="avatar-section mb-4">
                      <v-avatar size="64" class="mr-4">
                        <v-img
                          v-if="previewAvatar || selectedPlayer.avatar"
                          :src="previewAvatar || selectedPlayer.avatar"
                          alt="Player avatar"
                        ></v-img>
                        <v-icon
                          v-else
                          icon="mdi-account"
                          color="#42DDF2FF"
                          size="32"
                        ></v-icon>
                      </v-avatar>

                      <v-file-input
                        v-model="playerAvatar"
                        label="Player Avatar (Optional)"
                        variant="outlined"
                        accept="image/*"
                        prepend-icon="mdi-camera"
                        :show-size="true"
                        class="mt-4"
                        :rules="[]"
                        @change="onAvatarChange"
                      ></v-file-input>
                    </div>
                    <v-text-field
                      v-model="playerUsername"
                      label="Username"
                      variant="outlined"
                    ></v-text-field>

                    <v-text-field
                      v-model="playerFirstName"
                      label="First Name"
                      variant="outlined"
                    ></v-text-field>

                    <v-text-field
                      v-model="playerLastName"
                      label="Last Name"
                      variant="outlined"
                    ></v-text-field>

                    <v-text-field
                      v-model="playerCountry"
                      label="Country"
                      variant="outlined"
                    ></v-text-field>

                    <v-autocomplete
                      v-model="selectedTeam"
                      :items="teams"
                      item-title="name"
                      item-value="id"
                      :model-value="selectedPlayer?.team_name"
                      label="Team"
                      variant="outlined"
                      :loading="loadingTeams"
                      :filter="teamFilter"
                      clearable
                      class="custom-autocomplete"
                    ></v-autocomplete>
                  </template>
                  <div v-else class="text-center mt-4">
                    This player is linked to a user and cannot be updated.
                  </div>
                </div>

                <div v-if="playerError" class="error-message">
                  {{ playerError }}
                </div>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  class="cancel-btn"
                  @click="closeUpdatePlayerDialog"
                >
                  Cancel
                </v-btn>
                <v-btn
                  v-if="selectedPlayer && !selectedPlayer.user_email"
                  class="submit-btn"
                  @click="submitUpdatePlayer"
                  :loading="isSubmitting"
                >
                  Update Player
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-dialog>

        <!-- Success Snackbar -->
        <v-snackbar v-model="showSuccessAlert" color="success" timeout="3000">
          {{ successMessage }}
        </v-snackbar>
      </v-container>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref,computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { format } from 'date-fns';
import { API_URL } from '@/config';


const authStore = useAuthStore();

// Props and Emits
const props = defineProps({
  showDialog: Boolean,
  isSubmitting: Boolean
})
const emit = defineEmits(['update:showDialog', 'submit', 'cancel'])
// Data
interface Request {
  id: string;
  email: string;
  request_type: string;
  status: string;
  request_date: string;
  response_date: string | null;
  admin_id: string | null;
  username: string | null;
}

interface Player {
  id: string
  username: string
  first_name: string
  last_name: string
  country: string
  user_email: string | null
  avatar: string | null
}

const requests = ref<Request[]>([])
const isLoading = ref(true)
const requestHistoryError = ref<string | null>(null)
const actionsError = ref<string | null>(null)
const showSuccessAlert = ref(false)
const successMessage = ref('')
const currentStep = ref(1)
const form = ref(null)
const teamForm = ref(null)

// Add Tournament consts
const tournamentTitle = ref('')
const tournamentFormat = ref('')
const tournamentStartDate = ref('')
const tournamentPrizePool = ref('')
const selectedTeams = ref<Array<string | null>>(Array(8).fill(null))
const loadingTeams = ref(false)
const isSubmitting = ref(false)
const tournamentError = ref('')
const teams = ref([])
const customInputs = ref(Array(8).fill(''))
const isCustomTeam = ref(Array(8).fill(false))
const customTeamNames = ref(Array(8).fill(''))


const formattedFormatOptions = [
  { title: 'Single Elimination', value: 'single elimination' },
  { title: 'Round Robin', value: 'round robin' },
  { title: 'One-Off Match', value: 'one off match' }
]

const rules = {
  required: (v: string) => !!v || 'This field is required',
  minLength: (v: string) => v.length >= 3 || 'Title must be at least 3 characters',
  minPrize: (v: number) => v >= 1 || 'Prize pool must be at least 1 Kitty Kibble'
}

// Filter Options
const filterStatus = ref('');
const statusOptions = ['All', 'Pending', 'Accepted', 'Rejected'];

// Dialog visibility
const showAddTournamentDialog = ref(false)

// Form data and errors
const tournamentName = ref('')

// Player dialog state
const showUpdatePlayerDialog = ref(false)
const playerUsername = ref('')
const playerError = ref('')
const isCheckingPlayer = ref(false)
const selectedPlayer = ref<Player | null>(null)
const playerFirstName = ref('')
const playerLastName = ref('')
const playerCountry = ref('')
const playerAvatar = ref<File | null>(null)
const previewAvatar = ref<string | null>(null)
const selectedTeam = ref<string>('')

const tournamentTeams = ref('')

const showAddTeamDialog = ref(false)
const teamName = ref('')
const teamError = ref('')
const teamLogo = ref<File | null>(null)


// Computed

// Add Tournament

const getMaxTeams = computed(() => {
  const formatTeamCounts = {
    'single elimination': 8,
    'round robin': 5,
    'one off match': 2
  }
  return formatTeamCounts[tournamentFormat.value] || 0
})

const canProceedToTeams = computed(() => {
  return tournamentTitle.value.length >= 3 &&
         tournamentFormat.value &&
         tournamentStartDate.value &&
         tournamentPrizePool.value >= 1
})

const canSubmit = computed(() => {
  const requiredTeams = {
    'single elimination': 4,
    'round robin': 4,
    'one off match': 2
  }

  const validTeamsCount = selectedTeams.value.reduce((count, team, index) => {
    if (isCustomTeam.value[index]) {
      return customTeamNames.value[index]?.trim() ? count + 1 : count
    } else {
      return team ? count + 1 : count
    }
  }, 0)

  return validTeamsCount >= requiredTeams[tournamentFormat.value]
})

const handleNext = async () => {
  if (!form.value) return
  const { valid } = await form.value.validate()
  if (!valid) return

  // Fetch teams if not already loaded
  if (teams.value.length === 0) {
    try {
      loadingTeams.value = true
      const response = await fetch(`${API_URL}/teams`)
      if (!response.ok) throw new Error('Failed to load teams')
      const data = await response.json()
      teams.value = data
    } catch (e) {
      console.error('Error fetching teams:', e)
      tournamentError.value = 'Failed to load teams. Please try again.'
      return
    } finally {
      loadingTeams.value = false
    }
  }

  currentStep.value = 2
}

const teamFilter = (item: any, query: string) => {
  if (!query) return true
  const teamName = item.name.toLowerCase()
  const searchTerm = query.toLowerCase()
  return teamName.includes(searchTerm)
}

const getTeamRules = (index: number) => {
  if (tournamentFormat.value === 'single elimination') {
    return index < 4 ? [rules.required] : []
  } else if (tournamentFormat.value === 'round robin') {
    return index < 4 ? [rules.required] : []
  } else if (tournamentFormat.value === 'one off match') {
    return index < 2 ? [rules.required] : []
  }

  return []
}

const getAvailableTeamsForSlot = (currentIndex: number) => {
  return teams.value.filter(team => {
    return !selectedTeams.value.some(
      (selectedId, index) => selectedId === team.id && index !== currentIndex
    )
  })
}

const handleCancel = () => {
  showAddTournamentDialog.value = false
  resetForm()
}

const resetForm = () => {
  currentStep.value = 1
  tournamentTitle.value = ''
  tournamentFormat.value = ''
  tournamentStartDate.value = ''
  tournamentPrizePool.value = ''
  selectedTeams.value = Array(8).fill(null)
  customInputs.value = Array(8).fill('')
  isCustomTeam.value = Array(8).fill(false)
  customTeamNames.value = Array(8).fill('')
  tournamentError.value = ''
}

const submitTournament = async () => {
  if (!teamForm.value) return
  const { valid } = await teamForm.value.validate()
  if (!valid) return

  try {
    isSubmitting.value = true
    tournamentError.value = ''

    const formattedDate = new Date(tournamentStartDate.value).toISOString()

    const teamNames = selectedTeams.value.map((selectedTeam, index) => {
      if (isCustomTeam.value[index]) {
        return customTeamNames.value[index]
      }
      const existingTeam = teams.value.find(t => t.id === selectedTeam)
      return existingTeam?.name || ''
    }).filter(name => name !== '')

    console.log('Team names to send:', teamNames)

    const params = new URLSearchParams({
      title: tournamentTitle.value,
      tournament_format: tournamentFormat.value,
      start_date: formattedDate,
      prize_pool: tournamentPrizePool.value.toString()
    })

    const response = await fetch(`${API_URL}/tournaments/?${params.toString()}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(teamNames)
    })

    console.log('Full URL:', `${API_URL}/tournaments/?${params.toString()}`)
    console.log('Team names in body:', teamNames)

    if (!response.ok) {
      const errorData = await response.json()
      console.log('Full error response:', errorData)

      if (errorData.detail && Array.isArray(errorData.detail)) {
        const errorMessages = errorData.detail.map((err: any) => {
          console.log('Individual error:', err)
          return `${err.msg} (${err.loc.join('.')})`
        })
        throw new Error(errorMessages.join('\n'))
      } else {
        throw new Error('Unknown error occurred')
      }
    }

    showAddTournamentDialog.value = false
    successMessage.value = 'Tournament created successfully!'
    showSuccessAlert.value = true
    resetForm()

  } catch (e) {
    console.error('Full error:', e)
    tournamentError.value = e.message
  } finally {
    isSubmitting.value = false
  }
}

const toggleCustomTeam = (index: number) => {
  isCustomTeam.value[index] = !isCustomTeam.value[index]
  if (!isCustomTeam.value[index]) {
    customTeamNames.value[index] = ''
  } else {
    selectedTeams.value[index] = null
  }
}

// Add Teams

const formatRequestType = (type: string): string => {
  return type
    .split(' ')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

const formatStatus = (status: string): string => {
  return status.charAt(0).toUpperCase() + status.slice(1);
};

const formatDate = (date: string): string => {
  return format(new Date(date), 'dd MMM yyyy, HH:mm');
};

const getRequestTypeIcon = (type: string): string => {
  if (type === 'promote user to director') return 'mdi-shield-account';
  if (type === 'link user to player') return 'mdi-account-plus';
  return 'mdi-help';
};

const onAvatarChange = (file: File | null) => {
  if (file) {
    previewAvatar.value = URL.createObjectURL(file)
  } else {
    previewAvatar.value = null
  }
}


const fetchTeams = async () => {
  try {
    const response = await fetch(`${API_URL}/teams`)
    const data = await response.json()
    teams.value = data
  } catch (e) {
    console.error('Error fetching teams:', e)
  }
}

const fetchRequests = async () => {
  try {
    isLoading.value = true;
    requestHistoryError.value = null;

    const statusQuery = filterStatus.value && filterStatus.value !== 'All' ? `&status=${filterStatus.value.toLowerCase()}` : '';

    const response = await fetch(`${API_URL}/requests?offset=0&limit=50${statusQuery}`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'No requests found.');
    }

    const data = await response.json();

    requests.value = [...data];
  } catch (e) {
    console.error('Error fetching requests:', e);
    requestHistoryError.value =
      e.message || 'Failed to load request history. Please try again later.';
  } finally {
    isLoading.value = false;
  }
};

const approveRequest = async (requestId: string) => {
  try {
    isSubmitting.value = true;

    const response = await fetch(`${API_URL}/requests/${requestId}?status=accepted`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to approve request');
    }

    successMessage.value = 'Request approved successfully.';
    showSuccessAlert.value = true;
    fetchRequests();
  } catch (e) {
    console.error('Error approving request:', e);
    actionsError.value = 'Failed to approve request. Please try again.';
  } finally {
    isSubmitting.value = false;
  }
};

const rejectRequest = async (requestId: string) => {
  try {
    isSubmitting.value = true;


    const response = await fetch(`${API_URL}/requests/${requestId}?status=rejected`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('API Error:', errorData);
      throw new Error(errorData.detail?.[0]?.msg || 'Failed to reject request');
    }

    successMessage.value = 'Request rejected successfully.';
    showSuccessAlert.value = true;
    fetchRequests();
  } catch (e) {
    console.error('Error rejecting request:', e);
    actionsError.value = e.message || 'Failed to reject request. Please try again.';
  } finally {
    isSubmitting.value = false;
  }
};

const openAddTournamentDialog = () => {
  tournamentName.value = '';
  tournamentError.value = null;
  showAddTournamentDialog.value = true;
};

const submitAddTeam = async () => {
  if (!teamName.value) {
    teamError.value = 'Team name is required';
    return;
  }
  console.log('Team name:', teamName.value);
  try {
    isSubmitting.value = true;
    teamError.value = '';

    const formData = new FormData();
    if (teamLogo.value && teamLogo.value.size > 0) {
      formData.append('logo', teamLogo.value);
    }

    const params = new URLSearchParams({
      name: teamName.value,
    })

    const response = await fetch(`${API_URL}/teams/?${params.toString()}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      },
      body: formData
    })

    const data = await response.json();

    if (!response.ok) {
      console.error('Response not OK:', data);
      if (data.detail) {
        if (Array.isArray(data.detail)) {
          teamError.value = data.detail[0].msg;
        } else {
          teamError.value = data.detail;
        }
      } else {
        teamError.value = 'Failed to create team';
      }
      return;
    }

    showAddTeamDialog.value = false;
    successMessage.value = 'Team added successfully!';
    showSuccessAlert.value = true;
    teamName.value = '';
    teamLogo.value = null;
  } catch (e) {
    console.error('Error creating team:', e);
    teamError.value = e instanceof Error ? e.message : 'Unknown error occured';
  } finally {
    isSubmitting.value = false;
  }
};

const openAddTeamDialog = () => {
  teamName.value = ''
  teamLogo.value = null
  teamError.value = ''
  showAddTeamDialog.value = true
}

// Player methods
const openUpdatePlayerDialog = async () => {
  playerUsername.value = ''
  playerError.value = ''
  selectedPlayer.value = null
  playerFirstName.value = ''
  playerLastName.value = ''
  playerCountry.value = ''
  playerAvatar.value = null
  selectedTeam.value = ''
  showUpdatePlayerDialog.value = true

  await fetchTeams()
}

const checkPlayer = async () => {
  if (!playerUsername.value) {
    playerError.value = 'Username is required'
    return
  }

  try {
    isCheckingPlayer.value = true
    playerError.value = ''

    const response = await fetch(`${API_URL}/players?search=${encodeURIComponent(playerUsername.value)}`)
    const players = await response.json()

    if (!players || players.length === 0) {
      playerError.value = 'Player not found'
      return
    }

    selectedPlayer.value = players[0]

    // Pre-fill form if player exists and is not linked
    if (!selectedPlayer.value.user_email) {
      playerFirstName.value = selectedPlayer.value.first_name || ''
      playerLastName.value = selectedPlayer.value.last_name || ''
      playerCountry.value = selectedPlayer.value.country || ''
      selectedTeam.value = selectedPlayer.value.team_id || ''

      if (selectedPlayer.value.team_id) {
        selectedTeam.value = selectedPlayer.value.team_id
      }
      if (selectedPlayer.value.team_name) {
        const currentTeam = teams.value.find(t => t.name === selectedPlayer.value.team_name)
      if (currentTeam) {
        selectedTeam.value = currentTeam.id
      }
    }

      // Load teams if not loaded yet
      if (teams.value.length === 0) {
        await fetchTeams()
      }
    }

  } catch (e) {
    console.error('Error checking player:', e)
    playerError.value = 'Failed to check player'
  } finally {
    isCheckingPlayer.value = false
  }
}

const submitUpdatePlayer = async () => {
  if (!selectedPlayer.value) {
    playerError.value = 'No player selected'
    return
  }

  if (selectedPlayer.value.user_email) {
    playerError.value = 'Cannot update player linked to user'
    return
  }

  try {
    isSubmitting.value = true
    playerError.value = ''

    const params = new URLSearchParams({
      username: playerUsername.value,
      first_name: playerFirstName.value,
      last_name: playerLastName.value,
      country: playerCountry.value,
      team_name: teamName.value
  })

    const formData = new FormData();
    if (playerAvatar.value && playerAvatar.value.size > 0) {
      formData.append('avatar', playerAvatar.value);
    }

    const response = await fetch(`${API_URL}/players/${selectedPlayer.value.id}?${params.toString()}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      },
      body: formData
    })

    console.log('Response status:', response.status)
    const data = await response.json()
    console.log('Response data:', data)

    if (!response.ok) {
      if (data.detail) {
        if (Array.isArray(data.detail)) {
          playerError.value = data.detail[0].msg
        } else {
          playerError.value = data.detail
        }
      } else {
        playerError.value = 'Failed to update player'
      }
      return
    }

    showUpdatePlayerDialog.value = false
    successMessage.value = 'Player updated successfully!'
    showSuccessAlert.value = true

    closeUpdatePlayerDialog()

  } catch (e) {
    console.error('Error updating player:', e)
    playerError.value = 'Failed to connect to server. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}
const closeUpdatePlayerDialog = () => {
  showUpdatePlayerDialog.value = false
  playerUsername.value = ''
  playerError.value = ''
  selectedPlayer.value = null
  playerFirstName.value = ''
  playerLastName.value = ''
  playerCountry.value = ''
  playerAvatar.value = null
  selectedTeam.value = ''
  if (previewAvatar.value) {
    URL.revokeObjectURL(previewAvatar.value)
  }
  previewAvatar.value = null
}



onMounted(() => {
  fetchRequests();
});
</script>

<style scoped>
:deep(.v-select) {
  background: transparent !important;
}

:deep(.v-text-field),
:deep(.v-select) {
  margin-bottom: 16px;
}

:deep(.filter-select) {
  background: transparent !important;
  color: #ffffff !important;
  border-color: #42DDF2FF !important;
}

:deep(.v-select:focus),
:deep(.v-select--active) {
  background: transparent !important;
  border-color: #42DDF2FF !important;
}

:deep(.v-menu__content) {
  background: transparent !important;
  box-shadow: none !important;
}

:deep(.v-list-item) {
  background: transparent !important;
  color: #ffffff !important;
}

:deep(.v-list-item:hover) {
  background: rgba(66, 221, 242, 0.2) !important;
  color: #42DDF2FF !important;
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

:deep(.v-field--error input::placeholder),
:deep(.v-field--error .v-label.v-field-label) {
  color: #fed854 !important;
}
:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}
:deep(.v-field__outline) {
  color: rgba(66, 221, 242, 0.3) !important;
}
.format-select :deep(.v-select__selection) {
  color: white !important;
}

:deep(.v-file-input .v-field) {
  border-color: rgba(66, 221, 242, 0.3) !important;
}

:deep(.v-file-input .v-field:hover) {
  border-color: #42ddf2 !important;
}

:deep(.v-file-input .v-field.v-field--focused) {
  border-color: #42ddf2 !important;
}

:deep(.v-file-input .v-field__input) {
  color: white !important;
  font-size: 0.9rem;
}

:deep(.v-file-input .v-field__append-inner) {
  color: rgba(255, 255, 255, 0.7) !important;
}
:deep(.v-file-input .v-field__input) {
  color: white !important;
  font-size: 0.9rem;
}

:deep(.v-file-input .v-field__append-inner) {
  color: rgba(255, 255, 255, 0.7) !important;
}

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
  padding-top: 200px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100vw !important;
  margin-bottom: 100px;
}

.welcome-card,
.actions-card,
.history-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
  margin-bottom: 24px;
  padding: 24px;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
}

.welcome-content,
.actions-content,
.history-content {
  position: relative;
  z-index: 2;
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
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}

.action-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  font-weight: bold;
  padding: 20px 32px !important;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: #FED854FF !important;
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.3);
}

.filter-options {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  justify-content: center;
}

.filter-select {
  width: 200px;
}

.filter-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
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

.avatar-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar-section .v-avatar {
  border: 2px solid #42DDF2FF;
  background: rgba(8, 87, 144, 0.1);
}

.avatar-section .v-file-input {
  flex: 1;
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
  flex-wrap: wrap;
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

.request-actions {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}

.approve-btn {
  background: rgba(0, 255, 157, 0.1);
  color: #00ff9d;
  border: 1px solid rgba(0, 255, 157, 0.3);
}

.reject-btn {
  background: rgba(255, 99, 99, 0.1);
  color: #ff6363;
  border: 1px solid rgba(255, 99, 99, 0.3);
}

.reject-btn:disabled {
  opacity: 0.3;
  background-color: rgba(255, 99, 99, 0.1);
  color: #ff6363;
  border: 1px solid rgba(255, 99, 99, 0.3);
}

.approve-btn:disabled {
  opacity: 0.3;
  background: rgba(0, 255, 157, 0.1);
  color: #00ff9d;
  border: 1px solid rgba(0, 255, 157, 0.3);
}

.dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
}

.dialog-content {
  padding: 24px;
}

.dialog-title {
  color: #42ddf2 !important;
  font-weight: bold;
  font-size: 1.25rem;
  text-align: center;
  margin-bottom: 16px;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 14px;
}

:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

.error-message {
  color: #fed854;
  font-size: 0.9rem;
  margin-top: 8px;
  text-align: center;
}

.cancel-btn {
  color: #42DDF2FF !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  margin-left: 16px;
}

.team-slot {
  width: 100%;
}

.team-slot .v-autocomplete,
.team-slot .v-text-field {
  flex: 1;
}


.team-list-item {
  transition: background-color 0.2s;
}

.team-list-item:hover {
  background: rgba(66, 221, 242, 0.1);
}

.next-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  margin-left: 16px;
}


:deep(.v-text-field) {
  margin-top: 16px;
}

:deep(.v-field__input input) {
  color: white !important;
  -webkit-text-fill-color: white !important;
}

:deep(.v-field__input input::selection) {
  background-color: rgba(66, 221, 242, 0.3) !important;
  color: white !important;
}

:deep(.v-field__input input::-moz-selection) {
  background-color: rgba(66, 221, 242, 0.3) !important;
  color: white !important;
}

:deep(.v-overlay__content) {
  scrollbar-width: thin;
  scrollbar-color: rgba(66, 221, 242, 0.5) transparent;
}

:deep(.v-overlay__content::-webkit-scrollbar) {
  width: 8px;
}

:deep(.v-overlay__content::-webkit-scrollbar-track) {
  background: transparent;
}

:deep(.v-overlay__content::-webkit-scrollbar-thumb) {
  background-color: rgba(66, 221, 242, 0.5);
  border-radius: 4px;
}

:deep(.v-overlay__content::-webkit-scrollbar-thumb:hover) {
  background-color: rgba(66, 221, 242, 0.7);
}

.custom-autocomplete :deep(.v-field__input) {
  color: rgb(255, 255, 255) !important;
}

.custom-autocomplete :deep(.v-field--focused) {
  color: #42DDF2FF !important;
}

.custom-toggle-btn {
  color: #42DDF2FF !important;
  height: 40px !important;
  width: 40px !important;
  border: 2px solid rgba(66, 221, 242, 0.3) !important;
  margin-left: 8px !important;
  align-self: center;
  transition: all 0.3s ease;
}

.custom-toggle-btn:hover {
  border-color: #42DDF2FF !important;
  background: rgba(66, 221, 242, 0.1) !important;
  transform: scale(1.05);
}
</style>
