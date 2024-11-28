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
                prepend-icon="mdi-soccer"
                @click="openAddMatchDialog"
              >
                Add Match
              </v-btn>
              <v-btn
                class="action-btn"
                prepend-icon="mdi-account-plus"
                @click="openAddPlayerDialog"
              >
                Add Player
              </v-btn>
              <v-btn
                class="action-btn"
                prepend-icon="mdi-account-group"
                @click="openAssignPlayerDialog"
              >
                Assign Player to Team
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

        <!-- Dialogs -->
        <!-- Add Tournament Dialog -->
        <v-dialog v-model="showAddTournamentDialog" max-width="500">
          <v-card class="dialog-card">
            <div class="dialog-content">
              <v-card-title class="dialog-title">
                <span>Add Tournament</span>
              </v-card-title>
              <v-card-text>
                <v-text-field
                  v-model="tournamentTitle"
                  label="Tournament Title"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>

                <!-- Add fields for teams, start date, format, and prize pool -->
                <v-text-field
                  v-model="tournamentTeams"
                  label="Teams (comma-separated)"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>

                <v-text-field
                  v-model="tournamentStartDate"
                  label="Start Date"
                  variant="outlined"
                  type="date"
                  :rules="[rules.required]"
                ></v-text-field>

                <v-select
                  v-model="tournamentFormat"
                  :items="tournamentFormats"
                  label="Tournament Format"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-select>

                <v-text-field
                  v-model="tournamentPrizePool"
                  label="Prize Pool"
                  variant="outlined"
                  type="number"
                ></v-text-field>

                <!-- Display Error -->
                <div v-if="tournamentError" class="error-message">
                  {{ tournamentError }}
                </div>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn class="cancel-btn" @click="showAddTournamentDialog = false">
                  Cancel
                </v-btn>
                <v-btn
                  class="submit-btn"
                  @click="submitAddTournament"
                  :loading="isSubmitting"
                >
                  Submit
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-dialog>

        <!-- Add Match Dialog -->
        <v-dialog v-model="showAddMatchDialog" max-width="500">
          <v-card class="dialog-card">
            <div class="dialog-content">
              <v-card-title class="dialog-title">
                <span>Add Match</span>
              </v-card-title>
              <v-card-text>
                <!-- Match details inputs -->
                <v-text-field
                  v-model="matchDetails"
                  label="Match Details"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>
                <!-- Display Error -->
                <div v-if="matchError" class="error-message">
                  {{ matchError }}
                </div>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn class="cancel-btn" @click="showAddMatchDialog = false">
                  Cancel
                </v-btn>
                <v-btn
                  class="submit-btn"
                  @click="submitAddMatch"
                  :loading="isSubmitting"
                >
                  Submit
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-dialog>

        <!-- Add Player Dialog -->
        <v-dialog v-model="showAddPlayerDialog" max-width="500">
          <v-card class="dialog-card">
            <div class="dialog-content">
              <v-card-title class="dialog-title">
                <span>Add Player</span>
              </v-card-title>
              <v-card-text>
                <v-text-field
                  v-model="playerName"
                  label="Player Name"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>
                <!-- Display Error -->
                <div v-if="playerError" class="error-message">
                  {{ playerError }}
                </div>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn class="cancel-btn" @click="showAddPlayerDialog = false">
                  Cancel
                </v-btn>
                <v-btn
                  class="submit-btn"
                  @click="submitAddPlayer"
                  :loading="isSubmitting"
                >
                  Submit
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-dialog>

        <!-- Assign Player to Team Dialog -->
        <v-dialog v-model="showAddTournamentDialog" max-width="500">
          <v-card class="dialog-card">
            <div class="dialog-content">
              <v-card-title class="dialog-title">
                <span>Add Tournament</span>
              </v-card-title>
              <v-card-text>
                <v-text-field
                  v-model="tournamentTitle"
                  label="Tournament Title"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>

                <!-- Add fields for teams, start date, format, and prize pool -->
                <v-text-field
                  v-model="tournamentTeams"
                  label="Teams (comma-separated)"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>

                <v-text-field
                  v-model="tournamentStartDate"
                  label="Start Date"
                  variant="outlined"
                  type="date"
                  :rules="[rules.required]"
                ></v-text-field>

                <v-select
                  v-model="tournamentFormat"
                  :items="tournamentFormats"
                  label="Tournament Format"
                  item-text="label"
                  item-value="value"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-select>

                <v-text-field
                  v-model="tournamentPrizePool"
                  label="Prize Pool"
                  variant="outlined"
                  type="number"
                ></v-text-field>

                <!-- Display Error -->
                <div v-if="tournamentError" class="error-message">
                  {{ tournamentError }}
                </div>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn class="cancel-btn" @click="showAddTournamentDialog = false">
                  Cancel
                </v-btn>
                <v-btn
                  class="submit-btn"
                  @click="submitAddTournament"
                  :loading="isSubmitting"
                >
                  Submit
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
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { format } from 'date-fns';
import { API_URL } from '@/config';

