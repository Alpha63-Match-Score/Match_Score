<template>
  <div class="match-list-wrapper">
    <!-- Header with fade effect -->
    <div class="header-image"></div>
    <div class="header-overlay"></div>

    <div class="content-wrapper">
      <v-container>
        <!-- Filter Fields -->
        <v-row class="filter-row">
          <v-col cols="12" md="3">
            <v-select
              v-model="selectedStage"
              :items="stages"
              item-title="text"
              item-value="value"
              label="Stage"
              variant="outlined"
              density="comfortable"
              bg-color="rgba(45, 55, 75, 0.4)"
              color="#42DDF2FF"
              clearable
            ></v-select>
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="selectedIsFinished"
              :items="isFinishedOptions"
              item-title="text"
              item-value="value"
              label="Status"
              variant="outlined"
              density="comfortable"
              bg-color="rgba(45, 55, 75, 0.4)"
              color="#42DDF2FF"
              clearable
            ></v-select>
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="selectedTeam"
              :items="teams"
              item-title="text"
              item-value="value"
              label="Team"
              variant="outlined"
              density="comfortable"
              bg-color="rgba(45, 55, 75, 0.4)"
              color="#42DDF2FF"
              clearable
            ></v-select>
          </v-col>
        </v-row>

        <!-- Loading state -->
        <div v-if="isLoadingMatches" class="d-flex justify-center align-center" style="height: 200px">
          <v-progress-circular indeterminate color="#00ff9d"></v-progress-circular>
        </div>

        <!-- Error state -->
        <div v-else-if="matchesError" class="error-text pa-4">
          {{ matchesError }}
        </div>

        <!-- Matches Grid -->
        <v-row v-else justify="center">
          <v-col v-for="match in matches" :key="match.id" cols="12" md="6" class="match-column">
            <v-card class="match-card" @click="openMatchDialog(match)">
              <div class="match-card-content match-list-card">
                <div class="tournament-header-section">
                  <h3 class="match-card-tournament-title">{{ match.tournament_title }}</h3>
                  <div class="tournament-format">
                    {{ getTournamentFormat(match.tournament_id).toUpperCase() }}
                  </div>
                </div>
                <v-card-text>
                  <div class="match-layout">
                    <div class="team-info-left">
                      <v-tooltip location="top">
                        <template v-slot:activator="{ props }">
                          <v-avatar class="team-avatar" size="60" v-bind="props">
                            <v-img v-if="match.team1_logo" :src="match.team1_logo" :alt="match.team1_name"></v-img>
                            <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                          </v-avatar>
                        </template>
                        {{ match.team1_name }}
                      </v-tooltip>
                      <span class="team-score">{{ match.team1_score }}</span>
                    </div>

                    <div class="score-divider">:</div>

                    <div class="team-info-right">
                      <span class="team-score">{{ match.team2_score }}</span>
                      <v-tooltip location="top">
                        <template v-slot:activator="{ props }">
                          <v-avatar class="team-avatar" size="60" v-bind="props">
                            <v-img v-if="match.team2_logo" :src="match.team2_logo" :alt="match.team2_name"></v-img>
                            <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                          </v-avatar>
                        </template>
                        {{ match.team2_name }}
                      </v-tooltip>
                    </div>
                  </div>
                </v-card-text>
                <v-divider class="match-divider"></v-divider>
                <v-card-actions class="justify-center pa-4">
                  <v-icon icon="mdi-clock-outline" class="mr-2 neon-text"></v-icon>
                  <span class="time-text">{{ format(new Date(match.start_time), 'HH:mm, dd MMM yyyy') }}</span>
                </v-card-actions>
                </div>
            </v-card>
          </v-col>
        </v-row>

        <!-- Match Modal -->
        <v-dialog v-model="showMatchModal" max-width="800px" class="match-dialog">
          <v-card class="custom-dialog-card">
            <v-card-title class="headline text-center">
              {{ selectedMatch?.team1_name }} vs {{ selectedMatch?.team2_name }}
            </v-card-title>
            <v-card-text>
              <div class="match-details-centered">
                <div class="tournament-title">{{ selectedMatch?.tournament_title }}</div>
                <div class="tournament-stage">{{ selectedMatch?.stage }}</div>
                <div class="is-finished">{{ selectedMatch?.is_finished ? 'Finished' : 'Not finished' }}</div>

                <div class="match-layout">
                  <div class="team-info-left">
                    <v-tooltip location="top">
                      <template v-slot:activator="{ props }">
                        <router-link :to="`/teams/${selectedMatch?.team1_id}`" class="team-avatar-link">
                          <v-avatar class="team-avatar" size="150" v-bind="props">
                            <v-img v-if="selectedMatch?.team1_logo" :src="selectedMatch.team1_logo" :alt="selectedMatch.team1_name"></v-img>
                            <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                          </v-avatar>
                        </router-link>
                      </template>
                      {{ selectedMatch?.team1_name }}
                    </v-tooltip>
                    <span class="team-score">{{ selectedMatch?.team1_score }}</span>
                  </div>
                  <div class="score-divider">:</div>

                  <div class="team-info-right">
                    <span class="team-score">{{ selectedMatch?.team2_score }}</span>
                    <v-tooltip location="top">
                      <template v-slot:activator="{ props }">
                        <router-link :to="`/teams/${selectedMatch?.team2_id}`" class="team-avatar-link">
                          <v-avatar class="team-avatar" size="150" v-bind="props">
                            <v-img v-if="selectedMatch?.team2_logo" :src="selectedMatch.team2_logo" :alt="selectedMatch.team2_name"></v-img>
                            <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                          </v-avatar>
                        </router-link>
                      </template>
                      {{ selectedMatch?.team2_name }}
                    </v-tooltip>
                  </div>
                </div>

                <div class="match-time">
                  <v-icon icon="mdi-clock-outline" class="mr-2 neon-text"></v-icon>
                  <span class="time-text">
                    {{ selectedMatch ? format(new Date(selectedMatch.start_time), 'HH:mm, dd MMM yyyy') : '' }}
                  </span>
                </div>
                <div v-if="selectedMatch?.winner_id" class="winner">
                  <v-icon icon="mdi-crown" color="#fed854" size="24"></v-icon>
                  <span class="winner-name">
                    {{ selectedMatch.winner_id === selectedMatch.team1_id ? selectedMatch.team1_name : selectedMatch.team2_name }}
                  </span>
                </div>
              </div>
            </v-card-text>
            <v-card-actions>
              <v-btn @click="showMatchModal = false">
                Close
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Load More Button -->
        <div v-if="!isLoadingMatches && hasMoreMatches" class="load-more-wrapper">
          <v-btn
            class="load-more-btn"
            variant="outlined"
            @click="loadMoreMatches"
            :loading="isLoadingMore"
            :disabled="isLoadingMore"
          >
            <v-icon left class="mr-2">mdi-refresh</v-icon>
            Load More Matches
          </v-btn>
        </div>
      </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { API_URL } from '@/config'
