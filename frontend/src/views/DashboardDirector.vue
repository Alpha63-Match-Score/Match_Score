<template>
  <div class="dashboard-wrapper">
    <HeaderSection />

    <div class="content-wrapper">
      <v-container>
        <!-- Director Welcome Section -->
        <DashboardWelcome :userRole="'Director'" />

        <!-- Action Buttons Section -->
        <AdminActions
          :openAddTournamentDialog="openAddTournamentDialog"
          :openAddTeamDialog="openAddTeamDialog"
          :openAddPlayerDialog="openAddPlayerDialog"
          :openUpdatePlayerDialog="openUpdatePlayerDialog"
          @open-tournament="openAddTournamentDialog"
          @open-team="openAddTeamDialog"
          @open-player="openAddPlayerDialog"
          @open-update-player="openUpdatePlayerDialog"
        />

        <!-- Filter section -->
        <FilterBar @filter-change="handleFiltersChange"/>

        <!-- Tournaments Content -->
        <div class="tournaments-section">
          <!-- Loading state -->
          <div v-if="isLoadingTournaments" class="d-flex justify-center align-center" style="height: 200px">
            <v-progress-circular indeterminate color="#00ff9d"></v-progress-circular>
          </div>

          <!-- Error state -->
          <div v-else-if="tournamentsError" class="error-text pa-4">
            {{ tournamentsError }}
          </div>

          <!-- Empty state -->
          <div v-else-if="!tournaments.length" class="empty-state">
            <v-icon icon="mdi-tournament" size="64" color="#42DDF2FF" class="mb-4"></v-icon>
            <div class="empty-text">No tournaments created yet</div>
            <div class="empty-subtext">Get started by clicking the "Add Tournament" button</div>
          </div>

          <!-- Tournament Cards Grid -->
          <v-row v-else>
            <v-col v-for="tournament in tournaments"
               :key="tournament.id"
               cols="12"
               md="6"
               class="tournament-column">
              <TournamentCard :tournament="tournament" />
            </v-col>
          </v-row>

          <!-- Load More Button -->
          <LoadMoreButton
            v-if="!isLoadingTournaments && hasMoreTournaments"
            :is-loading="isLoadingMore"
            @load-more="loadMoreTournaments"
          />
        </div>

        <!-- Dialogs -->
        <AddTournamentDialog
          v-model="showAddTournamentDialog"
          @tournament-added="handleTournamentAdded"
        />
        <AddTeamDialog
          v-model="showAddTeamDialog"
          @team-added="handleTeamAdded"
        />
        <AddPlayerDialog
          v-model="showAddPlayerDialog"
          @player-added="handlePlayerAdded"
        />
        <UpdatePlayerDialog
          v-model="showUpdatePlayerDialog"
          @player-updated="handlePlayerUpdated"
        />

        <!-- Success Snackbar -->
        <v-snackbar v-model="showSuccessAlert" color="success" timeout="3000">
          {{ successMessage }}
        </v-snackbar>
      </v-container>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { format } from 'date-fns'
import { API_URL } from '@/config'
import DashboardWelcome from "@/components/DashboardWelcome.vue";
import AdminActions from "@/components/AdminActions.vue";
import FilterBar from "@/components/TournamentFilterBar.vue";
import TournamentCard from "@/components/TournamentCard.vue";
import AddTournamentDialog from "@/components/dialogs/AddTournamentDialog.vue";
import AddTeamDialog from "@/components/dialogs/AddTeamDialog.vue";
import UpdatePlayerDialog from "@/components/dialogs/UpdatePlayerDialog.vue";
import AddPlayerDialog from "@/components/dialogs/AddPlayerDialog.vue";
import type { Tournament, Request, Player, FilterValues } from '@/types/types'
import LoadMoreButton from "@/components/LoadMoreButton.vue";
import HeaderSection from "@/components/HeaderSection.vue";

// Props and Emits
const props = defineProps({
  showDialog: Boolean,
  isSubmitting: Boolean
})
const emit = defineEmits(['update:showDialog', 'submit', 'cancel'])



const authStore = useAuthStore()
const tournaments = ref<Tournament[]>([])
const tournamentsError = ref<string | null>(null)
const showSuccessAlert = ref(false)
const successMessage = ref('')
const selectedPeriod = ref('all')
const selectedStatus = ref('all')
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
const currentStep = ref(1)
const form = ref(null)
const teamForm = ref(null)
const currentLimit = ref(10);

const usernameError = ref('')
const firstNameError = ref('')
const lastNameError = ref('')
const countryError = ref('')

