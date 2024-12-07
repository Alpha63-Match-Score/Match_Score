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

const periodOptions = [
  { text: 'All Tournaments', value: 'all' },
  { text: 'Upcoming', value: 'future' },
  { text: 'Current', value: 'present' },
  { text: 'Past', value: 'past' }
]

const statusOptions = [
  { text: 'All Status', value: 'all' },
  { text: 'Active', value: 'active' },
  { text: 'Finished', value: 'finished' }
]

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

const handleTournamentAdded = () => {
  showSuccessAlert.value = true
  successMessage.value = 'Tournament created successfully!'
}

const handlePlayerAdded = (newPlayer: Player) => {
  showSuccessAlert.value = true
  successMessage.value = `Player ${newPlayer.username} was successfully added!`
}

const handlePlayerUpdated = (updatedPlayer: Player) => {
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

const getTournamentBackground = (format: string): string => {
  const formatMap: Record<string, string> = {
    'round robin': roundRobinBg,
    'one off match': oneOffMatchBg,
    'single elimination': singleEliminationBg,
  }
  return formatMap[format] || ''
}

const formatText = (text: string): string => {
  return text.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

const formatDateRange = (startDate: string, endDate: string): string => {
  return `${format(new Date(startDate), 'dd MMM yyyy')} / ${format(new Date(endDate), 'dd MMM yyyy')}`
}

const formatStage = (stage: string): string => {
  if (stage === 'finished') return 'Tournament Completed'
  if (stage === 'final') return 'Finals'
  return stage.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
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

// Placeholder functions for dialog actions
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

// const formatRequestType = (type: string): string => {
//   return type
//     .split(' ')
//     .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
//     .join(' ');
// };
//
// const formatStatus = (status: string): string => {
//   return status.charAt(0).toUpperCase() + status.slice(1);
// };
//
// const formatDate = (date: string): string => {
//   return format(new Date(date), 'dd MMM yyyy, HH:mm');
// };

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
  fetchTournaments()
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
  handleFiltersChange()
})
</script>

<style scoped>
.dashboard-wrapper {
  min-height: 100vh;
  position: relative;
}

.header-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 600px;
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
  height: 600px;
  background: linear-gradient(
    to bottom,
    rgba(23, 28, 38, 0) 0%,
    rgba(23, 28, 38, 0.8) 30%,
    rgba(23, 28, 38, 1) 80%
  );
  z-index: 2;
}

.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 100px;
  min-height: 100vh;
  width: 100vw !important;
}


:deep(.v-field) {
  background: rgba(45, 55, 75, 0.8) !important;
}

:deep(.v-select__selection) {
  color: white !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

.tournament-column {
  padding: 16px;
}

.tournament-card {
  position: relative;
  min-height: 300px;
  height: auto;
  border-radius: 20px;
  overflow: hidden;
  background: rgba(45, 55, 75, 0.8);
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
}

.tournament-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0 20px rgba(8, 117, 176, 0.4);
}

.tournament-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: var(--tournament-bg);
  background-position: center;
  background-size: cover;
  opacity: 0.05;
  z-index: 1;
}

.tournament-content {
  position: relative;
  z-index: 2;
  padding: 24px;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tournament-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  min-height: 100px;
}

.tournament-title {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.5rem;
  margin: 0;
  font-weight: 600;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-word;
  max-width: calc(100% - 120px);
  line-height: 1.3;
}

.title-tooltip {
  visibility: hidden;
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 0;
  background: rgba(45, 55, 75, 0.95);
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 1rem;
  border: 1px solid #42DDF2FF;
  box-shadow: 0 0 10px rgba(8, 87, 144, 0.3);
  min-width: 200px;
  max-width: 300px;
  opacity: 0;
  transition: opacity 0.3s;
}

.tournament-title:hover .title-tooltip {
  visibility: visible;
  opacity: 1;
}

.tournament-title:hover::after {
  content: attr(data-full-title);
  position: absolute;
  left: 0;
  top: 100%;
  background: rgba(45, 55, 75, 0.95);
  padding: 8px;
  border-radius: 4px;
  font-size: 1rem;
  z-index: 1000;
  white-space: normal;
  max-width: 300px;
  border: 1px solid #42DDF2FF;
  display: none;
}

.tournament-title.truncated:hover::after {
  display: block;
}

.format-tag {
  flex-shrink: 0;
  background: rgba(17, 78, 112, 0.56);
  color: #42DDF2FF;
  padding: 6px 16px;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid rgba(8, 87, 144, 0.8);
  cursor: pointer;
}

.format-tag:hover {
  color: #42DDF2FF !important;
  background: rgba(66, 221, 242, 0.1);
}

.tournament-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: auto;
}

.info-section {
  display: flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
}

.info-icon {
  color: rgba(66, 221, 242, 0.8) !important;
}

.view-details-btn {
  margin-top: auto;
  color: #42DDF2FF !important;
  border-color: #42DDF2FF !important;
  border-radius: 50px;
  width: 40%;
  align-self: center;
}

.view-details-btn:hover {
  color: #42DDF2FF !important;
  background: rgba(66, 221, 242, 0.1);
}

.error-text {
  text-align: center;
  color: rgba(255, 255, 255, 0.75);
  padding: 20px;
  background: rgba(255, 215, 0, 0.25);
  border-radius: 10px;
  margin: 20px 0;
}

.empty-message {
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  padding: 32px;
  font-size: 1.1rem;
}

.filter-button-space {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 8px;
  padding-bottom: 4px;
  position: relative;
  z-index: 4;
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

.error-message {
  color: #fed854;
  font-size: 0.9rem;
  margin-top: 8px;
  text-align: center;
}

.dialog-actions {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.cancel-btn {
  color: #42DDF2FF !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  margin-left: 16px;
}

.filters-section {
  width: 65%;
  max-width: 1400px;
  margin: 0 auto 16px;
  display: flex;
  justify-content: center;
}

.filters-wrapper {
  display: flex;
  gap: 16px;
  justify-content: center;
  width: 100%;
  max-width: 500px;
  margin-bottom: -30px;
}

.tournaments-section {
  width: 85%;
  max-width: 1400px;
  margin: 8px auto 0;
}

.tournaments-grid {
  margin: 0;
}

.tournament-column {
  padding: 8px;
}

.show-all-btn {
  background: rgba(45, 55, 75, 0.8);
  color: #ffffff !important;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  margin: 0 auto 16px;
  padding: 8px 24px;
  display: block;
  transition: all 0.2s;
}

.show-all-btn:hover {
  background: rgba(66, 221, 242, 0.1);
  border-color: #42DDF2FF;
}

.error-alert {
  color: #FED854FF !important;
  background-color: rgba(254, 216, 84, 0.1) !important;
  border: 1px solid #FED854FF !important;
  border-radius: 4px;
  padding: 12px;
  margin-bottom: 16px;
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

.title-wrapper {
  position: relative;
  flex: 1;
  max-width: calc(100% - 120px);
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