const authStore = useAuthStore();
const adminEmail = ref(authStore.userEmail);

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

const requests = ref<Request[]>([]);
const isLoading = ref(true);
const requestHistoryError = ref<string | null>(null);
const actionsError = ref<string | null>(null);
const isSubmitting = ref(false);
const showSuccessAlert = ref(false);
const successMessage = ref('');

// Filter Options
const filterStatus = ref('');
const statusOptions = ['All', 'Pending', 'Accepted', 'Rejected'];

// Dialog visibility
const showAddTournamentDialog = ref(false);
const showAddMatchDialog = ref(false);
const showAddPlayerDialog = ref(false);
const showAssignPlayerDialog = ref(false);
const startDateMenu = ref(false);

// Form data and errors
const tournamentName = ref('');
const matchDetails = ref('');
const playerName = ref('');
const assignPlayerName = ref('');
const assignTeamName = ref('');

const tournamentError = ref<string | null>(null);
const matchError = ref<string | null>(null);
const playerError = ref<string | null>(null);
const assignError = ref<string | null>(null);

const tournamentTitle = ref('');
const tournamentTeams = ref('');
const tournamentStartDate = ref('');
const tournamentFormat = ['single elimination', 'round robin', 'one off match']
const tournamentPrizePool = ref(0);

const rules = {
  required: (v: string) => !!v || 'This field is required',
};

// Methods
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

// Tournament Formats
const tournamentFormats = [
  { label: 'Single Elimination', value: 'single elimination' },
  { label: 'Round Robin', value: 'round robin' },
  { label: 'One Off Match', value: 'one off match' },
];

const submitAddTournament = async () => {
  // Reset error message
  tournamentError.value = '';

  // Validate required fields
  if (!tournamentTitle.value) {
    tournamentError.value = 'Tournament title is required.';
    return;
  }

  if (!tournamentTeams.value || tournamentTeams.value.split(',').length < 2) {
    tournamentError.value = 'At least two teams are required.';
    return;
  }

  if (!tournamentStartDate.value) {
    tournamentError.value = 'Tournament start date is required.';
    return;
  }

  if (!tournamentFormat.value) {
    tournamentError.value = 'Tournament format is required.';
    return;
  }

  try {
    isSubmitting.value = true;

    // Prepare the data
    const teamNames = tournamentTeams.value.split(',').map((team) => team.trim());

    // Build the request body
    const requestBody = {
      title: tournamentTitle.value,
      team_names: teamNames,
      start_date: tournamentStartDate.value,
      tournament_format: tournamentFormat.value || tournamentFormat.value, // Use .value if tournamentFormat is a ref
      prize_pool: Number(tournamentPrizePool.value) || 0,
    };

    // Make the POST request
    const response = await fetch(`${API_URL}/tournaments`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    // Check if the response is successful
    if (!response.ok) {
      const errorData = await response.json();
      // Handle validation errors from backend
      if (Array.isArray(errorData.detail)) {
        const errorMessages = errorData.detail
          .map((err) => {
            const field = err.loc[err.loc.length - 1];
            const message = err.msg;
            return `${field}: ${message}`;
          })
          .join(', ');
        throw new Error(errorMessages || 'Failed to add tournament');
      } else {
        throw new Error(errorData.detail || 'Failed to add tournament');
      }
    }

    // Success case: Update UI state
    showAddTournamentDialog.value = false;
    successMessage.value = 'Tournament added successfully.';
    showSuccessAlert.value = true;

    // Reset form fields
    tournamentTitle.value = '';
    tournamentTeams.value = '';
    tournamentStartDate.value = '';
    tournamentFormat.value = '';
    tournamentPrizePool.value = 0;

  } catch (e) {
    // Handle errors
    console.error('Error adding tournament:', e);
    tournamentError.value = e.message || 'Failed to add tournament. Please try again.';
  } finally {
    // Always reset submitting state
    isSubmitting.value = false;
  }
};

const openAddMatchDialog = () => {
  matchDetails.value = '';
  matchError.value = null;
  showAddMatchDialog.value = true;
};

const submitAddMatch = async () => {
  if (!matchDetails.value) {
    matchError.value = 'Match details are required.';
    return;
  }

  try {
    isSubmitting.value = true;

    const response = await fetch(`${API_URL}/matches`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ details: matchDetails.value }),
    });

    if (!response.ok) throw new Error('Failed to add match');

    showAddMatchDialog.value = false;
    successMessage.value = 'Match added successfully.';
    showSuccessAlert.value = true;
  } catch (e) {
    console.error('Error adding match:', e);
    matchError.value = 'Failed to add match. Please try again.';
  } finally {
    isSubmitting.value = false;
  }
};