const clearErrors = () => {
  usernameError.value = ''
  firstNameError.value = ''
  lastNameError.value = ''
  countryError.value = ''
}

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
const titleElement = ref(null)
const showTooltip = ref(false)
const isTitleTruncated = ref(false)


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

const checkTitleTruncation = () => {
  if (titleElement.value) {
    const element = titleElement.value
    return element.scrollWidth > element.offsetWidth
  }
  return false
}

const handleTeamAdded = () => {
  showSuccessAlert.value = true
  successMessage.value = 'Team added successfully!'
}

const handleTournamentAdded = async () => {
  await fetchTeamsForTournament()
  showSuccessAlert.value = true
  successMessage.value = 'Tournament created successfully!'
}

const handlePlayerAdded = async (newPlayer: Player) => {
  await fetchTeamsForPlayers()
  showSuccessAlert.value = true
  successMessage.value = `Player ${newPlayer.username} was successfully added!`
}

const handlePlayerUpdated = async (updatedPlayer: Player) => {
  await fetchTeamsForPlayers()
  showSuccessAlert.value = true
  successMessage.value = `Player ${updatedPlayer.username} was successfully updated!`
}

onMounted(() => {
  checkTitleTruncation()
  window.addEventListener('resize', checkTitleTruncation)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkTitleTruncation)
})

const resetTeamForm = () => {
  teamName.value = '';
  teamLogo.value = null;
  previewLogo.value = null;
  teamError.value = '';
};



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

const isFiltered = ref(false);
const isLoadingTournaments = ref(false);
const hasMoreTournaments = ref(true);
const isLoadingMore = ref(false);
const selectedFormat = ref<string | null>(null);

const handleFiltersChange = async (filters: FilterValues) => {
  try {
    isLoadingTournaments.value = true;
    tournamentsError.value = null;
    currentLimit.value = 10;

    const params = new URLSearchParams();
    params.append('offset', '0');
    params.append('limit', currentLimit.value.toString());

    if (filters.period) {
      params.append('period', filters.period);
    }

    if (filters.status) {
      params.append('status', filters.status);
    }

    if (filters.format) {
      params.append('tournament_format', filters.format);
    }

    const response = await fetch(`${API_URL}/tournaments/?${params}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    const results = Array.isArray(data) ? data : data.results || [];
    tournaments.value = results;

    isFiltered.value = !!(selectedPeriod.value || selectedStatus.value || selectedFormat.value);
    hasMoreTournaments.value = results.length === currentLimit.value;

  } catch (e) {
    console.error('Error fetching tournaments:', e);
    tournamentsError.value = 'Failed to load tournaments. Please try again later.';
  } finally {
    isLoadingTournaments.value = false;
  }
};

const fetchTournaments = async (loadMore = false) => {
  try {
    if (loadMore) {
      isLoadingMore.value = true;
    } else {
      isLoadingTournaments.value = true;
      isFiltered.value = false; // Reset filter state when loading initial tournaments
    }
    tournamentsError.value = null;

    const response = await fetch(`${API_URL}/tournaments/?offset=0&limit=${currentLimit.value}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    const results = Array.isArray(data) ? data : (data.results || []);

    tournaments.value = results;
    hasMoreTournaments.value = results.length === currentLimit.value;

  } catch (e) {
    console.error('Error fetching tournaments:', e);
    tournamentsError.value = 'Failed to load tournaments. Please try again later.';
  } finally {
    isLoadingTournaments.value = false;
    isLoadingMore.value = false;
  }
};

const loadMoreTournaments = async () => {
  currentLimit.value += 10;
  await fetchTournaments(true);
};

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

const fetchTeamsForTournament = async () => {
  try {
    loadingTeams.value = true;
    const response = await fetch(`${API_URL}/teams?has_space=true`);

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

const openAddTournamentDialog = () => {
  tournamentName.value = '';
  tournamentError.value = null;
  showAddTournamentDialog.value = true;
  fetchTeamsForTournament();
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



const initializeTeam = () => {
  if (selectedPlayer.value?.team_id) {
    selectedTeam.value = selectedPlayer.value.team_id;
  } else {
    selectedTeam.value = '';
  }
}

onMounted(() => {
  initializeTeam()
  fetchTournaments()
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
  width: 100vw !important;
}


.tournaments-section {
  width: 85%;
  max-width: 1400px;
  margin: 8px auto 0;
}

.tournament-column {
  padding: 8px;
}


.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px;
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(2px);
}

.empty-text {
  color: #42DDF2FF;
  font-size: 1.5rem;
  text-align: center;
  margin-bottom: 8px;
}

.empty-subtext {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
  text-align: center;
}
</style>
