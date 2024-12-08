<template>
  <v-dialog v-model="showDialog" max-width="800px" class="match-dialog">
    <v-card class="custom-dialog-card">
      <v-card-title class="headline text-center">
        {{ match?.team1_name }} vs {{ match?.team2_name }}
      </v-card-title>
      <v-card-text>
        <div class="match-details-centered">
          <!-- Error Alert -->
          <v-alert
            v-if="scoreUpdateError"
            type="error"
            variant="tonal"
            class="mb-4 error-alert"
            closable
            @click:close="scoreUpdateError = ''"
          >
            {{ scoreUpdateError }}
          </v-alert>

          <div class="tournament-title">{{ match?.tournament_title }}</div>
          <div class="tournament-stage">{{ match?.stage }}</div>
          <div class="is-finished">{{ match?.is_finished ? 'Finished' : 'Not finished' }}</div>

          <div class="match-layout">
            <div class="team-info-left">
              <div class="avatar-container">
                <div class="edit-container" v-if="canEdit" @click="openTeamEdit">
                  <v-icon icon="mdi-pencil" class="edit-icon"></v-icon>
                  <span class="edit-text">Edit Teams</span>
                </div>
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <router-link :to="`/teams/${match?.team1_id}`" class="team-avatar-link">
                      <v-avatar class="team-avatar" size="150" v-bind="props">
                        <v-img v-if="match?.team1_logo" :src="match.team1_logo" :alt="match.team1_name"></v-img>
                        <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                      </v-avatar>
                    </router-link>
                  </template>
                  {{ match?.team1_name }}
                </v-tooltip>
              </div>
              <span
                class="team-score"
                :class="{ 'clickable': canEdit }"
                @click="canEdit && handleScoreIncrement('team1')"
              >
                {{ match?.team1_score }}
              </span>
            </div>

            <div class="score-divider">:</div>

            <div class="team-info-right">
              <span
                class="team-score"
                :class="{ 'clickable': canEdit }"
                @click="canEdit && handleScoreIncrement('team2')"
              >
                {{ match?.team2_score }}
              </span>
              <div class="avatar-container">
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <router-link :to="`/teams/${match?.team2_id}`" class="team-avatar-link">
                      <v-avatar class="team-avatar" size="150" v-bind="props">
                        <v-img v-if="match?.team2_logo" :src="match.team2_logo" :alt="match.team2_name"></v-img>
                        <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                      </v-avatar>
                    </router-link>
                  </template>
                  {{ match?.team2_name }}
                </v-tooltip>
              </div>
            </div>
          </div>

          <div class="match-time">
            <v-icon icon="mdi-clock-outline" class="mr-2 neon-text"></v-icon>
            <span class="time-text">
              {{ match ? format(new Date(match.start_time), 'HH:mm, dd MMM yyyy') : '' }}
            </span>
            <v-icon
              v-if="canEdit"
              icon="mdi-pencil"
              class="edit-icon ml-2"
              @click="openTimeEdit"
            ></v-icon>
          </div>

          <div v-if="match?.winner_id" class="winner">
            <v-icon icon="mdi-crown" color="#fed854" size="24"></v-icon>
            <span class="winner-name">
              {{ match.winner_id === match.team1_id ? match.team1_name : match.team2_name }}
            </span>
          </div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="closeDialog">Close</v-btn>
      </v-card-actions>
    </v-card>

    <!-- Time Edit Dialog -->
    <v-dialog v-model="showTimeEdit" max-width="500px">
      <v-card class="edit-dialog">
        <v-card-title>Edit Match Time</v-card-title>
        <v-card-text>
          <v-alert
            v-if="editError"
            type="error"
            variant="tonal"
            class="mb-4"
          >
            {{ editError }}
          </v-alert>
          <v-text-field
            v-model="editedStartTime"
            label="Match Time"
            type="datetime-local"
            variant="outlined"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="showTimeEdit = false">Cancel</v-btn>
          <v-btn color="primary" @click="updateTime">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Team Edit Dialog -->
    <v-dialog v-model="showTeamEdit" max-width="500px">
      <v-card class="dialog-card">
        <div class="dialog-content">
          <v-card-title class="dialog-title">Edit Teams</v-card-title>
          <v-card-text>
            <v-alert
              v-if="editError"
              type="error"
              variant="tonal"
              class="mb-4"
            >
              {{ editError }}
            </v-alert>

            <v-form ref="teamForm">
              <div class="team-slot">
                <div class="d-flex align-center">
                  <v-autocomplete
                    v-model="newTeam1"
                    :items="availableTeams"
                    item-title="name"
                    item-value="id"
                    label="Team 1"
                    variant="outlined"
                    :loading="loadingTeams"
                    clearable
                    class="flex-grow-1 custom-autocomplete"
                  >
                    <template v-slot:item="{ props, item }">
                      <v-list-item
                        v-bind="props"
                        :title="item.raw.name"
                        class="team-list-item"
                      ></v-list-item>
                    </template>
                  </v-autocomplete>
                </div>
              </div>

              <div class="team-slot">
                <div class="d-flex align-center">
                  <v-autocomplete
                    v-model="newTeam2"
                    :items="availableTeams"
                    item-title="name"
                    item-value="id"
                    label="Team 2"
                    variant="outlined"
                    :loading="loadingTeams"
                    clearable
                    class="flex-grow-1 custom-autocomplete"
                  >
                    <template v-slot:item="{ props, item }">
                      <v-list-item
                        v-bind="props"
                        :title="item.raw.name"
                        class="team-list-item"
                      ></v-list-item>
                    </template>
                  </v-autocomplete>
                </div>
              </div>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" @click="showTeamEdit = false">Cancel</v-btn>
            <v-btn color="primary" @click="updateTeams">Save</v-btn>
          </v-card-actions>
        </div>
      </v-card>
    </v-dialog>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { format } from 'date-fns'
