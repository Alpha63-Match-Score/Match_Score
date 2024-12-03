<template>
  <div class="match-list-wrapper">
    <!-- Header with fade effect -->
    <div class="header-image"></div>
    <div class="header-overlay"></div>

    <div class="content-wrapper">
      <v-container>
        <!-- Loading state -->
        <div v-if="isLoadingMatches" class="d-flex justify-center align-center" style="height: 200px">
          <v-progress-circular indeterminate color="#00ff9d"></v-progress-circular>
        </div>

        <!-- Error state -->
        <div v-else-if="matchesError" class="error-text pa-4">
          {{ matchesError }}
        </div>

        <!-- Matches Grid -->
        <v-row v-else>
          <v-col v-for="match in filteredMatches" :key="match.id" cols="12" md="6" class="match-column">
            <v-card class="match-card" @click="openMatchDialog(match)">
              <div class="match-background"></div>
              <div class="match-content">
                <div class="tournament-tag">Tournament {{ match.tournament_title }}</div>
                <div class="tournament-format" @click.stop="filterByFormat(getTournamentFormat(match.tournament_id))">
                  {{ getTournamentFormat(match.tournament_id) }}
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
        <v-dialog v-model="showMatchModal" max-width="800px">
          <v-card class="custom-dialog-card">
            <v-card-title class="headline text-center">
              {{ selectedMatch?.team1_name }} vs {{ selectedMatch?.team2_name }}
            </v-card-title>
            <v-card-text>
              <div class="match-details-centered">
                <div class="tournament-title">{{ selectedMatch?.tournament_title }}</div>
                <div class="tournament-stage">{{ selectedMatch?.stage }}</div>
                <div class="is-finished">{{ selectedMatch?.is_finished ? 'Finished' : 'Ongoing' }}</div>
                <div class="match-layout">
                  <div class="team-info-left">
                    <v-tooltip location="top">
                      <template v-slot:activator="{ props }">
                        <v-avatar class="team-avatar" size="150" v-bind="props">
                          <v-img v-if="selectedMatch?.team1_logo" :src="selectedMatch.team1_logo" :alt="selectedMatch.team1_name"></v-img>
                          <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                        </v-avatar>
                      </template>
                      {{ selectedMatch.team1_name }}
                    </v-tooltip>
                    <span class="team-score">{{ selectedMatch?.team1_score }}</span>
                  </div>
                  <div class="score-divider">:</div>
                  <div class="team-info-right">
                    <span class="team-score">{{ selectedMatch?.team2_score }}</span>
                    <v-tooltip location="top">
                      <template v-slot:activator="{ props }">
                        <v-avatar class="team-avatar" size="150" v-bind="props">
                          <v-img v-if="selectedMatch?.team2_logo" :src="selectedMatch.team2_logo" :alt="selectedMatch.team2_name"></v-img>
                          <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                        </v-avatar>
                      </template>
                      {{ selectedMatch.team2_name }}
                    </v-tooltip>
                  </div>
                </div>
                <div class="match-time">
                  <v-icon icon="mdi-clock-outline" class="mr-2 neon-text"></v-icon>
                  <span class="time-text">{{ format(new Date(selectedMatch?.start_time), 'HH:mm, dd MMM yyyy') }}</span>
                </div>
                <div v-if="selectedMatch?.winner_id" class="winner">
                  <v-icon icon="mdi-crown" color="#fed854" size="24"></v-icon>
                  <span class="winner-name">{{ selectedMatch.winner_id === selectedMatch.team1_id ? selectedMatch.team1_name : selectedMatch.team2_name }}</span>
                </div>
              </div>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" text @click="showMatchModal = false">Close</v-btn>
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { API_URL } from '@/config'
import { format } from 'date-fns'
import singleEliminationBg from "@/assets/single-elimination.png";
import roundRobinBg from "@/assets/round-robin.png";
import oneOffMatchBg from "@/assets/one-off-match.png";

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

