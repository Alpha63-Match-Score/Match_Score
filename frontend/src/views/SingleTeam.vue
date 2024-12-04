<template>
  <div class="team-details" v-if="team">
    <!-- Header Section -->
    <div class="header-image" :style="{ backgroundImage: `url(${team.logo})` }"></div>
    <div class="header-overlay"></div>
    <v-container>
      <!-- Main Info Section -->
      <div class="info-container">
        <v-row justify="center" class="mb-6">
          <v-col cols="12" class="text-center">
            <v-card class="team-card team-header-card">
              <v-card-title class="team-header-title">{{ team.name }}</v-card-title>
              <v-card-text>
                <div class="player-icons">
                  <v-avatar v-for="i in 10" :key="i" size="70" class="player-avatar">
                    <v-img v-if="team.players[i-1]" :src="team.players[i-1].avatar" :alt="team.players[i-1].username"></v-img>
                  </v-avatar>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Team Statistics -->
        <v-row>
          <v-col cols="12" md="4">
            <v-card class="team-card">
              <v-card-title>Match Performance</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-content>
                      <span class="stat-title">Matches Played:</span>
                      <span class="stat-value">{{ team.team_stats.matches_played }}</span>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <span class="stat-title">Matches Won:</span>
                      <span class="stat-value">{{ team.team_stats.matches_won }}</span>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <span class="stat-title">Win/Loss Ratio:</span>
                      <span class="stat-value">{{ team.team_stats.match_win_loss_ratio.ratio }}</span>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card class="team-card">
              <v-card-title>Tournament Performance</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-content>
                      <span class="stat-title">Tournaments Played:</span>
                      <span class="stat-value">{{ team.team_stats.tournaments_played }}</span>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <span class="stat-title">Tournaments Won:</span>
                      <span class="stat-value">{{ team.team_stats.tournaments_won }}</span>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <span class="stat-title">Tournament Win/Loss Ratio:</span>
                      <span class="stat-value">{{ team.team_stats.tournament_win_loss_ratio.ratio }}</span>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card class="team-card">
              <v-card-title>Opponent Analysis</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-content>
                      <span class="stat-title">Most Played Opponent:</span>
                      <span class="stat-value">{{ team.team_stats.most_often_played_opponent || 'N/A' }}</span>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <span class="stat-title">Best Opponent:</span>
                      <span class="stat-value">{{ team.team_stats.best_opponent || 'N/A' }}</span>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <span class="stat-title">Worst Opponent:</span>
                      <span class="stat-value">{{ team.team_stats.worst_opponent || 'N/A' }}</span>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>

      <!-- Prizes and Matches Section -->
      <div class="info-container prizes-and-matches">
        <v-row>
          <v-col cols="12" md="6">
            <v-card class="team-card">
              <v-card-title>Prizes</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item
                    v-for="prizeCut in team.prize_cuts"
                    :key="prizeCut.id"
                    class="mb-2"
                  >
                    <v-list-item-content>
                      <span class="stat-title">{{ prizeCut.tournament_name }}:</span>
                      <span class="stat-value">
                        <v-icon v-if="prizeCut.place === 1" color="yellow">mdi-trophy</v-icon>
                        <v-icon v-else-if="prizeCut.place === 2" color="silver">mdi-trophy</v-icon>
                        {{ prizeCut.place === 1 ? '1st place' : '2nd place' }}
                      </span>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card class="team-card">
              <v-card-title>Recent Matches</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item
                    v-for="match in team.matches"
                    :key="match.id"
                    class="mb-2"
                  >
                    <v-list-item-title>{{ match.team1_name }} vs {{ match.team2_name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ match.tournament_title }} - {{ match.stage }}</v-list-item-subtitle>
                    <template v-slot:append>
                      <v-chip :color="match.winner_id === team.id ? 'success' : 'error'">
                        {{ match.winner_id === team.id ? 'Won' : 'Lost' }}
                      </v-chip>
                    </template>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </v-container>
  </div>

  <v-container v-else>
    <v-row justify="center" align="center">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <p class="mt-3">Loading team details...</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { API_URL } from '@/config'

interface Player {
  id: string
  username: string
  first_name: string
  last_name: string
  avatar: string | null
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
const team = ref<Team | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

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

onMounted(fetchTeamDetails)
</script>

<style scoped>
.team-details {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.header-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 700px;
  background-size: cover;
  background-position: top;
  z-index: 1;
  opacity: 1.5;
}

.header-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 700px;
  background: linear-gradient(
    to bottom,
    rgba(23, 28, 38, 0) 10%,
    rgba(23, 28, 38, 0.8) 40%,
    rgba(23, 28, 38, 1) 80%
  );
  z-index: 2;
}

.info-container {
  position: relative;
  z-index: 3;
  margin-top: 20px;
  padding-top: 20px;
}

.prizes-and-matches {
  margin-top: 20px;
  padding-bottom: 50px; /* Prevent clipping */
  position: relative;
  z-index: 3;
}

.team-card {
  border-radius: 20px;
  overflow: hidden;
  background: rgba(45, 55, 75, 0.8);
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
}

.team-header-card {
  padding: 20px;
}

.team-header-title {
  font-size: 2.2rem;
  color: #42DDF2FF;
  margin-top: -20px;
}

.player-icons {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.player-avatar {
  border: 2px solid #42ddf2;
  background: rgba(8, 87, 144, 0.1);
}

.stat-title {
  font-weight: bold;
  margin-right: 5px;
}

.v-theme--light .v-list {
  background: transparent !important;
}

.stat-value {
  font-weight: normal;
}
</style>