import { useAuthStore } from '@/stores/auth'
import { API_URL } from '@/config'
import type { Match } from '@/types/types'

interface Props {
  modelValue: boolean
  match: Match | null
  tournamentDirectorId?: string
  onMatchUpdate?: () => Promise<void>
}

const props = defineProps<Props>()
const emit = defineEmits(['update:modelValue', 'match-updated'])

const authStore = useAuthStore()

// Refs
const showDialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const showTimeEdit = ref(false)
const showTeamEdit = ref(false)
const editedStartTime = ref('')
const newTeam1 = ref('')
const newTeam2 = ref('')
const availableTeams = ref([])
const loadingTeams = ref(false)
const teamForm = ref(null)
const editError = ref('')
const scoreUpdateError = ref('')

// Computed
const canEdit = computed(() => {
  return authStore.isAuthenticated &&
    (authStore.userRole === 'admin' || props.tournamentDirectorId === authStore.userId)
})

// Methods
const closeDialog = () => {
  showDialog.value = false
}

const extractErrorMessage = async (response: Response) => {
  try {
    const responseClone = response.clone()
    const text = await responseClone.text()
    const data = JSON.parse(text)

    if (data.detail && Array.isArray(data.detail) && data.detail.length > 0) {
      return data.detail[0].msg
    }

    if (data.detail && typeof data.detail === 'string') {
      return data.detail
    }

    return 'An error occurred'
  } catch (e) {
    console.error('Error extracting message:', e)
    return 'An error occurred'
  }
}