import { format } from 'date-fns'

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
  team2_name: string
  team1_logo: string | null
  team2_logo: string | null
  winner_id: string | null
  tournament_id: string
  tournament_title: string
}

interface Tournament {
  id: string
  tournament_format: string
}

interface Team {
  id: string
  name: string
}

interface FilterOption {
  text: string
  value: string
}

const matches = ref<Match[]>([])
const tournaments = ref<Tournament[]>([])
const teams = ref<FilterOption[]>([])
const isLoadingMatches = ref(false)
const matchesError = ref<string | null>(null)
const currentLimit = ref(10)
const hasMoreMatches = ref(true)
const isLoadingMore = ref(false)
const showMatchModal = ref(false)
const selectedMatch = ref<Match | null>(null)
const selectedFormat = ref<string | null>(null)
const selectedStage = ref<string | null>(null)
const selectedIsFinished = ref<string | null>(null)
const selectedTeam = ref<string | null>(null)

const stages: FilterOption[] = [
  { text: 'Group Stage', value: 'group stage' },
  { text: 'Quarter-finals', value: 'quarter finals' },
  { text: 'Semi-finals', value: 'semi finals' },
  { text: 'Finals', value: 'finals' }
]

const isFinishedOptions: FilterOption[] = [
  { text: 'Active', value: 'active' },
  { text: 'Finished', value: 'finished' }
]

