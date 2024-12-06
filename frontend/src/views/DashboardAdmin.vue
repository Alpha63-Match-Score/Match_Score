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
            <div class="actions-grid">
              <div class="actions-row">
                <v-btn class="action-btn" prepend-icon="mdi-tournament" @click="openAddTournamentDialog">
                  Add Tournament
                </v-btn>
                <v-btn class="action-btn" prepend-icon="mdi-account-group" @click="openAddTeamDialog">
                  Add Team
                </v-btn>
              </div>
              <div class="actions-row">
                <v-btn class="action-btn" prepend-icon="mdi-account" @click="openAddPlayerDialog">
                  Add Player
                </v-btn>
                <v-btn class="action-btn" prepend-icon="mdi-account-edit" @click="openUpdatePlayerDialog">
                  Update Player
                </v-btn>
              </div>
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

            <!-- Filter Options -->
            <div class="filter-options">
              <v-select
                v-model="filterStatus"
                :items="statusOptions"
                item-title="text"
                item-value="value"
                variant="outlined"
                density="comfortable"
                label="Filter by Status"
                bg-color="rgba(45, 55, 75, 0.8)"
                color="#ffffff"
                menu-icon="mdi-chevron-down"
                @update:model-value="fetchRequests"
              ></v-select>
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
                    Player:
                    <span
                      class="request-player-link"
                      @click="handlePlayerClick(request.username)"
                    >
                      {{ request.username }}
                    </span>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="request-actions">
                  <v-btn
                    class="approve-btn"
                    @click="approveRequest(request.id)"
                    :loading="isApprovingRequest[request.id]"
                    :disabled="request.status !== 'pending' || isApprovingRequest[request.id] || isRejectingRequest[request.id]"
                  >
                    Approve
                  </v-btn>
                  <v-btn
                    class="reject-btn"
                    @click="rejectRequest(request.id)"
                    :loading="isRejectingRequest[request.id]"
                    :disabled="request.status !== 'pending' || isApprovingRequest[request.id] || isRejectingRequest[request.id]"
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
                    :error-messages="titleError"
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
                    :error-messages="dateError"
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
                    <div class="d-flex align-center">
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
                        class="flex-grow-1 custom-autocomplete"
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
                        class="flex-grow-1"
                        :rules="getTeamRules(index - 1)"
                      ></v-text-field>

                      <!-- Toggle button -->
                      <v-btn
                        icon
                        class="custom-toggle-btn ml-2"
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

        <!-- Update Player Dialog -->
        <v-dialog v-model="showUpdatePlayerDialog" max-width="450">
          <v-card class="dialog-card">
            <div class="dialog-content">
              <v-card-title class="dialog-title">
                <span>Update Player</span>
              </v-card-title>

              <v-card-text>
                <!-- Username Check Step -->
                <div v-if="!selectedPlayer" class="input-wrapper">
                  <v-text-field
                    v-model="playerUsername"
                    label="Player Username"
                    variant="outlined"
                    :rules="[rules.required]"
                    :error-messages="playerError"
                    @keyup.enter="checkPlayer"
                    @input="playerError = ''"
                  ></v-text-field>
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
                    <div class="file-upload-section">
                      <v-avatar size="120" class="preview-avatar">
                        <v-img
                          v-if="previewAvatar || selectedPlayer.avatar"
                          :src="previewAvatar || selectedPlayer.avatar"
                          alt="Player avatar"
                        ></v-img>
                        <v-icon
                          v-else
                          icon="mdi-account"
                          color="#42DDF2FF"
                          size="48"
                        ></v-icon>
                      </v-avatar>

                      <v-file-input
                        v-model="playerAvatar"
                        label="Player Avatar (Optional)"
                        variant="outlined"
                        accept="image/*"
                        prepend-icon="mdi-camera"
                        :show-size="true"
                        class="upload-input"
                        @change="onAvatarChange"
                        hide-details
                      ></v-file-input>
                    </div>

                    <v-text-field
                      v-model="playerUsername"
                      label="Username"
                      variant="outlined"
                      :rules="rules.username"
                      :error-messages="usernameError"
                      @input="clearErrors"
                    ></v-text-field>

                    <v-text-field
                      v-model="playerFirstName"
                      label="First Name"
                      variant="outlined"
                      :rules="rules.firstName"
                      :error-messages="firstNameError"
                      @input="clearErrors"
                    ></v-text-field>

                    <v-text-field
                      v-model="playerLastName"
                      label="Last Name"
                      variant="outlined"
                      :rules="rules.lastName"
                      :error-messages="lastNameError"
                      @input="clearErrors"
                    ></v-text-field>

                    <v-text-field
                      v-model="playerCountry"
                      label="Country"
                      variant="outlined"
                      :rules="rules.country"
                      :error-messages="countryError"
                      @input="clearErrors"
                    ></v-text-field>

                    <v-autocomplete
                      v-model="selectedTeam"
                      :items="teams"
                      item-title="name"
                      item-value="name"
                      label="Team"
                      variant="outlined"
                      :loading="loadingTeams"
                      clearable
                      :menu-props="{ contentClass: 'teams-menu' }"
                      :return-object="false"
                      :model-value="selectedTeam"
                      @update:model-value="handleTeamChange"
                    >
                      <template v-slot:item="{ props, item }">
                        <v-list-item
                          v-bind="props"
                          :title="item.raw.name"
                          class="team-list-item"
                        >
                        </v-list-item>
                      </template>
                    </v-autocomplete>
                  </template>

                  <div v-else class="text-center mt-4">
                    This player is linked to a user and cannot be updated.
                  </div>
                </div>
              </v-card-text>

              <v-card-actions class="dialog-actions">
                <v-spacer></v-spacer>
                <v-btn
                  class="cancel-btn"
                  variant="text"
                  @click="closeUpdatePlayerDialog"
                >
                  Cancel
                </v-btn>
                <v-btn
                  v-if="!selectedPlayer"
                  class="next-btn"
                  @click="checkPlayer"
                  :loading="isCheckingPlayer"
                  :disabled="!playerUsername"
                >
                  Next
                </v-btn>
                <v-btn
                  v-if="selectedPlayer && !selectedPlayer.user_email"
                  class="submit-btn"
                  @click="submitUpdatePlayer"
                  :loading="isSubmitting"
                  :disabled="!hasChanges"
                >
                  {{ hasChanges ? 'Update Player' : 'No Changes' }}
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-dialog>

        <!-- Add Player Dialog -->
        <v-dialog v-model="showAddPlayerDialog" max-width="450">
          <v-card class="dialog-card">
            <div class="dialog-content">
              <v-card-title class="dialog-title">
                <span>Add New Player</span>
              </v-card-title>

              <v-card-text>
                <div class="file-upload-section">
                  <v-avatar size="120" class="preview-avatar">
                    <v-img
                      v-if="previewAvatar"
                      :src="previewAvatar"
                      alt="Player avatar"
                    ></v-img>
                    <v-icon
                      v-else
                      icon="mdi-account"
                      color="#42DDF2FF"
                      size="48"
                    ></v-icon>
                  </v-avatar>

                  <v-file-input
                    v-model="playerAvatar"
                    label="Player Avatar (Optional)"
                    variant="outlined"
                    accept="image/*"
                    :show-size="true"
                    prepend-icon="mdi-camera"
                    class="upload-input"
                    @change="onAvatarChange"
                    @click:clear="clearAvatar"
                    hide-details
                  ></v-file-input>
                </div>

                <v-form ref="addPlayerForm" v-model="isFormValid">
                  <v-text-field
                    v-model="addPlayerUsername"
                    label="Username"
                    variant="outlined"
                    :rules="rules.username"
                    :error-messages="addPlayerUsernameError"
                    @input="clearAddPlayerErrors"
                  ></v-text-field>

                  <v-text-field
                    v-model="addPlayerFirstName"
                    label="First Name"
                    variant="outlined"
                    :rules="rules.firstName"
                    :error-messages="addPlayerFirstNameError"
                    @input="clearAddPlayerErrors"
                  ></v-text-field>

                  <v-text-field
                    v-model="addPlayerLastName"
                    label="Last Name"
                    variant="outlined"
                    :rules="rules.lastName"
                    :error-messages="addPlayerLastNameError"
                    @input="clearAddPlayerErrors"
                  ></v-text-field>

                  <v-text-field
                    v-model="addPlayerCountry"
                    label="Country"
                    variant="outlined"
                    :rules="rules.country"
                    :error-messages="addPlayerCountryError"
                    @input="clearAddPlayerErrors"
                  ></v-text-field>
                </v-form>

                <v-autocomplete
                  v-model="selectedTeam"
                  :items="teams"
                  item-title="name"
                  item-value="id"
                  label="Team (Optional)"
                  variant="outlined"
                  :loading="loadingTeams"
                  clearable
                  :menu-props="{ contentClass: 'teams-menu' }"
                  >
                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :title="item.title"
                      class="team-list-item"
                    ></v-list-item>
                  </template>
                ></v-autocomplete>
              </v-card-text>

              <v-card-actions class="dialog-actions">
                <v-spacer></v-spacer>
                <v-btn
                  class="cancel-btn"
                  variant="text"
                  @click="closeAddPlayerDialog"
                >
                  Cancel
                </v-btn>
                <v-btn
                  class="submit-btn"
                  @click="submitAddPlayer"
                  :loading="isSubmitting"
                  :disabled="!canSubmitPlayer"
                >
                  Create Player
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-dialog>


        <!-- Add Team Dialog -->
        <v-dialog v-model="showAddTeamDialog" max-width="450">
          <v-card class="dialog-card">
            <div class="dialog-content">
              <v-card-title class="dialog-title">
                <span>Add New Team</span>
              </v-card-title>

              <v-card-text>
                <div class="file-upload-section">
                  <v-avatar size="120" class="preview-avatar">
                    <v-img
                      v-if="previewLogo"
                      :src="previewLogo"
                      alt="Team logo"
                    ></v-img>
                    <v-icon
                      v-else
                      icon="mdi-shield"
                      color="#42DDF2FF"
                      size="48"
                    ></v-icon>
                  </v-avatar>

                  <v-file-input
                    v-model="teamLogo"
                    label="Team Logo (Optional)"
                    variant="outlined"
                    accept="image/*"
                    :show-size="true"
                    prepend-icon="mdi-camera"
                    class="upload-input"
                    @change="onLogoChange"
                    @click:clear="clearLogo"
                    hide-details
                  ></v-file-input>
                </div>

                <v-text-field
                  v-model="teamName"
                  label="Team Name"
                  variant="outlined"
                  :rules="rules.team"
                  :error-messages="teamError"
                  @input="validateTeamName"
                ></v-text-field>
              </v-card-text>

              <v-card-actions class="dialog-actions">
                <v-spacer></v-spacer>
                <v-btn
                  class="cancel-btn"
                  variant="text"
                  @click="handleCancelTeam"
                >
                  Cancel
                </v-btn>
                <v-btn
                  class="submit-btn"
                  @click="submitAddTeam"
                  :loading="isSubmitting"
                  :disabled="!teamName.trim()"
                >
                  Create Team
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-dialog>

        <!-- Player Modal -->
        <v-dialog v-model="showPlayerModal" max-width="600px" class="request-player-dialog">
          <v-card>
            <v-card-title class="request-dialog-title">
              {{ selectedPlayer?.username }}
            </v-card-title>
            <v-card-text class="request-dialog-content">
              <v-avatar size="150" class="mb-6">
                <v-img v-if="selectedPlayer?.avatar" :src="selectedPlayer.avatar" alt="Player avatar"></v-img>
                <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="100"></v-icon>
              </v-avatar>

              <div class="request-stats-grid">
                <div class="request-stat-item">
                  <div class="request-stat-label">Nickname</div>
                  <div class="request-stat-value">{{ selectedPlayer?.username }}</div>
                </div>

                <div class="request-stat-item">
                  <div class="request-stat-label">Full Name</div>
                  <div class="request-stat-value" style="text-align: right;">{{ selectedPlayer?.first_name }} {{ selectedPlayer?.last_name }}</div>
                </div>

                <div class="request-stat-item">
                  <div class="request-stat-label">Country</div>
                  <div class="request-stat-value">{{ selectedPlayer?.country }}</div>
                </div>

                <div class="request-stat-item">
                  <div class="request-stat-label">Win Ratio</div>
                  <div class="request-stat-value" style="color: #FED854FF;">{{ selectedPlayer?.game_win_ratio }}</div>
                </div>
              </div>
            </v-card-text>
            <v-card-actions>
              <v-btn
                block
                class="request-close-btn"
                @click="showPlayerModal = false"
              >
                Close
              </v-btn>
            </v-card-actions>
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
  team_id: string | null
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
const isApprovingRequest = ref<{ [key: string]: boolean }>({});
const isRejectingRequest = ref<{ [key: string]: boolean }>({});

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
const titleError = ref('')
const dateError = ref('')