const openAddPlayerDialog = () => {
  playerName.value = '';
  playerError.value = null;
  showAddPlayerDialog.value = true;
};

const submitAddPlayer = async () => {
  if (!playerName.value) {
    playerError.value = 'Player name is required.';
    return;
  }

  try {
    isSubmitting.value = true;

    const response = await fetch(`${API_URL}/players`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: playerName.value }),
    });

    if (!response.ok) throw new Error('Failed to add player');

    showAddPlayerDialog.value = false;
    successMessage.value = 'Player added successfully.';
    showSuccessAlert.value = true;
  } catch (e) {
    console.error('Error adding player:', e);
    playerError.value = 'Failed to add player. Please try again.';
  } finally {
    isSubmitting.value = false;
  }
};

const openAssignPlayerDialog = () => {
  assignPlayerName.value = '';
  assignTeamName.value = '';
  assignError.value = null;
  showAssignPlayerDialog.value = true;
};

const submitAssignPlayer = async () => {
  if (!assignPlayerName.value || !assignTeamName.value) {
    assignError.value = 'Both player name and team name are required.';
    return;
  }

  try {
    isSubmitting.value = true;

    const response = await fetch(`${API_URL}/teams/assign-player`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        playerName: assignPlayerName.value,
        teamName: assignTeamName.value,
      }),
    });

    if (!response.ok) throw new Error('Failed to assign player to team');

    showAssignPlayerDialog.value = false;
    successMessage.value = 'Player assigned to team successfully.';
    showSuccessAlert.value = true;
  } catch (e) {
    console.error('Error assigning player to team:', e);
    assignError.value = 'Failed to assign player. Please try again.';
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(() => {
  fetchRequests();
});
</script>

<style scoped>
/* Transparent dropdown styles */
:deep(.v-select) {
  background: transparent !important; /* Transparent background for the dropdown */
}

:deep(.filter-select) {
  background: transparent !important;
  color: #ffffff !important;
  border-color: #42DDF2FF !important;
}

:deep(.v-select:focus),
:deep(.v-select--active) {
  background: transparent !important; /* Transparent when focused or active */
  border-color: #42DDF2FF !important; /* Optional: Add a border to highlight focus */
}

:deep(.v-menu__content) {
  background: transparent !important; /* Transparent menu background */
  box-shadow: none !important; /* Remove shadow */
}

:deep(.v-list-item) {
  background: transparent !important; /* Transparent menu items */
  color: #ffffff !important; /* Ensure text remains readable */
}

:deep(.v-list-item:hover) {
  background: rgba(66, 221, 242, 0.2) !important; /* Optional: Light highlight on hover */
  color: #42DDF2FF !important; /* Accent color for hover text */
}
/* Same styles as the user dashboard, plus any additional styles needed */

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
  background: #00ff9d !important;
  color: #171c26 !important;
}

.reject-btn {
  background: #ff6363 !important;
  color: #171c26 !important;
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
  color: #42ddf2;
  font-weight: bold;
  font-size: 1.25rem;
  text-align: center;
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

:deep(.v-text-field) {
  margin-top: 16px;
}
</style>
