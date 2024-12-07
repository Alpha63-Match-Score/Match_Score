<template>
  <div class="dashboard-wrapper">
    <HeaderSection />

    <div class="content-wrapper">
      <v-container>
        <!-- Admin Welcome Section -->
        <DashboardWelcome :userRole="'Admin'" />

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


        <!-- Requests Management Section -->
        <AdminRequestManagement />

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
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { API_URL } from '@/config';
import HeaderSection from "@/components/HeaderSection.vue";
import AdminActions from "@/components/AdminActions.vue";
import DashboardWelcome from "@/components/DashboardWelcome.vue";
import AdminRequestManagement from "@/components/AdminRequestManagement.vue";
import AddTournamentDialog from "@/components/dialogs/AddTournamentDialog.vue";
import AddTeamDialog from "@/components/dialogs/AddTeamDialog.vue";
import UpdatePlayerDialog from "@/components/dialogs/UpdatePlayerDialog.vue";
import AddPlayerDialog from "@/components/dialogs/AddPlayerDialog.vue";
import type { Request, Player } from "@/types/types";


const authStore = useAuthStore();

const requests = ref<Request[]>([])
const isLoading = ref(true)
const requestHistoryError = ref<string | null>(null)
const showSuccessAlert = ref(false)
const successMessage = ref('')
const tournamentError = ref('')
const filterStatus = ref('');
const playerUsername = ref('')
const playerError = ref('')
const selectedPlayer = ref<Player | null>(null)
const playerFirstName = ref('')
const playerLastName = ref('')
const playerCountry = ref('')
const playerAvatar = ref<File | null>(null)
const previewAvatar = ref<string | null>(null)
const selectedTeam = ref<string>('')

const showAddTournamentDialog = ref(false)
const tournamentName = ref('')
const showUpdatePlayerDialog = ref(false)


const showAddTeamDialog = ref(false)
const teamName = ref('')
const teamError = ref('')
const teamLogo = ref<File | null>(null)


const showAddPlayerDialog = ref(false)
const usernameError = ref('')
const firstNameError = ref('')
const lastNameError = ref('')
const countryError = ref('')


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

const clearErrors = () => {
  usernameError.value = ''
  firstNameError.value = ''
  lastNameError.value = ''
  countryError.value = ''
}

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

const openAddTournamentDialog = () => {
  tournamentName.value = '';
  tournamentError.value = null;
  showAddTournamentDialog.value = true;
};

const openAddTeamDialog = () => {
  teamName.value = ''
  teamLogo.value = null
  teamError.value = ''
  showAddTeamDialog.value = true
}

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

  if (selectedPlayer.value && selectedPlayer.value.team_id) {
    selectedTeam.value = selectedPlayer.value.team_id;
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
  fetchRequests()
})
</script>

<style scoped>
.dashboard-wrapper {
  min-height: 100vh;
  position: relative;
}

:deep(.v-select) {
  background: transparent !important;
}

:deep(.v-text-field),
:deep(.v-select) {
  margin-bottom: 16px;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
  display: block !important;
}

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

.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 100px;
  flex-direction: column;
  gap: 20px;
  width: 100vw;
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
</style>