const matches = ref<Match[]>([])
const tournaments = ref<Tournament[]>([])
const isLoadingMatches = ref(false)
const matchesError = ref<string | null>(null)
const currentLimit = ref(10)
const hasMoreMatches = ref(true)
const isLoadingMore = ref(false)
const showMatchModal = ref(false)
const selectedMatch = ref<Match | null>(null)
const selectedFormat = ref<string | null>(null)

const fetchMatches = async () => {
  try {
    isLoadingMatches.value = true
    matchesError.value = null
    const response = await fetch(`${API_URL}/matches/?offset=0&limit=${currentLimit.value}`)
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

const getTournamentBackground = (format: string): string => {
  const formatMap: Record<string, string> = {
    "round robin": roundRobinBg,
    "one off match": oneOffMatchBg,
    "single elimination": singleEliminationBg,
  };

  return formatMap[format] || "@/assets/top-image.png";
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

const filterByFormat = (format: string) => {
  selectedFormat.value = format
}

const filteredMatches = computed(() => {
  if (!selectedFormat.value) {
    return matches.value
  }
  return matches.value.filter(match => getTournamentFormat(match.tournament_id) === selectedFormat.value)
})

onMounted(() => {
  fetchMatches()
  fetchTournaments()
})

onUnmounted(() => {
  // Clean up if necessary
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
    rgba(23, 28, 38, 0.8) 80%,
    rgba(23, 28, 38, 1) 100%
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
  padding: 16px;
}

.match-card {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  background: rgba(45, 55, 75, 0.8);
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  width: 100%; /* Adjust the width of the v-card as needed */
}

.match-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(8, 117, 176, 0.2);
}

.match-background {
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

.match-content {
  position: relative;
  z-index: 2;
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 10px;
  width: auto;
}

.match-layout {
  display: flex;
  align-items: center;
  justify-content: space-between; /* Ensures equal spacing */
  margin-top: 20px;
  gap: 20px; /* Adjust if needed for spacing between elements */
  padding: 0 10px;
}

.match-details-centered {
  text-align: center;
}

.tournament-title, .tournament-stage, .is-finished {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 10px 0;
}

.match-layout {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 20px;
  gap: 20px;
  padding: 0 10px;
}

.team-scores-box {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0;
  background: rgba(45, 55, 75, 0.8);
  border: 1px solid rgba(8, 87, 144, 0.2);
  border-radius: 10px;
  padding: 16px;
}

.team-info-left, .team-info-right {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

.team-avatar {
  min-width: 60px;
  min-height: 60px;
  border: 2px solid #42ddf2;
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s ease;
}

.team-logo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 2px solid #42ddf2;
  margin: 0 10px;
}

.team-score {
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

.team-info-left, .team-info-right {
  display: flex;
  align-items: center;
  justify-content: center; /* Centers content horizontally */
  flex: 1; /* Ensures equal width */
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

.tournament-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.tournament-tag {
  position: relative;
  top: 0px; /* Move it downwards */
  left: 0;
  width: auto; /* Adjust width */
  background: rgba(45, 55, 75, 0);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 1.2rem;
  color: #42DDF2FF;
  border: 1px solid rgba(0, 255, 157, 0);
  font-weight: bold;
  text-align: center;
}

.tournament-format {
  //flex: none !important; /* Prevents it from growing */
  display: inline-block !important; /* Adjust width based on content */
  //width: auto !important;
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

.custom-dialog-card {
  width: 600px; /* Adjust the value to make the box smaller */
  margin: 0 auto; /* Center the box horizontally */
  border-radius: 50px;
  background: rgba(45, 55, 75, 0.8);
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
}

.v-dialog .v-card-title {
  text-align: center;
  color: #42DDF2FF;
  font-size: 1.5rem;
  font-weight: bold;
  font-family: Orbitron, sans-serif;
}

</style>
