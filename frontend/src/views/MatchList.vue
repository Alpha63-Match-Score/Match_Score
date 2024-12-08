<template>
  <div class="match-list-wrapper">
    <HeaderSection />

    <div class="content-wrapper">
      <v-container>
        <!-- Filter Fields -->
        <MatchFilterBar
          :teams="teams"
          v-model:stage="selectedStage"
          v-model:status="selectedIsFinished"
          v-model:team="selectedTeam"
        />

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
            <MatchCard
              :match="match"
              :tournament-format="getTournamentFormat(match.tournament_id)"
              @open-match-dialog="openMatchDialog"
            />
          </v-col>
        </v-row>

        <!-- Match Modal -->
        <MatchModalDialog
          v-model="showMatchModal"
          :match="selectedMatch"
          :onMatchUpdate="refreshMatch"
        />

        <!-- Load More Button -->
        <div class="load-more-wrapper">
          <LoadMoreButton
            v-if="!isLoadingMatches && hasMoreMatches"
            :is-loading="isLoadingMore"
            button-text="Load More Matches"
            @load-more="loadMoreMatches"
          />
        </div>
      </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { API_URL } from '@/config'
import HeaderSection from "@/components/HeaderSection.vue";
import MatchFilterBar from "@/components/MatchFilterBar.vue";
import MatchCard from "@/components/MatchCard.vue";
import LoadMoreButton from "@/components/LoadMoreButton.vue";
import MatchModalDialog from "@/components/dialogs/MatchModalDialog.vue";
import type { Match, Tournament, Team, FilterOption } from '@/types/types'

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
const selectedStage = ref<string | null>(null)
const selectedIsFinished = ref<string | null>(null)
const selectedTeam = ref<string | null>(null)


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

const refreshMatch = async () => {
  if (selectedMatch.value) {
    try {
      const response = await fetch(`${API_URL}/matches/${selectedMatch.value.id}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const updatedMatch = await response.json()

      matches.value = matches.value.map(match =>
        match.id === updatedMatch.id ? updatedMatch : match
      )

      selectedMatch.value = updatedMatch
    } catch (e) {
      console.error('Error refreshing match:', e)
    }
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
</style>
