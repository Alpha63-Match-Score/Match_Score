<template>
  <div class="tournament-wrapper">
    <!-- Dynamic header based on tournament format -->
    <div
      class="header-image"
      :style="{ backgroundImage: `url(${getTournamentBackground(tournament?.tournament_format)})` }"
    ></div>
    <div class="header-overlay"></div>

    <div class="content-wrapper">
      <v-container v-if="tournament">
        <!-- Tournament Header Section -->
        <div class="tournament-header-card">
          <div class="tournament-title-section">
            <h1 class="tournament-title">
              {{ tournament.title }}
              <v-icon
                v-if="canEdit"
                icon="mdi-pencil"
                class="edit-icon ml-2"
                @click="openTitleEdit"
              ></v-icon>
            </h1>
            <div class="format-tag">
              {{ formatText(tournament.tournament_format.toUpperCase()) }}
            </div>
          </div>

          <div class="tournament-dates">
            <v-icon icon="mdi-calendar" class="mr-2"></v-icon>
            {{ formatDateRange(tournament.start_date, tournament.end_date) }}
            <v-icon
              v-if="canEdit"
              icon="mdi-pencil"
              class="edit-icon ml-2"
              @click="openEndDateEdit"
            ></v-icon>
          </div>

          <div class="stage-indicator">
            <v-icon icon="mdi-flag-checkered" class="mr-2"></v-icon>
            Current Stage: {{ formatStage(tournament.current_stage) }}
          </div>
        </div>

        <!-- Tournament Content Grid -->
        <v-row class="mt-6">
          <!-- Left Column: Prizes and Teams -->
          <v-col cols="12" md="4">
            <!-- Prizes Section -->
            <div class="prizes-card">
              <h3 class="section-title">
                <v-icon icon="mdi-cat" class="mr-2"></v-icon>
                Prizes
                <v-icon
                  v-if="canEdit"
                  icon="mdi-pencil"
                  class="edit-icon ml-2"
                  @click="openPrizeEdit"
                ></v-icon>
              </h3>
              <div class="prizes-list">
                <div v-for="prize in tournament.prizes" :key="prize.id" class="prize-item">
                  <div class="prize-trophy" :class="{ 'gold': prize.place === 1, 'silver': prize.place === 2 }">
                    <v-icon :icon="prize.place === 1 ? 'mdi-trophy' : 'mdi-trophy-variant'" size="32"></v-icon>
                  </div>
                  <div class="prize-details">
                    <span class="prize-place">{{ formatPlace(prize.place) }} place</span>
                    <span class="prize-amount">{{ prize.prize_cut }} kitty kibbles</span>
                  </div>
                  <v-tooltip location="top">
                    <template v-slot:activator="{ props }">
                      <router-link
                        v-if="prize.team_id"
                        :to="`/teams/${prize.team_id}`"
                        class="winner-team"
                        v-bind="props"
                      >
                        <v-avatar size="50">
                          <v-img
                            v-if="prize.team_logo"
                            :src="prize.team_logo"
                            alt="Winner team logo"
                          ></v-img>
                          <v-icon v-else icon="mdi-shield" color="#42DDF2FF"></v-icon>
                        </v-avatar>
                      </router-link>
                    </template>
                    {{ prize.team_name }}
                  </v-tooltip>
                </div>
              </div>
            </div>

            <!-- Teams List Section -->
            <div class="teams-card">
              <h3 class="section-title">
                <v-icon icon="mdi-account-group" class="mr-2"></v-icon>
                Participating Teams
              </h3>
              <div class="teams-list">
                <router-link
                  v-for="team in tournament.teams"
                  :key="team.id"
                  :to="`/teams/${team.id}`"
                  class="team-item"
                >
                  <v-avatar size="40" class="team-avatar">
                    <v-img v-if="team.logo" :src="team.logo" alt="Team logo"></v-img>
                    <v-icon v-else icon="mdi-shield" color="#42DDF2FF"></v-icon>
                  </v-avatar>
                  <span class="team-name">{{ team.name }}</span>
                </router-link>
              </div>
            </div>
          </v-col>

          <!-- Right Column: Brackets -->
            <v-col cols="12" md="8">
              <div class="brackets-card">
                <h3 class="section-title">
                  <v-icon icon="mdi-tournament" class="mr-2"></v-icon>
                  Tournament Brackets
                </h3>
                <div class="brackets-content">
                  <div class="stage-header">
                    <h4 class="stage-name">
                      {{ formatStage(tournament.current_stage) }}
                    </h4>
                  </div>

                  <div class="matches-grid">
                    <div v-for="match in tournament.matches_of_current_stage"
                         :key="match.id"
                         class="match-card"
                         :class="{ 'match-finished': match.is_finished }">

                      <div class="match-content">
                        <div class="match-layout">
                          <div class="team-left">
                            <v-tooltip location="top">
                              <template v-slot:activator="{ props }">
                                <router-link :to="`/teams/${match.team1_id}`" class="team-avatar-link">
                                  <v-avatar class="team-avatar" size="60" v-bind="props">
                                    <v-img v-if="match.team1_logo" :src="match.team1_logo" :alt="match.team1_name"></v-img>
                                    <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                                  </v-avatar>
                                </router-link>
                              </template>
                              {{ match.team1_name }}
                            </v-tooltip>
                            <span class="team-score">{{match.team1_score}}</span>
                          </div>

                          <div class="score-divider">:</div>

                          <div class="team-right">
                            <span class="team-score">{{match.team2_score}}</span>
                            <v-tooltip location="top">
                              <template v-slot:activator="{ props }">
                                <router-link :to="`/teams/${match.team2_id}`" class="team-avatar-link">
                                  <v-avatar class="team-avatar" size="60" v-bind="props">
                                    <v-img v-if="match.team2_logo" :src="match.team2_logo" :alt="match.team2_name"></v-img>
                                    <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                                  </v-avatar>
                                </router-link>
                              </template>
                              {{ match.team2_name }}
                            </v-tooltip>
                          </div>
                        </div>

                        <v-divider class="match-divider"></v-divider>

                        <div class="match-footer">
                          <div class="match-time">
                            <v-icon icon="mdi-clock-outline" class="mr-2 neon-text"></v-icon>
                            <span class="time-text">{{ format(new Date(match.start_time), 'HH:mm, dd MMM yyyy') }}</span>
                          </div>

                          <div v-if="match.is_finished" class="match-winner">
                            <v-icon icon="mdi-crown" class="winner-icon" color="#FED854FF"></v-icon>
                            <span class="winner-text">{{ match.winner_id === match.team1_id ? match.team1_name : match.team2_name }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </v-col>
        </v-row>
      </v-container>

      <!-- Loading State -->
      <div v-else-if="isLoading" class="loading-container">
        <v-progress-circular indeterminate color="#42DDF2FF"></v-progress-circular>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-container">
        {{ error }}
      </div>
    </div>

    <!-- Title Edit Dialog -->
    <v-dialog v-model="showTitleEdit" max-width="500px">
      <v-card class="edit-dialog">
        <v-card-title>Edit Tournament Title</v-card-title>
        <v-card-text>
          <v-alert
            v-if="titleError"
            type="error"
            variant="tonal"
            class="mb-4"
          >
            {{ titleError }}
          </v-alert>
          <v-text-field
            v-model="editedTitle"
            label="Tournament Title"
            variant="outlined"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="showTitleEdit = false">Cancel</v-btn>
          <v-btn color="primary" @click="updateTitle">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- End Date Edit Dialog -->
    <v-dialog v-model="showEndDateEdit" max-width="500px">
      <v-card class="edit-dialog">
        <v-card-title>Edit End Date</v-card-title>
        <v-card-text>
          <v-alert
            v-if="endDateError"
            type="error"
            variant="tonal"
            class="mb-4"
          >
            {{ endDateError }}
          </v-alert>
          <v-text-field
            v-model="editedEndDate"
            label="End Date"
            type="datetime-local"
            variant="outlined"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="showEndDateEdit = false">Cancel</v-btn>
          <v-btn color="primary" @click="updateEndDate">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Prize Edit Dialog -->
    <v-dialog v-model="showPrizeEdit" max-width="500px">
      <v-card class="edit-dialog">
        <v-card-title>Edit Prize Pool</v-card-title>
        <v-card-text>
          <v-alert
            v-if="prizeError"
            type="error"
            variant="tonal"
            class="mb-4"
          >
            {{ prizeError }}
          </v-alert>
          <v-text-field
            v-model="editedPrizePool"
            label="Prize Pool (Kitty Kibbles)"
            type="number"
            variant="outlined"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="showPrizeEdit = false">Cancel</v-btn>
          <v-btn color="primary" @click="updatePrizePool">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import '@/styles/vuetify.css'
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { format } from 'date-fns'
import { useAuthStore } from '@/stores/auth'
import { API_URL } from '@/config'
import singleEliminationBg from '@/assets/single-elimination.png'
import roundRobinBg from '@/assets/round-robin.png'
import oneOffMatchBg from '@/assets/one-off-match.png'

interface Player {
  id: string
  username: string
  first_name: string
  last_name: string
  country: string
  user_email: string | null
  team_name: string
  avatar: string | null
}

interface Team {
  id: string
  name: string
  logo: string | null
  game_win_ratio: string
  players: Player[]
}

interface Match {
  id: string
  match_format: string
  start_time: string
  is_finished: boolean
  stage: string
  team1_id: string
  team2_id: string
  team1_score: number
  team2_score: number
  team1_name: string
  team1_logo: string
  team2_name: string
  team2_logo: string
  winner_id: string | null
  tournament_id: string
  tournament_title: string
}

interface Prize {
  id: string
  place: number
  prize_cut: number
  tournament_id: string
  tournament_name: string
  team_id: string | null
  team_name: string | null
  team_logo: string | null
}

interface Tournament {
  id: string
  title: string
  tournament_format: string
  start_date: string
  end_date: string
  current_stage: string
  number_of_teams: number
  matches_of_current_stage: Match[]
  teams: Team[]
  prizes: Prize[]
  director_id?: string
}

const route = useRoute()
const authStore = useAuthStore()

const isInitialized = ref(false)
const tournament = ref<Tournament | null>(null)
const isLoading = ref(true)
const error = ref<string | null>(null)

// Edit state
const showTitleEdit = ref(false)
const showEndDateEdit = ref(false)
const showPrizeEdit = ref(false)
const editedTitle = ref('')
const editedEndDate = ref('')
const editedPrizePool = ref(0)
const titleError = ref('')
const endDateError = ref('')
const prizeError = ref('')

const canEdit = computed(() => {
  if (!isInitialized.value || !tournament.value || !authStore.isAuthenticated) return false
  return authStore.userRole === 'admin' || tournament.value.director_id === authStore.userId
})

const getTournamentBackground = (format: string | undefined): string => {
  if (!format) return ''
  const formatMap: Record<string, string> = {
    'round robin': roundRobinBg,
    'one off match': oneOffMatchBg,
    'single elimination': singleEliminationBg
  }
  return formatMap[format] || ''
}

const formatText = (text: string): string => {
  return text.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

const formatDateRange = (startDate: string, endDate: string): string => {
  return `${format(new Date(startDate), 'dd MMM yyyy')} - ${format(new Date(endDate), 'dd MMM yyyy')}`
}

const formatStage = (stage: string): string => {
  if (stage === 'finished') return 'Tournament Completed'
  if (stage === 'final') return 'Finals'
  return stage.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

const formatPlace = (place: number): string => {
  return place === 1 ? '1st' : place === 2 ? '2nd' : `${place}th`
}

const fetchTournament = async () => {
  try {
    isLoading.value = true
    error.value = null
    const response = await fetch(`${API_URL}/tournaments/${route.params.id}`)
    if (!response.ok) throw new Error('Failed to fetch tournament details')
    const data = await response.json()
    tournament.value = data
  } catch (e) {
    console.error('Error fetching tournament:', e)
    error.value = 'Failed to load tournament details'
  } finally {
    isLoading.value = false
  }
}

// Edit handlers
const openTitleEdit = () => {
  if (!tournament.value) return
  editedTitle.value = tournament.value.title
  showTitleEdit.value = true
}

const openEndDateEdit = () => {
  if (!tournament.value) return
  editedEndDate.value = tournament.value.end_date
  showEndDateEdit.value = true
}

const openPrizeEdit = () => {
  if (!tournament.value) return
  editedPrizePool.value = tournament.value.prizes[0]?.prize_cut || 0
  showPrizeEdit.value = true
}

const extractErrorMessage = async (response: Response) => {
  try {
    const responseClone = response.clone()
    const text = await responseClone.text()
    const data = JSON.parse(text)

    // Ако detail е масив (FastAPI validation errors)
    if (data.detail && Array.isArray(data.detail) && data.detail.length > 0) {
      return data.detail[0].msg
    }

    // Ако detail е string (HTTP exceptions)
    if (data.detail && typeof data.detail === 'string') {
      return data.detail
    }

    return 'An error occurred'
  } catch (e) {
    console.error('Error extracting message:', e)
    return 'An error occurred'
  }
}

const updateTitle = async () => {
  try {
    titleError.value = ''
    if (!tournament.value) return

    const response = await fetch(
      `${API_URL}/tournaments/${tournament.value.id}?title=${encodeURIComponent(editedTitle.value)}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    if (!response.ok) {

      titleError.value = await extractErrorMessage(response)
      return
    }

    await fetchTournament()
    showTitleEdit.value = false
  } catch (e) {
    console.error('Update error:', e)
    titleError.value = 'An unexpected error occurred'
  }
}

const updateEndDate = async () => {
  try {
    endDateError.value = ''
    if (!tournament.value) return

    const response = await fetch(
      `${API_URL}/tournaments/${tournament.value.id}?end_date=${encodeURIComponent(editedEndDate.value)}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    if (!response.ok) {
      endDateError.value = await extractErrorMessage(response)
      return
    }

    await fetchTournament()
    showEndDateEdit.value = false
  } catch (e) {
    endDateError.value = 'An unexpected error occurred'
  }
}

const updatePrizePool = async () => {
  try {
    prizeError.value = ''
    if (!tournament.value) return

    const response = await fetch(
      `${API_URL}/tournaments/${tournament.value.id}?prize_pool=${editedPrizePool.value}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    if (!response.ok) {
      prizeError.value = await extractErrorMessage(response)
      return
    }

    await fetchTournament()
    showPrizeEdit.value = false
  } catch (e) {
    prizeError.value = 'An unexpected error occurred'
  }
}


onMounted(async () => {
  await authStore.initializeFromToken()
  isInitialized.value = true
  await fetchTournament()
})


</script>

<style scoped>
.tournament-wrapper {
  min-height: 100vh;
  position: relative;
}

.header-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 700px;
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
  height: 700px;
  background: linear-gradient(
    to bottom,
    rgba(23, 28, 38, 0) 0%,
    rgba(23, 28, 38, 0.8) 20%,
    rgba(23, 28, 38, 1) 40%
  );
  z-index: 2;
}

.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 200px;
  min-height: 100vh;
  width: 100vw !important;
}

.tournament-header-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  margin-bottom: 24px;
}

.tournament-title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.tournament-title {
  color: #42DDF2FF;
  font-size: 2rem;
  margin: 0;
  display: flex;
  align-items: center;
}

.format-tag {
  background: rgba(17, 78, 112, 0.56);
  color: #42DDF2FF;
  padding: 6px 16px;
  border-radius: 50px;
  font-size: 0.9rem;
  border: 1px solid rgba(8, 87, 144, 0.8);
}

.tournament-dates {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.stage-indicator {
  color: #FED854FF;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
}

.teams-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
}

.prizes-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  margin-bottom: 24px;
}

.section-title {
  color: #42DDF2FF;
  font-size: 1.4rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.teams-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.team-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(45, 55, 75, 0.8);
  border: 1px solid rgba(8, 87, 144, 0.5);
  border-radius: 10px;
  transition: all 0.2s;
  text-decoration: none;
}

.team-item:hover {
  background: rgb(45, 55, 75);
  border-color: #42DDF2FF;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(8, 117, 176, 0.2);
}

.team-avatar {
  border: 2px solid #42DDF2FF;
  background: rgba(8, 87, 144, 0.1);
}

.team-name {
  color: white;
  font-size: 1.1rem;
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
  background: rgba(45, 55, 75, 0);
  border: 1px solid rgba(8, 87, 144, 0);
  border-radius: 10px;
}

.prize-trophy {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.prize-trophy.gold {
  color: #FED854FF;
  background: rgba(254, 216, 84, 0.1);
  border: 2px solid #FED854FF;
}

.prize-trophy.silver {
  color: #c6c6c6;
  background: rgba(192, 192, 192, 0.1);
  border: 2px solid #C0C0C0;
}

.prize-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.prize-place {
  color: white;
  font-size: 1.1rem;
  font-weight: 500;
}

.prize-amount {
  color: rgba(64, 231, 237, 0.73);
  font-size: 0.9rem;
  font-weight: 550;
}

.winner-team {
  text-decoration: none;
  background: transparent !important;
}

.winner-team v-avatar {
  border: 2px solid #42DDF2FF;
  transition: transform 0.2s;
  background: transparent !important;
  transition: transform 0.2s;
}

.winner-team:hover {
  background: transparent !important;
  transform: scale(1.2);
}

.brackets-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  height: 100%;
  min-height: 600px;
}


.brackets-content {
  padding: 24px;
  height: auto;
  min-height: 500px;
  background: rgba(45, 55, 75, 0.4);
  border-radius: 12px;
  margin-top: 16px;
}

.stage-header {
  margin-bottom: 24px;
  text-align: center;
}

.stage-name {
  color: #42DDF2FF;
  font-size: 1.6rem;
  font-weight: 500;
}

.stage-section {
  margin-bottom: 32px;
}

.stage-subtitle {
  color: #FED854FF;
  font-size: 1.2rem;
  margin-bottom: 16px;
  padding-left: 16px;
  border-left: 3px solid #FED854FF;
}

.matches-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  padding: 16px;
}

.match-card {
  height: 250px;
  /* remove position: fixed */
  border-radius: 15px;
  overflow: hidden;
  background: rgba(45, 55, 75, 0.8);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  padding: 20px;
}

.match-card:hover {
  transform: translateY(-2px);
  border-color: #42DDF2FF;
  box-shadow: 0 4px 8px rgba(8, 117, 176, 0.2);
}

.match-content {
  position: relative;
  z-index: 2;
}

.match-layout {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  gap: 20px;
  padding: 0 10px;
}

.team-left, .team-right {
  display: flex;
  align-items: center;
  gap: 15px;
  flex: 1;
}

.team-avatar {
  border: 2px solid #42ddf2;
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s ease;
}

.team-avatar:hover {
  transform: scale(1.2);
}

.team-score {
  font-size: 2rem;
  font-weight: bold;
  color: #fed854;
  text-shadow: 0 0 10px rgba(238, 173, 60, 0.5);
}

.score-divider {
  font-size: 2rem;
  color: #FED854FF;
  text-shadow: 0 0 10px rgba(238, 173, 60, 0.5);
  margin: 0 8px;
}

.match-divider {
  opacity: 0.2;
  margin: 16px 0;
}

.match-footer {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
}

.match-time {
  display: flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.7);
}

.neon-text {
  color: #fed854 !important;
}

.match-winner {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #FED854FF;
  font-weight: 500;
}

.winner-icon {
  font-size: 1.2rem;
}

.winner-text {
  font-size: 0.9rem;
}

.team-avatar-link {
  text-decoration: none;
  background: transparent !important;
}

.team-avatar-link:hover {
  text-decoration: none;
  background: transparent !important;
}

.match-time {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  text-align: center;
  margin-bottom: 16px;
}

.team-winner .team-score {
  color: #FED854FF;
}

.match-divider {
  text-align: center;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
  padding: 4px 0;
}

.match-status {
  text-align: center;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(254, 216, 84, 0.3);
  color: #FED854FF;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stage-name {
  color: #42DDF2FF;
  font-size: 1.6rem;
  text-align: center;
  margin-bottom: 24px;
}

.prize-item {
  padding: 12px;
  margin-bottom: 8px; /* по-малко отстояние между призите */
}

.placeholder-text {
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
}

/* Ако трябва да се намали spacing-а между компонентите */
.section-title {
  margin-bottom: 16px;  /* по-малък margin */
}

.placeholder-text {
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
}

.loading-container, .error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
}

.error-container {
  color: #FED854FF;
  font-size: 1.2rem;
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

.edit-dialog {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
}

:deep(.v-card-title) {
  color: #42DDF2FF !important;
}

:deep(.v-text-field) {
  color: white !important;
}

:deep(.v-field__input) {
  color: white !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.v-field__outline) {
  color: rgba(66, 221, 242, 0.3) !important;
}

:deep(.v-btn) {
  text-transform: none;
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

.team-avatar {
  min-width: 55px;
  min-height: 55px;
  border: 1px solid rgba(8, 117, 176, 0.3);
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s;
  cursor: pointer;
}

.team-avatar:hover {
  transform: scale(1.2);
}
</style>
