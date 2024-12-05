<template>
  <div class="team-list-wrapper">
    <!-- Header with fade effect -->
    <div class="header-image"></div>
    <div class="header-overlay"></div>

    <div class="content-wrapper">
      <v-container>
        <!-- Add Reset Button when filtered -->
        <div class="filter-button-space">
          <transition name="fade">
            <div v-if="isFiltered" class="reset-filter-wrapper">
              <v-btn
                class="reset-filter-btn"
                variant="outlined"
                @click="resetFilters"
                prepend-icon="mdi-filter-off"
              >
                Show All Teams
              </v-btn>
            </div>
          </transition>
        </div>

        <!-- Loading state -->
        <div v-if="isLoadingTeams" class="d-flex justify-center align-center" style="height: 200px">
          <v-progress-circular indeterminate color="#00ff9d"></v-progress-circular>
        </div>

        <!-- Error state -->
        <div v-else-if="teamsError" class="error-text pa-4">
          {{ teamsError }}
        </div>

        <!-- Teams Grid -->
        <v-row v-else>
          <v-col v-for="team in teams" :key="team.id" cols="12" md="6" class="team-column">
            <div class="team-card">
              <div class="team-content">
                <div class="team-header">
                  <div class="team-left-section">
                    <v-avatar class="team-avatar" size="100">
                      <v-img v-if="team.logo" :src="team.logo" alt="Team logo"></v-img>
                      <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="100"></v-icon>
                    </v-avatar>
                    <div class="team-info">
                      <div class="team-title">{{ team.name }}</div>
                      <div class="players-avatars">
                        <v-avatar
                          v-for="(player, index) in team.players.slice(0, 10)"
                          :key="player.id"
                          size="36"
                          class="player-avatar"
                          @click="handlePlayerClick(player.id)"
                        >
                          <v-img v-if="player.avatar && player.avatar !== ''" :src="player.avatar" alt="Player avatar"></v-img>
                          <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="24"></v-icon>
                        </v-avatar>
                      </div>
                    </div>
                  </div>

                  <div class="team-right-section">
                    <div class="progress-wrapper">
                      <v-progress-linear
                        :model-value="parseInt(team.game_win_ratio)"
                        color="#42DDF2FF"
                        height="6"
                        rounded
                        class="progress-bar"
                      ></v-progress-linear>
                      <span class="win-ratio">{{ team.game_win_ratio }}</span>
                    </div>
                  </div>
                </div>

                <v-btn class="view-details-btn" variant="outlined" :to="'/teams/' + team.id">
                  View Details
                </v-btn>
              </div>
            </div>
          </v-col>
        </v-row>

        <!-- Player Modal -->
          <v-dialog v-model="showPlayerModal" max-width="600px">
            <v-card>
              <v-card-title>
                <span class="headline">{{ selectedPlayer?.username }}</span>
              </v-card-title>
              <v-card-text>
                <v-avatar size="150" class="player-avatar">
                  <v-img v-if="selectedPlayer?.avatar" :src="selectedPlayer.avatar" alt="Player avatar"></v-img>
                  <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="100"></v-icon>
                </v-avatar>
                <div class="player-info">
                  <p><strong>Username:</strong> {{ selectedPlayer?.username }}</p>
                  <p><strong>First Name:</strong> {{ selectedPlayer?.first_name }}</p>
                  <p><strong>Last Name:</strong> {{ selectedPlayer?.last_name }}</p>
                  <p><strong>Game Win Ratio:</strong> {{ selectedPlayer?.game_win_ratio }}</p>
                  <p><strong>Country:</strong> {{ selectedPlayer?.country }}</p>
                  <p><strong>Email:</strong> {{ selectedPlayer?.user_email }}</p>
                  <p><strong>Team Name:</strong> {{ selectedPlayer?.team_name }}</p>
                </div>
              </v-card-text>
              <v-card-actions>
                <v-btn color="primary" text @click="showPlayerModal = false">Close</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

        <!-- Load More Button -->
        <div v-if="!isLoadingTeams && hasMoreTeams" class="load-more-wrapper">
          <v-btn
            class="load-more-btn"
            variant="outlined"
            @click="loadMoreTeams"
            :loading="isLoadingMore"
            :disabled="isLoadingMore"
          >
            <v-icon left class="mr-2">mdi-refresh</v-icon>
            Load More Teams
          </v-btn>
        </div>
      </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { API_URL } from '@/config'

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