// Match score update
const handleScoreIncrement = async (team: 'team1' | 'team2') => {
  if (!props.match) return
  try {
    scoreUpdateError.value = ''
    const response = await fetch(
      `${API_URL}/matches/${props.match.id}/team-scores?team_to_upvote_score=${team}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    if (!response.ok) {
      const error = await extractErrorMessage(response)
      scoreUpdateError.value = error
      return
    }

    if (props.onMatchUpdate) {
      await props.onMatchUpdate()
    }

  } catch (e) {
    console.error('Error updating score:', e)
    scoreUpdateError.value = 'An unexpected error occurred while updating the score'
  }
}

// Time edit
const openTimeEdit = () => {
  if (!props.match) return
  editedStartTime.value = props.match.start_time
  showTimeEdit.value = true
}

const updateTime = async () => {
  try {
    editError.value = ''
    if (!props.match) return

    const response = await fetch(
      `${API_URL}/matches/${props.match.id}?start_time=${encodeURIComponent(editedStartTime.value)}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      }
    )

    if (!response.ok) {
      editError.value = await extractErrorMessage(response)
      return
    }

    if (props.onMatchUpdate) {
      await props.onMatchUpdate()
    }
    showTimeEdit.value = false
  } catch (e) {
    editError.value = 'Failed to update match time'
  }
}

// Team edit
const openTeamEdit = async () => {
  try {
    loadingTeams.value = true
    const response = await fetch(`${API_URL}/teams/?is_available=true`)
    if (!response.ok) throw new Error('Failed to load teams')
    const data = await response.json()
    availableTeams.value = data

    if (props.match) {
      const team1 = availableTeams.value.find(t => t.name === props.match?.team1_name)
      const team2 = availableTeams.value.find(t => t.name === props.match?.team2_name)

      newTeam1.value = team1?.id || ''
      newTeam2.value = team2?.id || ''
    }

    showTeamEdit.value = true
  } catch (e) {
    console.error('Error fetching teams:', e)
    editError.value = 'Failed to load teams'
  } finally {
    loadingTeams.value = false
  }
}

const updateTeams = async () => {
  if (!props.match) return

  try {
    editError.value = ''
    let params = new URLSearchParams()

    if (newTeam1.value) {
      const team1 = availableTeams.value.find(t => t.id === newTeam1.value)
      if (team1) {
        params.append('team1_name', team1.name)
      }
    }

    if (newTeam2.value) {
      const team2 = availableTeams.value.find(t => t.id === newTeam2.value)
      if (team2) {
        params.append('team2_name', team2.name)
      }
    }

    if (params.toString()) {
      const response = await fetch(
        `${API_URL}/matches/${props.match.id}?${params.toString()}`,
        {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        }
      )

      if (!response.ok) {
        const error = await extractErrorMessage(response)
        throw new Error(error)
      }

      if (props.onMatchUpdate) {
        await props.onMatchUpdate()
      }

      showTeamEdit.value = false
    }
  } catch (e) {
    console.error('Error updating teams:', e)
    editError.value = e.message || 'Failed to update teams'
  }
}
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
  padding-top: 100px;
  min-height: 100vh;
  width: 100vw !important;
}

