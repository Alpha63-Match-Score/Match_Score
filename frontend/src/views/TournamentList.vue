<template>
  <div class="tournament-list-wrapper">
    <!-- Header with fade effect -->
    <div class="header-image"></div>
    <div class="header-overlay"></div>

    <div class="content-wrapper">
      <v-container>
      <!-- Add Reset Button when filtered -->
      <div class="filter-button-space">
        <div class="filters-wrapper">
          <v-select
            v-model="selectedPeriod"
            :items="periodOptions"
            item-title="text"
            item-value="value"
            label="Period"
            variant="outlined"
            density="comfortable"
            bg-color="rgba(45, 55, 75, 0.8)"
            color="#ffffff"
            menu-icon="mdi-chevron-down"
            @update:model-value="handleFiltersChange"
          />

          <v-select
            v-model="selectedStatus"
            :items="statusOptions"
            item-title="text"
            item-value="value"
            label="Status"
            variant="outlined"
            density="comfortable"
            class="filter-select"
            bg-color="rgba(45, 55, 75, 0.8)"
            color="#ffffff"
            menu-icon="mdi-chevron-down"
            @update:model-value="handleFiltersChange"
          ></v-select>
        </div>

        <transition name="fade">
          <div class="reset-filter-wrapper">
            <v-btn
              class="reset-filter-btn"
              variant="outlined"
              @click="resetFilters"
              prepend-icon="mdi-filter-off"
            >
              Show All Tournaments
            </v-btn>
          </div>
        </transition>
      </div>

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
                  <div
                    class="format-tag"
                    @click="handleFormatClick(tournament.tournament_format)"
                    role="button"
                    :class="{ 'format-tag--loading': isLoadingTournaments }"
                  >
                    {{ formatText(tournament.tournament_format).toUpperCase() }}
                  </div>
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
                       :to="'/events/' + tournament.id">
                  View Details
                </v-btn>
              </div>
            </div>
          </v-col>
        </v-row>
        <!-- Load More Button -->
          <div v-if="!isLoadingTournaments && hasMoreTournaments" class="load-more-wrapper">
            <v-btn
              class="load-more-btn"
              variant="outlined"
              @click="loadMoreTournaments"
              :loading="isLoadingMore"
              :disabled="isLoadingMore"
            >
              <v-icon left class="mr-2">mdi-refresh</v-icon>
              Load More Tournaments
            </v-btn>
          </div>
      </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { format } from 'date-fns'
import { API_URL } from '@/config'
import singleEliminationBg from "@/assets/single-elimination.png";
import roundRobinBg from "@/assets/round-robin.png";
import oneOffMatchBg from "@/assets/one-off-match.png";

interface Tournament {
  id: string
  title: string
  tournament_format: string
  start_date: string
  end_date: string
  current_stage: string
  number_of_teams: number
}

interface FilterOption {
  text: string
  value: string
}

const isFiltered = ref(false);
const tournaments = ref<Tournament[]>([]);
const isLoadingTournaments = ref(false);
const tournamentsError = ref<string | null>(null);
const currentLimit = ref(10);
const hasMoreTournaments = ref(true);
const isLoadingMore = ref(false);
const selectedPeriod = ref('all');
const selectedStatus = ref('all');

const periodOptions: FilterOption[] = [
  { text: 'All Tournaments', value: 'all' },
  { text: 'Upcoming', value: 'future' },
  { text: 'Current', value: 'present' },
  { text: 'Past', value: 'past' }
]

const statusOptions: FilterOption[] = [
  { text: 'All Status', value: 'all' },
  { text: 'Active', value: 'active' },
  { text: 'Finished', value: 'finished' }
]

const handleFiltersChange = async () => {
  try {
    isLoadingTournaments.value = true;
    tournamentsError.value = null;
    currentLimit.value = 10; // Reset limit

    let url = `${API_URL}/tournaments/?offset=0&limit=${currentLimit.value}`;

    if (selectedPeriod.value !== 'all') {
      url += `&period=${selectedPeriod.value}`;
    }

    if (selectedStatus.value !== 'all') {
      url += `&status=${selectedStatus.value}`;
    }

    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    const results = Array.isArray(data) ? data : data.results || [];
    tournaments.value = results;
    isFiltered.value = selectedPeriod.value !== 'all' || selectedStatus.value !== 'all';
    hasMoreTournaments.value = results.length === currentLimit.value;

  } catch (e) {
    console.error('Error fetching tournaments:', e);
    tournamentsError.value = 'Failed to load tournaments. Please try again later.';
  } finally {
    isLoadingTournaments.value = false;
  }
};

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


const handleFormatClick = async (format: string) => {
  try {
    isLoadingTournaments.value = true;
    tournamentsError.value = null;
    currentLimit.value = 10; // Reset limit
    const encodedFormat = encodeURIComponent(format.toLowerCase());
    console.log('Encoded Format:', encodedFormat);

    const response = await fetch(
      `${API_URL}/tournaments/?tournament_format=${encodedFormat}&offset=0&limit=${currentLimit.value}`
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    const results = Array.isArray(data) ? data : data.results || [];
    tournaments.value = results;
    isFiltered.value = true;

    // Check if we have reached the end
    hasMoreTournaments.value = results.length === currentLimit.value;

  } catch (e) {
    console.error('Error fetching tournaments:', e);
    tournamentsError.value = 'Failed to load tournaments. Please try again later.';
  } finally {
    isLoadingTournaments.value = false;
  }
};

const resetFilters = async () => {
  selectedPeriod.value = 'all';
  selectedStatus.value = 'active';
  await handleFiltersChange();
};


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

// Lifecycle
onMounted(() => {
  fetchTournaments()
  window.addEventListener('search-results', ((event: CustomEvent) => {
    if (event.detail.route === '/events') {
      // Update tournaments data with search results
      tournaments.value = event.detail.results
      isLoadingTournaments.value = false
      tournamentsError.value = null
    }
  }) as EventListener)
})

// Don't forget to remove the event listener when component is destroyed
onUnmounted(() => {
  window.removeEventListener('search-results', ((event: CustomEvent) => {
    if (event.detail.route === '/events') {
      tournaments.value = event.detail.results
    }
  }) as EventListener)
})
</script>


<style scoped>

.filters-wrapper {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 16px;
  width: 100%;
  max-width: 500px; /* или каквато ширина предпочитате */
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


.reset-filter-wrapper {
  margin-top: 8px;
  margin-bottom: 16px;
}

.reset-filter-wrapper.hidden {
  opacity: 0;
  transform: translateY(-20px);
}

.reset-filter-btn {
  background: rgba(45, 55, 75, 0.8);
  color: #ffffff !important;
  border-color: rgba(255, 255, 255, 0.7)  !important;
  border-width: 0.5px !important;
  border-radius: 50px;
  transition: all 0.2s ease;
  padding: 7px 40px !important;
  font-size: 1.1rem !important;
}

.reset-filter-btn:hover {
  border-color: #ffffff !important;
  transform: translateY(-2px);
}

.tournament-list-wrapper {
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
  height: 600px; /* Same as header-image */
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
  padding-top: 100px;
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
  justify-content: space-between;
  gap: 10px;
}

.tournament-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  height: 100px;
}

.tournament-title {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.5rem;
  margin: 0;
  font-weight: 600;
  font-family: Orbitron, sans-serif;
  max-width: 320px;
}

.format-tag {
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

.format-tag--loading {
  opacity: 0.7;
  cursor: wait;
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.reset-filter-wrapper {
  position: absolute;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  margin-top: 70px;
}

.filter-button-space {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 30px;
  position: relative;
  z-index: 4;
}

</style>