const formattedFormatOptions = [
  { title: 'Single Elimination', value: 'single elimination' },
  { title: 'Round Robin', value: 'round robin' },
  { title: 'One-Off Match', value: 'one off match' }
]

const rules = {
  required: (v: string) => !!v || 'This field is required',
  minLength: (v: string) => v.length >= 3 || 'Title must be at least 3 characters',
  minPrize: (v: number) => v >= 1 || 'Prize pool must be at least 1 Kitty Kibble',
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
  team: [
    (v: string) => !!v || 'Team name is required',
    (v: string) => v.length >= 3 || 'Team name must be at least 3 characters',
    (v: string) => v.length <= 50 || 'Team name must not exceed 50 characters',
    (v: string) => /^[a-zA-Z0-9\s-]+$/.test(v) || 'Team name can only contain letters, numbers, spaces and dashes'
  ],
};

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
const previewLogo = ref<string | null>(null)
const teamLogo = ref<File | null>(null)


const canSubmitAddPlayer = computed(() => {
  return addPlayerUsername.value.trim() &&
         addPlayerFirstName.value.trim() &&
         addPlayerLastName.value.trim() &&
         addPlayerCountry.value.trim() &&
         !addPlayerUsernameError.value &&
         !addPlayerFirstNameError.value &&
         !addPlayerLastNameError.value &&
         !addPlayerCountryError.value
})
const showAddPlayerDialog = ref(false)
const addPlayerUsername = ref('')
const addPlayerFirstName = ref('')
const addPlayerLastName = ref('')
const addPlayerCountry = ref('')
const addPlayerAvatar = ref<File | null>(null)
const addPlayerPreviewAvatar = ref<string | null>(null)
const addPlayerSelectedTeam = ref<string>('')
const addPlayerError = ref('')
const addPlayerUsernameError = ref('')
const addPlayerFirstNameError = ref('')
const addPlayerLastNameError = ref('')
const addPlayerCountryError = ref('')
const isFormValid = ref(false);
const addPlayerForm = ref(null)