.tournament-header-card {
  background: rgba(45, 55, 75, 0.7);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  margin-bottom: 24px;
  width: 80%;
  max-width: 1000px;
  justify-self: center;
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
  font-weight: 700;
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

.tournament-content-wrapper {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.tournament-header-card {
  background: rgba(45, 55, 75, 0.4);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  margin-bottom: 24px;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
}


.teams-card {
  background: rgba(45, 55, 75, 0.4);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
}

.prizes-card {
  background: rgba(45, 55, 75, 0.4);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  margin-bottom: 24px;
}

.section-title {
  text-align: center;
  width: 100%;
  margin-bottom: 24px;
  color: #42DDF2FF;
  font-size: 1.4rem;
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
}

.winner-team:hover {
  background: transparent !important;
  transform: scale(1.2);
}

.brackets-card {
  background: rgba(45, 55, 75, 0.4);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px 10px;
  height: 100%;
  min-height: 600px;
}


.brackets-content {
  padding: 24px;
  height: auto;
  min-height: 500px;
  background: rgba(45, 55, 75, 0);
  border-radius: 12px;
  margin-top: 0px;
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

.match-card {
  height: 250px;
  /* remove position: fixed */
  border-radius: 15px;
  overflow: hidden;
  background: rgba(45, 55, 75, 0);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  padding: 20px;
}

.match-card:hover {
  transform: translateY(-2px);
  border-color: #42DDF2FF;
  box-shadow: 0 4px 8px rgba(8, 117, 176, 0.2);
  cursor: pointer;
}

.match-card.match-finished {
  border: 2px solid #FED854FF !important;  /* Добавяме !important */
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.2);
}

.match-card.match-finished:hover {
  border-color: #FED854FF !important;
  box-shadow: 0 0 20px rgba(254, 216, 84, 0.3);
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
  justify-content: center;
  align-items: center;
  width: 100%;
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

.winner-text.pending {
  color: #808080;
  font-style: italic;
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

.stage-name {
  color: #42DDF2FF;
  font-size: 1.6rem;
  text-align: center;
  margin-bottom: 24px;
}

.prize-item {
  padding: 12px;
  margin-bottom: 8px;
}

.section-title {
  margin-bottom: 16px;
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

.custom-dialog-card .v-btn:hover {
  background: rgba(66, 221, 242, 0.1) !important;
  transform: translateY(-2px);
}

.match-details-centered {
  text-align: center;
  display: flex;
  flex-direction: column;
}

.tournament-title {
  color: #42DDF2FF;
  font-size: 1.6rem;
  font-weight: bold;
  margin-top: -30px;
  align-self: center;
}

.tournament-stage {
  color: #FED854FF;
  font-size: 1.2rem;
}

.is-finished {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  margin-bottom: 8px;
}

.custom-dialog-card .match-layout {
  display: flex;
  justify-content: center;
  align-items: center; /* Важно за вертикалното подравняване */
  gap: 32px;
  margin: 24px 0;
  min-height: 150px; /* Осигуряваме достатъчно пространство */
}

.custom-dialog-card .team-info-left, .team-info-right {
  display: flex;
  align-items: center; /* Променяме от column на center */
  gap: 16px;
  height: 150px; /* Фиксирана височина */
}

.custom-dialog-card .score-container {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 48px;
}

.custom-dialog-card .score-divider {
  margin: 0 20px;
  font-size: 2.5rem;
  color: #FED854FF;
  text-shadow: 0 0 10px rgba(238, 173, 60, 0.5);
  align-self: center;
  padding-bottom: 10px;
}

.edit-container {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  padding: 4px 25px;
  border-radius: 50px;
  transition: all 0.2s;
}

.edit-container:hover {
  background: rgba(66, 221, 242, 0.1);
}

.edit-text {
  font-size: 0.8rem;
  color: #42DDF2FF;
  opacity: 0.8;
}

.edit-container:hover .edit-text {
  opacity: 1;
}

.winner {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
}

.winner-name {
  color: #FED854FF;
  font-size: 1.2rem;
  font-weight: bold;
}

.score-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.team-score.clickable {
  cursor: pointer;
  transition: all 0.2s;
}

.team-score.clickable:hover {
  color: #42DDF2FF;
  text-shadow: 0 0 15px rgba(66, 221, 242, 0.5);
  transform: scale(1.1);
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


.dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
}

.dialog-content {
  padding: 24px;
}

.dialog-title {
  color: #42ddf2;
  font-weight: bold;
  font-size: 1.25rem;
  text-align: center;
}

.matches-history {
  padding: 20px;
}

.stage-section {
  margin-bottom: 40px;
}

.stage-subtitle {
  color: #FED854FF;
  font-size: 1.2rem;
  margin-bottom: 20px;
  padding-left: 16px;
  border-left: 3px solid #FED854FF;
}

.loading-matches, .matches-error {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  color: #42DDF2FF;
}

.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

@media (max-width: 768px) {
  .matches-grid {
    grid-template-columns: 1fr;
  }
}

.error-alert {
  width: 100%;
  margin: 0 auto;
  background-color: rgba(255, 215, 0, 0.12) !important;
  color: #ffd700 !important;
  border-color: #ffd700 !important;
  border-radius: 8px;
}

.error-alert :deep(.v-alert__close-button) {
  color: #ffd700 !important;
}

.error-alert :deep(.v-alert__prepend) {
  color: #ffd700 !important;
}
</style>