const isFiltered = ref(false)
const teams = ref<Team[]>([])
const isLoadingTeams = ref(false)
const teamsError = ref<string | null>(null)
const currentLimit = ref(10)
const hasMoreTeams = ref(true)
const isLoadingMore = ref(false)
const router = useRouter()
const showPlayerModal = ref(false)
const selectedPlayer = ref<Player | null>(null)
const isLoadingPlayer = ref(false)
const playerError = ref<string | null>(null)

const fetchTeams = async () => {
  try {
    isLoadingTeams.value = true
    teamsError.value = null
    const response = await fetch(`${API_URL}/teams/?sort_by=desc&offset=0&limit=${currentLimit.value}`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    teams.value = Array.isArray(data) ? data : (data.results || [])
    hasMoreTeams.value = teams.value.length === currentLimit.value
  } catch (e) {
    console.error('Error fetching teams:', e)
    teamsError.value = 'Failed to load teams. Please try again later.'
  } finally {
    isLoadingTeams.value = false
  }
}

const loadMoreTeams = async () => {
  currentLimit.value += 10
  await fetchTeams()
}

const fetchPlayer = async (playerId: string) => {
  try {
    isLoadingPlayer.value = true
    playerError.value = null
    const response = await fetch(`${API_URL}/players/${playerId}`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    selectedPlayer.value = await response.json()
  } catch (e) {
    console.error('Error fetching player:', e)
    playerError.value = 'Failed to load player. Please try again later.'
  } finally {
    isLoadingPlayer.value = false
  }
}

const handlePlayerClick = (playerId: string) => {
  fetchPlayer(playerId)
  showPlayerModal.value = true
}

onMounted(() => {
  fetchTeams()
})

onUnmounted(() => {
  // Clean up if necessary
})
</script>

<style scoped>
.team-list-wrapper {
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
    rgba(23, 28, 38, 1) 50%
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

.team-column {
  padding: 16px;
}

.team-card {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  background: rgba(45, 55, 75, 0.8);
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  //height: 500px;
  display: flex;
  flex-direction: column;
  //justify-content: space-between;
  //padding: 24px;
}

.team-content {
  position: relative;
  z-index: 2;
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 10px;
}

/* Add the box styles */
.team-card {
  height: 300px;
}

.team-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.team-left-section {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-grow: 1;
}

.team-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  margin-left: 10px;
}

.team-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #42DDF2FF;
  text-align: center;
  margin-bottom: 5px;
}

.team-avatar {
  min-width: 170px;
  min-height: 170px;
  border: 2px solid #42ddf2;
  background: rgba(8, 87, 144, 0.1);
}

.player-info {
  margin-top: 16px;
}

.player-info p {
  margin: 4px 0;
}

.v-dialog .v-card {
  width: 400px; /* Adjust the value to make the box smaller */
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

.v-dialog .v-card-text {
  display: flex;
  flex-direction: column; /* This will push the avatar to the right */
  align-items: center; /* This will vertically center the content */
  color: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
  font-family: Arial, sans-serif;
}

.v-dialog .player-avatar {
  display: flex;
  margin-bottom: 16px; /* Add some space between the avatar and the player info */
}

.v-dialog .v-card-actions .v-btn {
  color: #42DDF2FF !important;
  border-color: #42DDF2FF !important;
  border-radius: 50px;
}

.v-dialog .v-card-actions .v-btn:hover {
  background: rgba(66, 221, 242, 0.1);
}

.players-avatars {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 4px;
  max-width: 400px;
  flex: 1;
  justify-content: flex-start;
  margin-left: 10px;
}

.player-avatar {
  min-width: 55px;
  min-height: 55px;
  border: 1px solid rgba(8, 117, 176, 0.3);
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s;
  cursor: pointer;
}

.player-avatar:hover {
  transform: scale(1.2);
}

.team-right-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.progress-wrapper {
  display: flex;
  align-items: center;
  color: #42ddf2;
  font-size: 0.9rem;
  width: 170px; /* Match the width of team-avatar */
  text-align: left;
  align-self: flex-end;
  position: absolute;
  bottom: 60px;
  left: 8px;
  margin: 8px;
}

.progress-bar {
  flex-grow: 1;
  bottom: 16px;
}

.win-ratio {
  color: #42ddf2;
  font-size: 0.9rem;
  min-width: 45px;
  text-align: left;
  align-self: flex-end;
  position: absolute;
  bottom: 5px;
  left: 0;
  margin: 8px;
}

.view-details-btn {
  margin-top: 45px;
  align-self: center;
  color: #42DDF2FF !important;
  border-color: #42DDF2FF !important;
  border-radius: 50px;
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

</style>
