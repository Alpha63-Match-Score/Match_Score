<template>
  <div class="team-wrapper">
    <!-- Dynamic header based on team logo -->
    <div
      class="header-image"
      :style="{ backgroundImage: `url(${team?.logo})` }"
    ></div>
    <div class="header-overlay"></div>

    <div class="content-wrapper">
      <v-container v-if="team">
        <!-- Team Header Section -->
        <div class="team-header-card">
            <div class="team-title-section">
              <h1 class="team-title">
                {{ team.name }}
                <div v-if="canEdit" class="edit-controls">
                  <v-icon
                    icon="mdi-pencil"
                    class="edit-icon ml-2"
                    @click="openNameEdit"
                    size="26"
                  ></v-icon>
                  <v-icon
                    icon="mdi-camera"
                    class="edit-icon ml-2"
                    @click="openLogoEdit"
                    size="26"
                  ></v-icon>
                </div>
              </h1>
            </div>

          <!-- Team Players Section -->
          <div class="players-showcase">
            <div class="players-grid">
              <div v-for="player in team.players"
                   :key="player.id"
                   class="player-item"
                   @click="showPlayerInfo(player)">
                <v-avatar size="80" class="player-avatar" @click="handlePlayerClick(player.id)">
                  <v-img v-if="player.avatar" :src="player.avatar" :alt="player.username"></v-img>
                  <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>

                </v-avatar>
                <span class="player-name">{{ player.username }}</span>
              </div>
              <!-- Add Player Button -->
              <div v-if="canEdit" class="player-item add-player" @click="openAddPlayerDialog">
                <v-avatar size="80" class="player-avatar add-avatar">
                  <v-icon icon="mdi-plus" color="#42DDF2FF" size="40"></v-icon>
                </v-avatar>
                <span class="player-name">Add Player</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Team Content Grid -->
        <div class="team-content-wrapper">
          <v-row class="mt-6">
            <!-- Stats Cards Row -->
            <v-col cols="12" md="4">
              <div class="stats-card">
                <h3 class="section-title">
                  <v-icon icon="mdi-trophy" class="mr-2"></v-icon>
                  Match Performance
                </h3>
                <div class="stats-list">
                  <div class="stat-item">
                    <span class="stat-label">Matches Played</span>
                    <span class="stat-value">{{ team.team_stats.matches_played }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Matches Won</span>
                    <span class="stat-value glow-text">{{ team.team_stats.matches_won }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Win/Loss Ratio</span>
                    <span class="stat-value">{{ team.team_stats.match_win_loss_ratio.ratio }}</span>
                  </div>
                </div>
              </div>
            </v-col>

            <v-col cols="12" md="4">
              <div class="stats-card">
                <h3 class="section-title">
                  <v-icon icon="mdi-medal" class="mr-2"></v-icon>
                  Tournament Stats
                </h3>
                <div class="stats-list">
                  <div class="stat-item">
                    <span class="stat-label">Tournaments Played</span>
                    <span class="stat-value">{{ team.team_stats.tournaments_played }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Tournaments Won</span>
                    <span class="stat-value glow-text">{{ team.team_stats.tournaments_won }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Win/Loss Ratio</span>
                    <span class="stat-value">{{ team.team_stats.tournament_win_loss_ratio.ratio }}</span>
                  </div>
                </div>
              </div>
            </v-col>

            <v-col cols="12" md="4">
              <div class="stats-card">
                <h3 class="section-title">
                  <v-icon icon="mdi-sword-cross" class="mr-2"></v-icon>
                  Rival Analysis
                </h3>
                <div class="stats-list">
                  <div class="stat-item">
                    <span class="stat-label">Most Frequent Rival</span>
                    <span class="stat-value">{{ team.team_stats.most_often_played_opponent || 'N/A' }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Strongest Rival</span>
                    <span class="stat-value accent-text">{{ team.team_stats.best_opponent || 'N/A' }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Favorable Matchup</span>
                    <span class="stat-value">{{ team.team_stats.worst_opponent || 'N/A' }}</span>
                  </div>
                </div>
              </div>
            </v-col>
          </v-row>

          <!-- Prizes and Matches Row -->
          <v-row class="mt-6">
            <v-col cols="12" md="6">
              <div class="content-card">
                <h3 class="section-title">
                  <v-icon icon="mdi-cat" class="mr-2"></v-icon>
                  Achievement Showcase
                </h3>
                <div class="prizes-list">
                  <div v-for="prize in team.prize_cuts"
                       :key="prize.id"
                       class="prize-item"
                       :class="{ 'gold': prize.place === 1, 'silver': prize.place === 2 }">
                    <div class="prize-trophy">
                      <v-icon :icon="prize.place === 1 ? 'mdi-trophy' : 'mdi-trophy-variant'"
                             size="32"
                             :color="prize.place === 1 ? '#FED854FF' : '#C0C0C0'">
                      </v-icon>
                    </div>
                    <div class="prize-details">
                      <span class="tournament-name">{{ prize.tournament_name }}</span>
                      <span class="prize-place">{{ formatPlace(prize.place) }} Place</span>
                    </div>
                  </div>
                </div>
              </div>
            </v-col>

            <v-col cols="12" md="6">
              <div class="content-card">
                <h3 class="section-title">
                  <v-icon icon="mdi-sword" class="mr-2"></v-icon>
                  Recent Matches
                </h3>
                <div class="matches-list">
                  <div v-for="match in team.matches"
                       :key="match.id"
                       class="match-item"
                       :class="{ 'match-won': match.winner_id === team.id }">
                    <div class="match-teams">
                      <span class="team1" :class="{ 'winner': match.winner_id === match.team1_id }">
                        {{ match.team1_name }}
                      </span>
                      <span class="vs">vs</span>
                      <span class="team2" :class="{ 'winner': match.winner_id === match.team2_id }">
                        {{ match.team2_name }}
                      </span>
                    </div>
                    <div class="match-info">
                      <span class="tournament-name">{{ match.tournament_title }}</span>
                      <span class="match-stage">{{ match.stage }}</span>
                    </div>
                    <div class="match-result" :class="{ 'won': match.winner_id === team.id }">
                      {{ match.winner_id === team.id ? 'Victory' : 'Defeat' }}
                    </div>
                  </div>
                </div>
              </div>
            </v-col>
          </v-row>
        </div>
      </v-container>

      <!-- Loading State -->
      <div v-else-if="loading" class="loading-container">
        <v-progress-circular indeterminate color="#42DDF2FF"></v-progress-circular>
      </div>
    </div>

    <!-- Player Modal -->
    <v-dialog v-model="showPlayerModal" max-width="400px" class="player-dialog">
      <v-card>
        <v-card-title class="dialog-title">
          {{ selectedPlayer?.username }}
        </v-card-title>
        <v-card-text class="dialog-content">
          <v-avatar size="150" class="mb-6">
            <v-img v-if="selectedPlayer?.avatar" :src="selectedPlayer.avatar" alt="Player avatar"></v-img>
            <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="100"></v-icon>
          </v-avatar>

          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-label">Nickname</div>
              <div class="stat-value">{{ selectedPlayer?.username }}</div>
            </div>

            <div class="stat-item">
              <div class="stat-label">Full Name</div>
              <div class="stat-value">{{ selectedPlayer?.first_name }} {{ selectedPlayer?.last_name }}</div>
            </div>

            <div class="stat-item">
              <div class="stat-label">Country</div>
              <div class="stat-value">{{ selectedPlayer?.country }}</div>
            </div>

            <div class="stat-item">
              <div class="stat-label">Win Ratio</div>
              <div class="stat-value" style="color: #FED854FF;">{{ selectedPlayer?.game_win_ratio }}</div>
            </div>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn
            block
            class="close-btn"
            @click="showPlayerModal = false"
            max-width="30px"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>

  <!-- Name Edit Dialog -->
  <v-dialog v-model="showNameEdit" max-width="500px" class="edit-dialog">
    <v-card>
      <v-card-title class="dialog-title">Edit Team Name</v-card-title>
      <v-card-text>
        <v-alert
          v-if="nameError"
          type="error"
          variant="tonal"
          class="mb-4"
        >
          {{ nameError }}
        </v-alert>
        <v-text-field
          v-model="editedName"
          label="Team Name"
          variant="outlined"
        ></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" @click="showNameEdit = false">Cancel</v-btn>
        <v-btn color="primary" @click="updateName">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Logo Edit Dialog -->
  <v-dialog v-model="showLogoEdit" max-width="500px" class="edit-dialog">
    <v-card>
      <v-card-title class="dialog-title">Update Team Logo</v-card-title>
      <v-card-text>
        <v-alert
          v-if="logoError"
          type="error"
          variant="tonal"
          class="mb-4"
        >
          {{ logoError }}
        </v-alert>
        <v-file-input
          v-model="logoFile"
          label="Choose logo"
          accept="image/*"
          variant="outlined"
          prepend-icon="mdi-camera"
        ></v-file-input>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" @click="showLogoEdit = false">Cancel</v-btn>
        <v-btn color="primary" @click="updateLogo">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Add Player Dialog -->
  <v-dialog v-model="showAddPlayer" max-width="500px" class="edit-dialog">
    <v-card>
      <v-card-title class="dialog-title">Add Player to Team</v-card-title>
      <v-card-text>
        <v-alert
          v-if="addPlayerError"
          type="error"
          variant="tonal"
          class="mb-4"
        >
          {{ addPlayerError }}
        </v-alert>
        <v-autocomplete
          v-model="selectedPlayerId"
          :items="availablePlayers"
          item-title="username"
          item-value="id"
          label="Select Player"
          variant="outlined"
          :loading="loadingPlayers"
        >
          <template v-slot:item="{ props, item }">
            <v-list-item v-bind="props" :title="item.raw.username">
              <template v-slot:prepend>
                <v-avatar size="32">
                  <v-img v-if="item.raw.avatar" :src="item.raw.avatar"></v-img>
                  <v-icon v-else>mdi-account</v-icon>
                </v-avatar>
              </template>
            </v-list-item>
          </template>
        </v-autocomplete>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" @click="showAddPlayer = false">Cancel</v-btn>
        <v-btn color="primary" @click="addPlayer">Add Player</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { API_URL } from '@/config'
import { useAuthStore } from '@/stores/auth'

interface Player {
  id: string
  username: string
  first_name: string
  last_name: string
  avatar: string | null
  game_win_ratio: string
  country: string
  user_email: string | null
  team_name: string
}

interface Match {
  id: string
  team1_name: string
  team2_name: string
  tournament_title: string
  stage: string
  winner_id: string
}

interface PrizeCut {
  id: string
  tournament_name: string
  prize_cut: number
  place: number
}

interface TeamStats {
  tournaments_played: number
  tournaments_won: number
  tournament_win_loss_ratio: {
    ratio: string
  }
  matches_played: number
  matches_won: number
  match_win_loss_ratio: {
    ratio: string
  }
  most_often_played_opponent: string
  best_opponent: string
  worst_opponent: string
}

interface Team {
  id: string
  name: string
  logo: string | null
  players: Player[]
  matches: Match[]
  prize_cuts: PrizeCut[]
  team_stats: TeamStats
}

const route = useRoute()
const authStore = useAuthStore()
const team = ref<Team | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const playerDialog = ref(false)
const selectedPlayer = ref<Player | null>(null)
const showPlayerModal = ref(false)


// Edit name state
const showNameEdit = ref(false)
const editedName = ref('')
const nameError = ref('')

// Edit logo state
const showLogoEdit = ref(false)
const logoFile = ref<File | null>(null)
const logoError = ref('')

// Add player state
const showAddPlayer = ref(false)
const selectedPlayerId = ref('')
const availablePlayers = ref<Player[]>([])
const loadingPlayers = ref(false)
const addPlayerError = ref('')

const canEdit = computed(() => {
  if (!authStore.isAuthenticated) return false
  return authStore.userRole === 'admin' || authStore.userRole === 'director'
})


const formatPlace = (place: number): string => {
  return place === 1 ? '1st' : place === 2 ? '2nd' : `${place}th`
}

// Edit handlers
const openNameEdit = () => {
  if (!team.value) return
  editedName.value = team.value.name
  showNameEdit.value = true
}

const handlePlayerClick = (playerId: string) => {
  fetchPlayer(playerId)
  showPlayerModal.value = true
}

const openLogoEdit = () => {
  logoFile.value = null
  showLogoEdit.value = true
}

const openAddPlayerDialog = async () => {
  try {
    loadingPlayers.value = true
    addPlayerError.value = ''
    const response = await fetch(`${API_URL}/players/?is_available=true`)
    if (!response.ok) throw new Error('Failed to load available players')
    availablePlayers.value = await response.json()
    showAddPlayer.value = true
  } catch (e) {
    console.error('Error fetching available players:', e)
    addPlayerError.value = 'Failed to load available players'
  } finally {
    loadingPlayers.value = false
  }
}

const updateName = async () => {
  if (!team.value) return
  try {
    nameError.value = ''
    const response = await fetch(
      `${API_URL}/teams/${team.value.id}?name=${encodeURIComponent(editedName.value)}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      }
    )

    if (!response.ok) {
      const error = await response.text()
      throw new Error(error)
    }

    await fetchTeamDetails()
    showNameEdit.value = false
  } catch (e) {
    console.error('Error updating team name:', e)
    nameError.value = e.message || 'Failed to update team name'
  }
}

const updateLogo = async () => {
  if (!team.value || !logoFile.value) return
  try {
    logoError.value = ''
    const formData = new FormData()
    formData.append('logo', logoFile.value)

    const response = await fetch(
      `${API_URL}/teams/${team.value.id}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        },
        body: formData
      }
    )

    if (!response.ok) {
      const error = await response.text()
      throw new Error(error)
    }

    await fetchTeamDetails()
    showLogoEdit.value = false
  } catch (e) {
    console.error('Error updating team logo:', e)
    logoError.value = e.message || 'Failed to update team logo'
  }
}

const addPlayer = async () => {
  if (!team.value || !selectedPlayerId.value) return
  try {
    addPlayerError.value = ''
    const response = await fetch(
      `${API_URL}/players/${selectedPlayerId.value}?team_name=${encodeURIComponent(team.value.name)}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      }
    )

    if (!response.ok) {
      const error = await response.text()
      throw new Error(error)
    }

    await fetchTeamDetails()
    showAddPlayer.value = false
  } catch (e) {
    console.error('Error adding player:', e)
    addPlayerError.value = e.message || 'Failed to add player'
  }
}

const fetchTeamDetails = async () => {
  try {
    loading.value = true
    const response = await fetch(`${API_URL}/teams/${route.params.id}`)

    if (!response.ok) {
      throw new Error('Failed to fetch team details')
    }

    team.value = await response.json()
  } catch (err) {
    console.error('Error fetching team details:', err)
    error.value = 'Failed to load team details'
  } finally {
    loading.value = false
  }
}

const fetchPlayer = async (playerId: string) => {
  try {
    const response = await fetch(`${API_URL}/players/${playerId}`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    selectedPlayer.value = await response.json()
  } catch (e) {
    console.error('Error fetching player:', e)
  }
}

const showPlayerInfo = (player: Player) => {
  fetchPlayer(player.id)
  playerDialog.value = true
}

onMounted(fetchTeamDetails)
</script>

<style scoped>
.team-wrapper {
  min-height: 100vh;
  position: relative;
}

.header-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 900px;
  background-size: cover;
  background-position: center;
  z-index: 1;
  opacity: 0.2;
}

.header-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 900px;
  background: linear-gradient(
    to bottom,
    rgba(23, 28, 38, 0) 0%,
    rgba(23, 28, 38, 0.8) 20%,
    rgba(23, 28, 38, 1) 60%
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
.team-header-card {
  background: rgba(45, 55, 75, 0.3);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  margin-bottom: 24px;
  text-align: center;
  width: 100%;
  max-width: 1000px;
  justify-self: center;
}

.team-title {
  color: #42DDF2FF;
  font-size: 2.5rem;
  margin-bottom: 20px;
  font-weight: 700;
  text-shadow: 0 0 10px rgba(66, 221, 242, 0.3);
}

.players-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 20px;
  padding: 20px;
}

.player-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}

.player-item:hover {
  transform: translateY(-5px);
}

.player-avatar {
  border: 2px solid #42DDF2FF;
  background: rgba(8, 87, 144, 0.1);
  transition: all 0.2s;
}

.player-avatar:hover {
  transform: scale(1.1);
  box-shadow: 0 0 5px rgba(66, 221, 242, 0.5);
}

.player-name {
  color: white;
  font-size: 0.9rem;
  opacity: 0.9;
}

.team-content-wrapper {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.stats-card, .content-card {
  background: rgba(45, 55, 75, 0.4);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  height: 100%;
  transition: transform 0.2s;
}

.stats-card:hover, .content-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(8, 87, 144, 0.4);
}

.section-title {
  color: #42DDF2FF;
  font-size: 1.4rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: rgba(45, 55, 75, 0.8);
  border: 1px solid rgba(8, 87, 144, 0.5);
  border-radius: 10px;
  transition: all 0.2s;
}

.stat-item:hover {
  background: rgba(45, 55, 75, 0.9);
  border-color: #42DDF2FF;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

.stat-value {
  color: white;
  font-weight: 500;
}

.glow-text {
  color: #FED854FF;
  text-shadow: 0 0 10px rgba(254, 216, 84, 0.3);
}

.accent-text {
  color: #42DDF2FF;
  text-shadow: 0 0 10px rgba(66, 221, 242, 0.3);
}

.prizes-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.prize-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(45, 55, 75, 0.8);
  border: 1px solid rgba(8, 87, 144, 0.5);
  border-radius: 10px;
  transition: all 0.2s;
}

.prize-item.gold {
  border-color: #FED854FF;
  background: rgba(254, 216, 84, 0.1);
}

.prize-item.silver {
  border-color: #C0C0C0;
  background: rgba(192, 192, 192, 0.1);
}

.prize-trophy {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.prize-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tournament-name {
  color: white;
  font-size: 1rem;
}

.prize-place {
  color: #42DDF2FF;
  font-size: 0.9rem;
}

.matches-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.match-item {
  padding: 16px;
  background: rgba(45, 55, 75, 0.8);
  border: 1px solid rgba(8, 87, 144, 0.5);
  border-radius: 10px;
  transition: all 0.2s;
}

.match-teams {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.team1, .team2 {
  color: white;
  font-size: 1rem;
}

.vs {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
}

.winner {
  color: #FED854FF;
  text-shadow: 0 0 10px rgba(254, 216, 84, 0.3);
}

.match-info {
  display: flex;
  justify-content: space-between;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin-top: 8px;
}

.match-stage {
  color: #42DDF2FF;
}

.match-result {
  text-align: center;
  margin-top: 8px;
  font-weight: 500;
  color: #ff4444;
}

.match-result.won {
  color: #FED854FF;
  text-shadow: 0 0 10px rgba(254, 216, 84, 0.3);
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
}

/* Dialog Styles */
.player-dialog :deep(.v-card) {
  width: 400px;
  margin: 0 auto;
  border-radius: 50px !important;
  background: rgba(45, 55, 75, 0.8) !important;
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF !important;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
}

.edit-dialog :deep(.v-card) {
  background: rgba(45, 55, 75, 0.7) !important;
  border: 2px solid #42DDF2FF !important;
  backdrop-filter: blur(10px);
  width: 100%;
  max-width: 400px;
  align-self: center;
}

.dialog-title {
  color: #42DDF2FF !important;
  font-size: 1.5rem !important;
  text-align: center;
  padding: 20px !important;
}

.dialog-content {
  padding: 24px;
}

.player-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.profile-avatar {
  border: 3px solid #42DDF2FF;
  box-shadow: 0 0 20px rgba(66, 221, 242, 0.3);
}

.player-stats {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 16px;
  background: rgba(45, 55, 75, 0.8);
  border-radius: 8px;
  border: 1px solid rgba(8, 87, 144, 0.5);
}

:deep(.v-btn) {
  text-transform: none !important;
  border-radius: 50px !important;
}

:deep(.v-card-actions .v-btn) {
  background: rgba(17, 78, 112, 0.56) !important;
  color: #42DDF2FF !important;
  border: 2px solid #42DDF2FF !important;
  min-width: 120px;
  font-weight: bold;
  letter-spacing: 1px;
  transition: all 0.2s;
}

:deep(.v-card-actions .v-btn:hover) {
  background: rgba(66, 221, 242, 0.1) !important;
  transform: translateY(-2px);
}

.team-title-section {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.edit-controls {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.edit-icon {
  color: #42DDF2FF;
  cursor: pointer;
  opacity: 0.7;
  transition: all 0.2s;
}

.edit-icon:hover {
  opacity: 1;
  transform: scale(1.1);
}

.add-player {
  cursor: pointer;
}

.add-avatar {
  border: 2px dashed #42DDF2FF;
  background: rgba(66, 221, 242, 0.1);
  transition: all 0.2s;
}

.add-avatar:hover {
  border-color: #42DDF2FF;
  background: rgba(66, 221, 242, 0.2);
  transform: scale(1.1);
}

:deep(.v-file-input) {
  color: white !important;
}

:deep(.v-file-input .v-field) {
  color: white !important;
  border-color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.v-file-input .v-field__outline) {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.v-file-input .v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.v-file-input .v-field__input) {
  color: white !important;
}

:deep(.v-file-input .v-icon) {
  color: #42DDF2FF !important;
}

.dialog-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.stats-grid {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-item {
  background: rgba(30, 40, 55, 0.5);
  border: 1px solid rgba(66, 221, 242, 0.3);
  border-radius: 10px;
  padding: 12px 20px;
}

.stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin-bottom: 4px;
}

.stat-value {
  color: white;
  font-size: 1.1rem;
}

.close-btn {
  background: transparent !important;
  color: #42DDF2FF !important;
  border: 2px solid #42DDF2FF !important;
  border-radius: 50px !important;
  margin: 20px !important;
  padding: 10px 40px !important;
  font-size: 1.1rem !important;
}

.close-btn:hover {
  background: rgba(66, 221, 242, 0.1) !important;
}
</style>