const showPlayerModal = ref(false)
const selectedModalPlayer = ref(null)
const isLoadingPlayer = ref(false)

const usernameError = ref('')
const firstNameError = ref('')
const lastNameError = ref('')
const countryError = ref('')

// Add Tournament

const clearErrors = () => {
  usernameError.value = ''
  firstNameError.value = ''
  lastNameError.value = ''
  countryError.value = ''
}

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

const clearAddPlayerErrors = () => {
  addPlayerUsernameError.value = ''
  addPlayerFirstNameError.value = ''
  addPlayerLastNameError.value = ''
  addPlayerCountryError.value = ''
}

const canSubmitPlayer = computed(() => {
  return isFormValid.value
})

const clearAddPlayerForm = () => {
  addPlayerUsername.value = '';
  addPlayerFirstName.value = '';
  addPlayerLastName.value = '';
  addPlayerCountry.value = '';
  addPlayerAvatar.value = null;
  addPlayerPreviewAvatar.value = null;
  addPlayerError.value = '';
  addPlayerSelectedTeam.value = '';
};

const handleNext = async () => {
  if (!form.value) return

  titleError.value = ''
  dateError.value = ''
  tournamentError.value = ''
  let hasErrors = false

  try {
    const response = await fetch(`${API_URL}/tournaments?search=${encodeURIComponent(tournamentTitle.value)}`)
    const tournaments = await response.json()
    if (tournaments.some(t => t.title.toLowerCase() === tournamentTitle.value.toLowerCase())) {
      titleError.value = 'A tournament with this name already exists'
      hasErrors = true
    }
  } catch (e) {
    console.error('Error checking tournament title:', e)
  }

  const selectedDate = new Date(tournamentStartDate.value)
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  tomorrow.setHours(selectedDate.getHours(), selectedDate.getMinutes(), selectedDate.getSeconds())
  const now = new Date()

  if (selectedDate < now) {
    dateError.value = 'Tournament start date cannot be in the past'
    hasErrors = true
  } if (selectedDate <= tomorrow) {
    dateError.value = 'Start date must be at least 1 day in the future'
    hasErrors = true
  }
  if (hasErrors) return

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

  const { valid } = await form.value.validate()
  if (!valid) return

  currentStep.value = 2
}