const fetchMatches = async () => {
  try {
    isLoadingMatches.value = true
    matchesError.value = null


    const params = new URLSearchParams()
    if (selectedStage.value) params.append('stage', selectedStage.value)
    if (selectedIsFinished.value === 'active') params.append('is_finished', 'false')
    if (selectedIsFinished.value === 'finished') params.append('is_finished', 'true')
    if (selectedTeam.value) params.append('team_name', selectedTeam.value)
    params.append('offset', '0')
    params.append('limit', currentLimit.value.toString())

    const response = await fetch(`${API_URL}/matches/?${params}`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    matches.value = Array.isArray(data) ? data : (data.results || [])
    hasMoreMatches.value = matches.value.length === currentLimit.value
  } catch (e) {
    console.error('Error fetching matches:', e)
    matchesError.value = 'Failed to load matches. Please try again later.'
  } finally {
    isLoadingMatches.value = false
  }
}

const fetchTournaments = async () => {
  try {
    const response = await fetch(`${API_URL}/tournaments/?offset=0&limit=10`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    tournaments.value = Array.isArray(data) ? data : (data.results || [])
  } catch (e) {
    console.error('Error fetching tournaments:', e)
  }
}


const fetchTeams = async () => {
  try {
    const response = await fetch(`${API_URL}/teams/?offset=0&limit=100`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()

    const teamsData = Array.isArray(data) ? data : (data.results || [])

    teams.value = teamsData.map((team: Team) => ({
      text: team.name,
      value: team.name
    }))
  } catch (e) {
    console.error('Error fetching teams:', e)
  }
}

const loadMoreMatches = async () => {
  currentLimit.value += 10
  await fetchMatches()
}

const openMatchDialog = async (match: Match) => {
  try {
    const response = await fetch(`${API_URL}/matches/${match.id}`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    selectedMatch.value = await response.json()
    showMatchModal.value = true
  } catch (e) {
    console.error('Error fetching match details:', e)
  }
}

const getTournamentFormat = (tournamentId: string) => {
  const tournament = tournaments.value.find(t => t.id === tournamentId)
  return tournament ? tournament.tournament_format : 'Unknown Format'
}

onMounted(() => {
  fetchMatches()
  fetchTournaments()
  fetchTeams()
  window.addEventListener('search-results', ((event: CustomEvent) => {
    if (event.detail.route === '/matches') {
      matches.value = event.detail.results
      console.log('Received search results:', matches.value)
      isLoadingMatches.value = false
      matchesError.value = null
    }
  }) as EventListener)
})

watch([selectedStage, selectedIsFinished, selectedTeam], () => {
  currentLimit.value = 10 // Reset to initial limit when filters change
  fetchMatches()
})

onUnmounted(() => {
  window.addEventListener('search-results', ((event: CustomEvent) => {
    if (event.detail.route === '/matches') {
      matches.value = event.detail.results
      console.log('Received search results:', matches.value)
      isLoadingMatches.value = false
      matchesError.value = null
    }
  }) as EventListener)
})
</script>

<style scoped>
.match-list-wrapper {
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
    rgba(23, 28, 38, 0.8) 25%,
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

.match-column {
  display: flex;
  justify-content: flex-end;
  padding: 8px;
}

.match-column:nth-child(even) {
  justify-content: flex-start;
}


.match-card {
  height: 300px;
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  background: rgba(45, 55, 75, 0.4);
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  width: 500px;
}

.match-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0 20px rgba(8, 117, 176, 0.4);
}

.match-card-content {
  position: relative;
  z-index: 3;
  height: 100%;
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.tournament-header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  height: 100px;
}

.match-card-tournament-title {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.5rem;
  margin: 0;
  font-weight: 600;
  font-family: Orbitron, sans-serif;
  max-width: 250px;
}

.match-layout {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 0 10px;
}

.match-card .team-info-left, .team-info-right {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

.match-card .team-avatar {
  min-width: 60px;
  min-height: 60px;
  border: 2px solid #42ddf2;
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s ease;
}

.match-card .team-score {
  font-size: 2rem;
  font-weight: bold;
  color: #fed854;
  text-shadow: 0 0 10px rgba(238, 173, 60, 0.5);
}

.score-divider {
  font-size: 2rem;
  color: #fed854;
  text-shadow: 0 0 10px rgba(238, 173, 60, 0.5);
  margin: 0 8px;
  align-self: center;
}

.match-time {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.neon-text {
  color: #fed854 !important;
}

.time-text {
  color: rgba(255, 255, 255, 0.7);
}

.winner {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.winner-name {
  font-size: 1.5rem;
  font-weight: bold;
  color: #fed854;
  margin-left: 10px;
}


.team-info-left .team-score {
  margin-left: auto; /* Push the score inward */
  margin-right: 10px; /* Fine-tune spacing if needed */
}

.team-info-right .team-score {
  margin-right: auto; /* Push the score inward */
  margin-left: 10px; /* Fine-tune spacing if needed */
}



.team-avatar {
  min-width: 60px;
  min-height: 60px;
  border: 2px solid #42ddf2;
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s ease;
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
  align-self: center; /* Centers it vertically within the layout */
}

.match-divider {
  opacity: 0.2;
  margin: 5px 0;
}

.neon-text {
  color: #fed854 !important;
}

.time-text {
  color: rgba(255, 255, 255, 0.7);
}


.tournament-format {
  display: inline-block !important; /* Adjust width based on content */
  background: rgba(17, 78, 112, 0.56);
  color: #42DDF2FF;
  padding: 6px 16px;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid rgba(8, 87, 144, 0.8);
  cursor: pointer;
  text-transform: uppercase; /* This will make the text uppercase */
  text-align: center;
  margin-top: 5px;
}

.tournament-format:hover {
  color: #42DDF2FF !important;
  background: rgba(66, 221, 242, 0.1);
}

.error-text {
  text-align: center !important;
  color: rgba(255, 255, 255, 0.75);
  padding: 10px;
}

.load-more-wrapper {
  display: flex;
  justify-content: center;
  margin: 40px 0;
  position: relative;
  z-index: 4;
}

.load-more-btn {
  background: rgba(17, 78, 112, 0.56);
  color: #ffffff !important;
  border-color: #42DDF2FF !important;
  border-width: 2px !important;
  border-radius: 50px;
  transition: all 0.2s ease;
  padding: 5px 40px !important;
  font-size: 1.1rem !important;
}

.load-more-btn:hover {
  background: rgba(66, 221, 242, 0.1);
  border-color: #42DDF2FF !important;
  transform: translateY(-2px);
  box-shadow: 0 0 15px rgba(66, 221, 242, 0.3);
}

.load-more-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.match-dialog :deep(.v-card) {
  border-radius: 35px !important;
}



.custom-dialog-card {
  width: 600px;
  margin: 0 auto;
  border-radius: 50px;
  background: rgba(45, 55, 75, 0.8);
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  padding: 10px;
}

.custom-dialog-card .v-btn {
  background: rgba(17, 78, 112, 0.56) !important;
  color: #42DDF2FF !important;
  border: 2px solid #42DDF2FF !important;
  border-radius: 50px;
  min-width: 120px;
  font-weight: bold;
  letter-spacing: 1px;
  transition: all 0.2s ease;
}

.team-avatar-link {
  text-decoration: none;
  background: transparent !important;
}

.team-avatar-link:hover {
  text-decoration: none;
  background: transparent !important;
}

.custom-dialog-card .v-btn:hover {
  background: rgba(66, 221, 242, 0.1) !important;
  transform: translateY(-2px);
}

.custom-dialog-card .match-details-centered {
  text-align: center;
  display: flex;
  flex-direction: column;
}

.match-details-centered .team-avatar:hover {
  transform: none;
  cursor: pointer;
}

.match-details-centered .team-avatar {
  border: 3px solid rgba(66, 221, 242, 0);
  background: rgba(8, 87, 144, 0.2);
  transition: none;
  cursor: default;
}

.custom-dialog-card .tournament-title {
  color: #42DDF2FF;
  font-size: 1.6rem;
  font-weight: bold;
  margin-top: -30px;
  align-self: center;
}

.custom-dialog-card .tournament-stage {
  color: #FED854FF;
  font-size: 1.2rem;
}

.custom-dialog-card .is-finished {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  margin-bottom: 8px;
}

.custom-dialog-card .match-layout {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 32px;
  margin: 24px 0;
}

.custom-dialog-card .team-info-left, .team-info-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.custom-dialog-card .score-divider {
  margin: 0 20px;
  font-size: 2.5rem;
  color: #FED854FF;
  text-shadow: 0 0 10px rgba(238, 173, 60, 0.5);
  align-self: center;
  padding-bottom: 10px;
}

.custom-dialog-card .winner {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
}

.custom-dialog-card .winner-name {
  color: #FED854FF;
  font-size: 1.2rem;
  font-weight: bold;
}


:deep(.v-card-title) {
  color: #42DDF2FF !important;
}


.reset-filter-btn .mdi-filter-remove-outline {
  margin-right: 8px;
  color: rgba(255, 255, 255, 0.7) !important;
}

.reset-filter-btn:hover {
  background: rgba(66, 221, 242, 0.1);
  color: #ffffff !important;
  transform: translateY(-2px);
  box-shadow: 0 0 15px rgba(66, 221, 242, 0.3);
}

.filter-row {
  display: flex;
  justify-content: center;
  margin-bottom: 8px;/* Center the row horizontally */
}

.filter-row .v-col {
  max-width: 300px; /* Adjust the max-width as needed */
}

</style>
