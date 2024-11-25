<template>
  <div class="tournament-list-wrapper">
    <!-- Header with fade effect -->
    <div class="header-image"></div>
    <div class="header-overlay"></div>

    <div class="content-wrapper">
      <v-container>
        <!-- Loading state -->
        <div v-if="isLoadingTournaments" class="d-flex justify-center align-center" style="height: 200px">
          <v-progress-circular indeterminate color="#00ff9d"></v-progress-circular>
        </div>

        <!-- Error state -->
        <div v-else-if="tournamentsError" class="error-text pa-4">
          {{ tournamentsError }}
        </div>

        <!-- Tournaments Grid -->
        <v-row v-else>
          <v-col v-for="tournament in tournaments"
                 :key="tournament.id"
                 cols="12"
                 md="6"
                 class="tournament-column">
            <div class="tournament-card">
              <div
                class="tournament-background"
                :style="{ '--tournament-bg': `url(${getTournamentBackground(tournament.tournament_format)})` }"
              ></div>
              <div class="tournament-content">
                <div class="tournament-header">
                  <h3 class="tournament-title">{{ tournament.title }}</h3>
                  <div class="format-tag">{{ formatText(tournament.tournament_format) }}</div>
                </div>

                <div class="tournament-info">
                  <div class="info-section">
                    <v-icon icon="mdi-calendar" class="mr-2 info-icon"></v-icon>
                    <span>{{ formatDateRange(tournament.start_date, tournament.end_date) }}</span>
                  </div>

                  <div class="info-section">
                    <v-icon icon="mdi-flag" class="mr-2 info-icon"></v-icon>
                    <span>Stage: {{ formatStage(tournament.current_stage) }}</span>
                  </div>

                  <div class="info-section">
                    <v-icon icon="mdi-account-group" class="mr-2 info-icon"></v-icon>
                    <span>{{ tournament.number_of_teams }} teams</span>
                  </div>
<!--                  <div class="info-section">-->
<!--                    <v-icon icon="mdi-cash" class="mr-2 info-icon"></v-icon>-->
<!--                    <span>Prize Pool: {{ formatPrizePool(tournament.prize_pool) }}</span>-->
<!--                  </div>-->
                </div>

                <v-btn class="view-details-btn"
                       variant="outlined"
                       :to="'/tournaments/' + tournament.id">
                  View Details
                </v-btn>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { format } from 'date-fns'
import { API_URL } from '@/config'
import singleEliminationBg from "@/assets/single-elimination.png";
import roundRobinBg from "@/assets/round-robin.png";
import oneOffMatchBg from "@/assets/one-off-match.png";
import topImageBg from "@/assets/top-image.png";

// const formatPrizePool = (prizePool: number): string => {
//   return `${prizePool} pate`;
// };

const getTournamentBackground = (format: string): string => {
  const formatMap: Record<string, string> = {
    "round robin": roundRobinBg,
    "one off match": oneOffMatchBg,
    "single elimination": singleEliminationBg,
  };

  const background = formatMap[format];

  // Log the background URL to ensure correctness
  console.log("Mapped Background URL:", background);

  return background || "@/assets/top-image.png"; // Return an empty string if the format is not found
};


interface Tournament {
  id: string
  title: string
  tournament_format: string
  start_date: string
  end_date: string
  current_stage: string
  number_of_teams: number
  // prize_pool: number
}

import { defineComponent } from 'vue';

enum TournamentFormat {
  SINGLE_ELIMINATION = 'SINGLE_ELIMINATION',
  ROUND_ROBIN = 'ROUND_ROBIN',
  ONE_OFF_MATCH = 'ONE_OFF_MATCH',
}

// Reactive data
const stageFormat = ref(TournamentFormat.SINGLE_ELIMINATION);
const tournaments = ref<Tournament[]>([]);
const isLoadingTournaments = ref(false);
const tournamentsError = ref<string | null>(null);

// // Helper methods
// const getTournamentBackground = (format: string): string => {
//   const formatMap = {
//     [TournamentFormat.SINGLE_ELIMINATION]: "@/assets/single-elimination.png",
//     [TournamentFormat.ROUND_ROBIN]: "@/assets/round-robin.png",
//     [TournamentFormat.ONE_OFF_MATCH]: "@/assets/one-off-match.png",
//   };
//
//   return formatMap[format as TournamentFormat] || "@/assets/top-image.png";
// };

const formatText = (text: string) => {
  return text.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

const formatDateRange = (startDate: string, endDate: string) => {
  const start = format(new Date(startDate), 'dd MMM yyyy')
  const end = format(new Date(endDate), 'dd MMM yyyy')
  return `${start} / ${end}`
}

const formatStage = (stage: string) => {
  return stage.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

// Fetch tournaments
const fetchTournaments = async () => {
  try {
    isLoadingTournaments.value = true;
    tournamentsError.value = null;
    const response = await fetch(`${API_URL}/tournaments/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    tournaments.value = Array.isArray(data) ? data : data.results || [];
  } catch (e) {
    console.error('Error fetching tournaments:', e);
    tournamentsError.value = 'Failed to load tournaments. Please try again later.';
  } finally {
    isLoadingTournaments.value = false;
  }
};

// Lifecycle
onMounted(() => {
  fetchTournaments()
})
</script>

<style scoped>


.tournament-list-wrapper {
  min-height: 100vh;
  position: relative;
}

.header-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px;
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
  height: 400px;
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
  padding-top: 250px;
  min-height: 100vh;
  width: 100vw !important;
}

.tournament-column {
  padding: 16px;
}

.tournament-card {
  position: relative;
  height: 300px;
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
  background-image: var(--tournament-bg, url('@/assets/top-image.png'));
  background-position: center;
  background-size: cover;
  opacity: 0.1;
  z-index: 1;
}

.tournament-content {
  position: relative;
  z-index: 2;
  padding: 24px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.tournament-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.tournament-title {
  color: #42DDF2FF;
  font-size: 1.5rem;
  margin: 0;
  font-weight: 600;
}

.format-tag {
  background: rgba(8, 117, 176, 0.1);
  color: #42DDF2FF;
  padding: 6px 16px;
  border-radius: 12px;
  font-size: 0.9rem;
  border: 1px solid rgba(8, 87, 144, 0.8);
}

.tournament-info {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-section {
  display: flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
}

.info-icon {
  color: #42DDF2FF !important;
}

.view-details-btn {
  margin-top: auto;
  color: #42DDF2FF !important;
  border-color: #42DDF2FF !important;
  width: 100%;
}

.error-text {
  text-align: center;
  color: rgba(255, 255, 255, 0.75);
  padding: 20px;
  background: rgba(255, 0, 0, 0.1);
  border-radius: 10px;
  margin: 20px 0;
}
</style>