const teamFilter = (item: any, query: string) => {
  if (!query) return true
  const teamName = item.name.toLowerCase()
  const searchTerm = query.toLowerCase()
  return teamName.includes(searchTerm)
}

const resetTeamForm = () => {
  teamName.value = '';
  teamLogo.value = null;
  previewLogo.value = null;
  teamError.value = '';
};

const clearLogo = () => {
  teamLogo.value = null;
  previewLogo.value = null;
};

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
const handleCancelTeam = () => {
  resetTeamForm();
  showAddTeamDialog.value = false;
};

const handleCancel = () => {
  showAddTournamentDialog.value = false
  resetForm()
}

const hasTeamChanges = () => {
  const currentTeamId = selectedPlayer.value?.team_id || null;
  const newTeamId = selectedTeam.value || null;
  return currentTeamId !== newTeamId;
}

const validateTeamName = () => {
  teamError.value = '';
  if (!teamName.value?.trim()) {
    teamError.value = 'Team name is required';
  }
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
  titleError.value = ''
  dateError.value = ''
}

const submitTournament = async () => {
  if (!teamForm.value) return
  const { valid } = await teamForm.value.validate()
  if (!valid) return

  try {
    isSubmitting.value = true
    tournamentError.value = ''

    const formattedDate = new Date(tournamentStartDate.value).toISOString()

    const teamNamesForCheck = selectedTeams.value
      .map((selectedTeam, index) => {
        if (isCustomTeam.value[index]) {
          return null
        }
        const existingTeam = teams.value.find(t => t.id === selectedTeam)
        return existingTeam?.name
      })
      .filter(name => name !== null)

    for (const teamName of teamNamesForCheck) {
      const response = await fetch(`${API_URL}/teams?search=${encodeURIComponent(teamName)}`)
      const teamData = await response.json()
      const team = teamData[0]

      if (team && team.tournament_id) {
        tournamentError.value = `Team "${teamName}" is already participating in another tournament`
        return
      }
    }

    const teamNames = selectedTeams.value.map((selectedTeam, index) => {
      if (isCustomTeam.value[index]) {
        return customTeamNames.value[index]
      }
      const existingTeam = teams.value.find(t => t.id === selectedTeam)
      return existingTeam?.name || ''
    }).filter(name => name !== '')

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

    if (!response.ok) {
      const errorData = await response.json()
      if (errorData.detail && Array.isArray(errorData.detail)) {
        const errorMessages = errorData.detail.map((err: any) => {
          return `${err.msg} (${err.loc.join('.')})`
        })
        throw new Error(errorMessages.join('\n'))
      } else {
        throw new Error(errorData.detail || 'Unknown error occurred')
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

const onAvatarChange = (event: Event | File[] | File) => {
  let file: File | null = null;

  if (Array.isArray(event)) {
    file = event[0];
  } else if (event instanceof File) {
    file = event;
  } else if (event?.target instanceof HTMLInputElement && event.target.files) {
    file = event.target.files[0];
  }

  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewAvatar.value = e.target.result as string;
    };
    reader.readAsDataURL(file);
    playerAvatar.value = file;
  } else {
    previewAvatar.value = null;
    playerAvatar.value = null;
  }
}

const onLogoChange = (event: Event | File[] | File) => {
  let file: File | null = null;

  if (Array.isArray(event)) {
    file = event[0];
  } else if (event instanceof File) {
    file = event;
  } else if (event?.target instanceof HTMLInputElement && event.target.files) {
    file = event.target.files[0];
  }

  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewLogo.value = e.target.result as string;
    };
    reader.readAsDataURL(file);
    teamLogo.value = file;
  } else {
    previewLogo.value = null;
    teamLogo.value = null;
  }
};

const clearAvatar = () => {
  playerAvatar.value = null;
  if (previewAvatar.value) {
    URL.revokeObjectURL(previewAvatar.value);
  }
  previewAvatar.value = null;
};

const submitAddPlayer = async () => {
  const { valid } = await addPlayerForm.value.validate();

  if (!valid) {
    return;
  }

  try {
    isSubmitting.value = true;

    const playerData = {
      username: addPlayerUsername.value,
      first_name: addPlayerFirstName.value,
      last_name: addPlayerLastName.value,
      country: addPlayerCountry.value,
    };

    if (selectedTeam.value) {
      const teamName = teams.value.find(t => t.id === selectedTeam.value)?.name
      if (teamName) {
        playerData.team_name = teamName;
      }
    }

    const params = new URLSearchParams(playerData);
    let url = `${API_URL}/players/?${params.toString()}`;
    let headers = {
      'Authorization': `Bearer ${authStore.token}`
    };
    let body;

    if (playerAvatar.value) {
      const formData = new FormData();
      formData.append('avatar', playerAvatar.value);
      body = formData;
    } else {
      headers['Content-Type'] = 'application/json';
      body = JSON.stringify({ avatar: null });
    }

    const response = await fetch(url, {
      method: "POST",
      headers: headers,
      body: body,
    });

    if (!response.ok) {
      const data = await response.json();
      if (data.detail) {
        if (typeof data.detail === 'string') {
          if (data.detail.includes("username")) {
            addPlayerUsernameError.value = "Player with this username already exists";
          }
          if (data.detail.includes("first_name")) {
            addPlayerFirstNameError.value = "Invalid first name";
          }
          if (data.detail.includes("last_name")) {
            addPlayerLastNameError.value = "Invalid last name";
          }
          if (data.detail.includes("country")) {
            addPlayerCountryError.value = "Invalid country";
          }
        }
      } else {
        throw new Error(data.detail || "Failed to create player");
      }
      return;
    }

    showAddPlayerDialog.value = false;
    successMessage.value = "Player added successfully!";
    showSuccessAlert.value = true;
    clearAddPlayerForm();

  } catch (e) {
    console.error("Error adding player:", e.message);
  } finally {
    isSubmitting.value = false;
  }
};


const openAddPlayerDialog = async () => {
  playerAvatar.value = null;
  if (previewAvatar.value) {
    URL.revokeObjectURL(previewAvatar.value);
  }
  previewAvatar.value = null;
  playerUsername.value = ''
  playerError.value = ''
  playerFirstName.value = ''
  playerLastName.value = ''
  playerCountry.value = ''
  playerAvatar.value = null
  selectedTeam.value = ''
  showAddPlayerDialog.value = true

  // Load teams for the dropdown
  if (teams.value.length === 0) {
    await fetchTeamsForPlayers()
  }
}

const closeAddPlayerDialog = () => {
  showAddPlayerDialog.value = false;
  addPlayerAvatar.value = null;
  previewAvatar.value = null;
  addPlayerUsername.value = '';
  addPlayerFirstName.value = '';
  addPlayerLastName.value = '';
  addPlayerCountry.value = '';
  addPlayerError.value = '';
  addPlayerSelectedTeam.value = '';

  if (previewAvatar.value) {
    URL.revokeObjectURL(previewAvatar.value);
    previewAvatar.value = null;
  }

  if (addPlayerForm.value) {
    addPlayerForm.value.reset();
  }
};

const fetchTeams = async () => {
  try {
    loadingTeams.value = true;
    const response = await fetch(`${API_URL}/teams?is_available=true`);

    if (!response.ok) throw new Error('Failed to fetch teams');
    const data = await response.json();
    teams.value = data;
    console.log('Loaded teams:', teams.value);
  } catch (e) {
    console.error('Error fetching teams:', e);
  } finally {
    loadingTeams.value = false;
  }
};

const handlePlayerClick = async (username: string) => {
  try {
    isLoadingPlayer.value = true
    const response = await fetch(`${API_URL}/players?search=${encodeURIComponent(username)}`)
    if (!response.ok) {
      throw new Error('Failed to fetch player')
    }
    const players = await response.json()
    if (players.length > 0) {
      selectedPlayer.value = players[0]
      showPlayerModal.value = true
    }
  } catch (e) {
    console.error('Error fetching player:', e)
  } finally {
    isLoadingPlayer.value = false
  }
}

const fetchTeamsForPlayers = async () => {
  try {
    loadingTeams.value = true;
    const response = await fetch(`${API_URL}/teams?has_space=true`);
    if (!response.ok) throw new Error('Failed to fetch teams');
    const data = await response.json();
    teams.value = data;
  } catch (e) {
    console.error('Error fetching teams:', e);
  } finally {
    loadingTeams.value = false;
  }
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
    isApprovingRequest.value[requestId] = true;
    isSubmitting.value = true;

    // 1. First approve the selected request
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

    // 2. Get the approved request details
    const approvedRequest = requests.value.find(r => r.id === requestId);

    // 3. If it's a player link request, reject all other pending requests for the same player
    if (approvedRequest && approvedRequest.username) {
      const otherPendingRequests = requests.value.filter(r =>
        r.id !== requestId &&
        r.status === 'pending' &&
        r.username === approvedRequest.username
      );

      // Reject all other pending requests for this player
      for (const request of otherPendingRequests) {
        await fetch(`${API_URL}/requests/${request.id}?status=rejected`, {
          method: 'PUT',
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
      }
    }

    successMessage.value = 'Request approved successfully.';
    showSuccessAlert.value = true;

    // 4. Refresh the requests list
    await fetchRequests();

  } catch (e) {
    console.error('Error approving request:', e);
    actionsError.value = 'Failed to approve request. Please try again.';
  } finally {
    isSubmitting.value = false;
    isApprovingRequest.value[requestId] = false;
  }
};

const rejectRequest = async (requestId: string) => {
  try {
    isRejectingRequest.value[requestId] = true;
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

    isRejectingRequest.value[requestId] = false;

    successMessage.value = 'Request rejected successfully.';
    showSuccessAlert.value = true;
    fetchRequests();
  } catch (e) {
    console.error('Error rejecting request:', e);
    actionsError.value = e.message || 'Failed to reject request. Please try again.';
  } finally {
    isSubmitting.value = false;
    isRejectingRequest.value[requestId] = false;
  }
};

const openAddTournamentDialog = () => {
  tournamentName.value = '';
  tournamentError.value = null;
  showAddTournamentDialog.value = true;
};

const submitAddTeam = async () => {
  try {
    isSubmitting.value = true;
    teamError.value = '';

    if (!teamName.value?.trim()) {
      teamError.value = 'Team name is required';
      return;
    }

    if (teamName.value.length < 3) {
      teamError.value = 'Team name must be at least 3 characters long';
      return;
    }

    const params = new URLSearchParams({
      name: teamName.value.trim()
    });

    let headers = {
      'Authorization': `Bearer ${authStore.token}`
    };

    let body;

    if (teamLogo.value) {
      const formData = new FormData();
      formData.append('logo', teamLogo.value);
      body = formData;
    } else {
      headers['Content-Type'] = 'application/json';
      body = JSON.stringify({ logo: null });
    }

    const response = await fetch(`${API_URL}/teams/?${params.toString()}`, {
      method: 'POST',
      headers: headers,
      body: body
    });

    if (!response.ok) {
      const data = await response.json();
      if (data.detail) {
        if (Array.isArray(data.detail)) {
          teamError.value = data.detail[0].msg || 'Invalid team data';
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
    resetTeamForm();
  } catch (e) {
    console.error('Error creating team:', e);
    teamError.value = 'Failed to connect to server. Please try again.';
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
  clearErrors()
  playerError.value = ''
  usernameError.value = ''
  firstNameError.value = ''
  lastNameError.value = ''
  countryError.value = ''

  playerUsername.value = ''
  playerError.value = ''
  selectedPlayer.value = null
  playerFirstName.value = ''
  playerLastName.value = ''
  playerCountry.value = ''
  playerAvatar.value = null
  selectedTeam.value = ''
  showUpdatePlayerDialog.value = true

  if (teams.value.length === 0) {
    await fetchTeamsForPlayers();
  }

  if (selectedPlayer.value && selectedPlayer.value.team_id) {
    selectedTeam.value = selectedPlayer.value.team_id;
  }
}

const checkPlayer = async () => {
  playerError.value = ''

  if (!playerUsername.value?.trim()) {
    playerError.value = 'Username is required'
    return
  }

  try {
    isCheckingPlayer.value = true
    playerError.value = ''

    const response = await fetch(`${API_URL}/players?search=${encodeURIComponent(playerUsername.value)}`)
    const players = await response.json()

    const exactMatch = players.find(p => p.username.toLowerCase() === playerUsername.value.toLowerCase())

    if (!exactMatch) {
      playerError.value = 'Player not found.'
      return
    }

    selectedPlayer.value = exactMatch

    // Pre-fill form if player exists and is not linked
    if (!selectedPlayer.value.user_email) {
      playerFirstName.value = selectedPlayer.value.first_name || ''
      playerLastName.value = selectedPlayer.value.last_name || ''
      playerCountry.value = selectedPlayer.value.country || ''
      playerUsername.value = selectedPlayer.value.username || ''
      selectedTeam.value = selectedPlayer.value.team_name || ''

      if (selectedPlayer.value.avatar) {
        originalAvatarUrl.value = selectedPlayer.value.avatar
        previewAvatar.value = selectedPlayer.value.avatar
      }

      // Load teams if not loaded yet
      if (teams.value.length === 0) {
        await fetchTeamsForPlayers()
      }
    }

  } catch (e) {
    console.error('Error checking player:', e)
    playerError.value = 'Failed to check player'
  } finally {
    isCheckingPlayer.value = false
  }
}

const handleFieldChange = async (field: string, value: any) => {
  if (!selectedPlayer.value) return

  try {
    playerError.value = ''
    const params = new URLSearchParams()
    params.append(field, value)

    const response = await fetch(
      `${API_URL}/players/${selectedPlayer.value.id}?${params.toString()}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
        }
      }
    )

    if (!response.ok) {
      const data = await response.json()
      handleError(data)
      return
    }

    selectedPlayer.value = {
      ...selectedPlayer.value,
      [field]: value
    }

  } catch (e) {
    console.error(`Error updating ${field}:`, e)
    playerError.value = 'Failed to update player'
  }
}
const handleTeamChange = (newTeam: string | null) => {
  handleFieldChange('team_id', newTeam)
}

const handleUsernameChange = (newUsername: string) => {
  handleFieldChange('username', newUsername)
}

const initializeTeam = () => {
  if (selectedPlayer.value?.team_id) {
    selectedTeam.value = selectedPlayer.value.team_id;
  } else {
    selectedTeam.value = '';
  }
}

onMounted(() => {
  initializeTeam()
})

const submitUpdatePlayer = async () => {
  if (!selectedPlayer.value) {
    playerError.value = 'No player selected'
    return
  }

  try {
    clearErrors()
    isSubmitting.value = true
    playerError.value = ''

    if (playerUsername.value && !rules.username.every(rule => rule(playerUsername.value) === true)) {
      usernameError.value = 'Invalid username format'
      return
    }
    if (playerFirstName.value && !rules.firstName.every(rule => rule(playerFirstName.value) === true)) {
      firstNameError.value = 'Invalid first name format'
      return
    }
    if (playerLastName.value && !rules.lastName.every(rule => rule(playerLastName.value) === true)) {
      lastNameError.value = 'Invalid last name format'
      return
    }
    if (playerCountry.value && !rules.country.every(rule => rule(playerCountry.value) === true)) {
      countryError.value = 'Invalid country format'
      return
    }

    let url = `${API_URL}/players/${selectedPlayer.value.id}`
    const params = new URLSearchParams()

    if (playerUsername.value !== selectedPlayer.value.username) {
      params.append('username', playerUsername.value)
    }
    if (playerFirstName.value !== selectedPlayer.value.first_name) {
      params.append('first_name', playerFirstName.value)
    }
    if (playerLastName.value !== selectedPlayer.value.last_name) {
      params.append('last_name', playerLastName.value)
    }
    if (playerCountry.value !== selectedPlayer.value.country) {
      params.append('country', playerCountry.value)
    }
    if ((selectedPlayer.value.team_id && selectedTeam.value === '') ||
        (selectedTeam.value && selectedTeam.value !== selectedPlayer.value.team_id)) {
      if (selectedTeam.value === '') {
        params.append('team_name', '')
      } else {
        const team = teams.value.find(t => t.id === selectedTeam.value)
        if (team) {
          params.append('team_name', team.name)
        }
      }
    }

    if (params.toString()) {
      url += '?' + params.toString()
    }

    const formData = new FormData()
    if (playerAvatar.value) {
      formData.append('avatar', playerAvatar.value)
    } else {
      formData.append('avatar', '')
    }

    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      },
      body: formData
    })

    if (!response.ok) {
      const data = await response.json()
      if (data.detail && typeof data.detail === 'string') {
        if (data.detail.includes('username')) {
          usernameError.value = data.detail
        } else if (data.detail.includes('first_name')) {
          firstNameError.value = data.detail
        } else if (data.detail.includes('last_name')) {
          lastNameError.value = data.detail
        } else if (data.detail.includes('country')) {
          countryError.value = data.detail
        } else {
          throw new Error(data.detail)
        }
        return
      }
      throw new Error(data.detail || 'Failed to update player')
    }

    const updatedPlayer = await response.json()
    selectedPlayer.value = updatedPlayer

    showUpdatePlayerDialog.value = false
    successMessage.value = 'Player updated successfully!'
    showSuccessAlert.value = true
    closeUpdatePlayerDialog()

  } catch (e) {
    console.error('Error updating player:', e)
    playerError.value = e.message || 'Failed to connect to server. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

const hasChanges = computed(() => {
  if (!selectedPlayer.value) return false;

  const hasPlayerDataChanges =
    playerUsername.value !== selectedPlayer.value.username ||
    playerFirstName.value !== selectedPlayer.value.first_name ||
    playerLastName.value !== selectedPlayer.value.last_name ||
    playerCountry.value !== selectedPlayer.value.country ||
    selectedTeam.value !== selectedPlayer.value.team_id;

  // Check for avatar changes
  const hasAvatarChanges = playerAvatar.value !== null;

  // Check if team was removed (selectedTeam is null but player had a team)
  const hasTeamRemovalChange =
    selectedTeam.value === null &&
    selectedPlayer.value.team_id !== null;

  return hasPlayerDataChanges || hasAvatarChanges || hasTeamRemovalChange;
});

const fetchPlayerByEmail = async (email) => {
  try {
    isLoadingPlayer.value = true;
    playerError.value = null;
    const response = await fetch(`${API_URL}/players?email=${email}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    selectedPlayer.value = await response.json();
    showPlayerModal.value = true;
  } catch (e) {
    console.error('Error fetching player:', e);
    playerError.value = 'Failed to load player details. Please try again later.';
  } finally {
    isLoadingPlayer.value = false;
  }
};


const removeFromTeam = () => {
  selectedTeam.value = '';
};

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
  font-size: 0.85rem;
  line-height: 1.2;
  display: block !important;
}

:deep(.v-input input) {
  color: white !important;
}

/*:deep(.v-field--error) {*/
/*  --v-field-border-color: #fed854 !important;*/
/*}*/

:deep(.v-field--variant-outlined.v-field--error) {
  border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline) {
  color: #fed854 !important;
}
:deep(.v-text-field .v-field--error) {
  --v-field-border-color: #fed854;
}
:deep(.v-messages__message) {
  color: #FED854FF !important;
  margin-bottom: 8px;
}

:deep(.v-field--error .v-label) {
  color: #FED854FF !important;
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
  width: 65%;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
}

.welcome-content,
.actions-content,
.history-content {
  position: relative;
  justify-items: center;
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

.actions-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.actions-row {
  display: flex;
  gap: 16px;
  justify-content: center;
  width: 100%;
}

.action-btn {
  flex: 1;
  min-width: 200px;
  max-width: 300px;
  height: 56px !important;
  background: #42DDF2FF !important;
  color: #171c26 !important;
  font-weight: bold;
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
  gap: 16px;
  width: 400px;
}

.request-list {
  display: grid;
  flex-direction: column;
  gap: 16px;
  width: 100%;
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
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.avatar-section .v-avatar {
  border: 2px solid #42DDF2FF;
  background: rgba(8, 87, 144, 0.1);
}

.logo-preview {
  border: 2px solid #42DDF2FF;
  background: rgba(8, 87, 144, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.logo-preview:hover {
  transform: scale(1.05);
}

.logo-upload {
  width: 100%;
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
  border: 1px solid #42DDF2FF;
  backdrop-filter: blur(10px);
  border-radius: 12px;
}

.dialog-content {
  padding: 20px;
}

.input-wrapper {
  width: 100%;
  max-width: 320px;
  margin: 0 auto;
}

.username-input {
  margin-bottom: 0;
}

.dialog-actions {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: -32px;
}

.dialog-title {
  color: #42ddf2;
  font-size: 1.4rem;
  font-weight: 500;
  text-align: center;
  margin-bottom: 16px;
}
:deep(.v-card-text) {
  padding-bottom: 8px;
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
  margin-bottom: 16px;
}

.team-slot .d-flex {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.toggle-btn {
  height: 56px !important;
  width: 56px !important;
  margin-top: 0 !important;
  color: #42DDF2FF !important;
  border-color: rgba(66, 221, 242, 0.3) !important;
}

.toggle-btn:hover {
  border-color: #42DDF2FF !important;
  background: rgba(66, 221, 242, 0.1) !important;
}

.team-slot .v-autocomplete,
.team-slot .v-text-field {
  flex: 1;
}


.team-list-item {
  padding: 8px 16px;
  transition: background-color 0.2s;
  border-radius: 4px;
  margin: 2px 0;
}

.team-list-item:hover {
  background: rgba(66, 221, 242, 0.1);
}

.team-list-item--selected {
  background: rgba(66, 221, 242, 0.15);
}

:deep(.v-autocomplete .v-field__input) {
  color: white !important;
  min-height: 56px;
}

:deep(.v-autocomplete .v-field__append-inner) {
  padding-top: 14px;
}

:deep(.v-list-item__content) {
  color: white;
}

:deep(.v-list) {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 1px solid rgba(66, 221, 242, 0.3);
}

.next-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
}
:deep(.v-messages) {
  min-height: 14px;
  padding-top: 2px;
  display: block !important;
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
  margin-top: -22px !important;
  height: 48px !important;
  width: 48px !important;
  color: #42DDF2FF !important;
  border: 2px solid rgba(66, 221, 242, 0.3) !important;
  flex-shrink: 0;
}

.custom-toggle-btn:hover {
  border-color: #42DDF2FF !important;
  background: rgba(66, 221, 242, 0.1) !important;
}

.flex-grow-1 {
  flex-grow: 1;
}

:deep(.v-alert) {
  background-color: rgba(254, 216, 84, 0.1) !important;
  color: #FED854FF !important;
  border-color: #FED854FF !important;
}

:deep(.v-alert__close-button) {
  color: #FED854FF !important;
}

:deep(.v-alert__prepend) {
  color: #FED854FF !important;
}

.error-alert {
  color: #FED854FF !important;
  background-color: rgba(254, 216, 84, 0.1) !important;
  border: 1px solid #FED854FF !important;
  border-radius: 4px;
  padding: 12px;
  margin-bottom: 16px;
}

.file-upload-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-bottom: 8px;
}

.preview-avatar {
  border: 2px solid #42DDF2FF;
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s;
}

.preview-avatar:hover {
  transform: scale(1.05);
}

.upload-input {
  width: 100%;
}

.status-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.status-chip {
  font-size: 0.9rem;
}

.form-fields {
  margin-top: 16px;
}

.preview-avatar .v-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

:deep(.v-field__input) {
  color: white !important;
}

:deep(.v-file-input .v-field) {
  border-color: rgba(66, 221, 242, 0.3) !important;
}

:deep(.v-file-input .v-field:hover) {
  border-color: #42ddf2 !important;
}

.dialog-content .v-card-text > div > * {
  margin-top: 0 !important;
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
.clickable-player {
  cursor: pointer;
  color: #42DDF2FF;
  transition: transform 0.2s;
}

.clickable-player:hover {
  transform: scale(1.1);
}

.request-player-link {
  cursor: pointer;
  color: #42DDF2FF;
  transition: transform 0.2s;
  margin-left: 4px;
}

.request-player-link:hover {
  transform: scale(1.1);
}

.request-player-dialog :deep(.v-card) {
  width: 400px;
  margin: 0 auto;
  border-radius: 50px !important;
  background: rgba(45, 55, 75, 0.8) !important;
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF !important;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
}

.request-dialog-title {
  color: #42DDF2FF !important;
  font-size: 1.5rem !important;
  text-align: center;
  padding: 20px !important;
}

.request-dialog-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px;
  gap: 2px;
}

.request-stats-grid {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.request-stat-item {
  background: rgba(30, 40, 55, 0.5);
  border: 1px solid rgba(66, 221, 242, 0.3);
  border-radius: 10px;
  padding: 12px 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
}

.request-stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin-bottom: 0;
  justify-self: start;
}

.request-stat-value {
  color: white;
  font-size: 1.1rem;
  justify-self: end;
}

.request-close-btn {
  background: transparent !important;
  color: #42DDF2FF !important;
  border: 2px solid #42DDF2FF !important;
  border-radius: 50px !important;
  margin: 20px !important;
  padding: 10px 40px !important;
  font-size: 1.1rem !important;
}

.request-close-btn:hover {
  background: rgba(66, 221, 242, 0.1) !important;
}

.request-player-dialog :deep(.v-card-actions) {
  display: flex;
  justify-content: center;
}

.request-player-dialog :deep(.v-card-actions .v-btn) {
  background: rgba(17, 78, 112, 0.56) !important;
  color: #42DDF2FF !important;
  border: 2px solid #42DDF2FF !important;
  min-width: 120px;
  font-weight: bold;
  letter-spacing: 1px;
  transition: all 0.2s;
  margin: 20px auto;
}

.request-player-dialog :deep(.v-card-actions .v-btn:hover) {
  background: rgba(66, 221, 242, 0.1) !important;
  transform: translateY(-2px);
}

.request-close-btn {
  min-width: 120px !important;
  padding: 8px 24px !important;
  border: 2px solid #42DDF2FF !important;
  color: #42DDF2FF !important;
  background: transparent !important;
  border-radius: 50px !important;
  font-size: 0.9rem !important;
  text-transform: none !important;
  transition: all 0.2s !important;
}

.request-close-btn:hover {
  background: rgba(66, 221, 242, 0.1) !important;
}


</style>
