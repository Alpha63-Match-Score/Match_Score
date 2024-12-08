<template>
  <v-dialog v-model="showAddTournamentDialog" max-width="500">
    <v-card class="dialog-card">
      <div class="dialog-content">
        <v-card-title class="dialog-title">
          <span>{{ currentStep === 1 ? 'Tournament Details' : 'Select Teams' }}</span>
        </v-card-title>

        <v-card-text>
          <!-- Error Alert -->
          <v-alert
            v-if="tournamentError"
            type="error"
            variant="tonal"
            closable
            class="mb-4"
          >
            {{ tournamentError }}
          </v-alert>

          <!-- Step 1: Tournament Details -->
          <v-form v-if="currentStep === 1" ref="form">
            <v-text-field
              v-model="tournamentTitle"
              label="Tournament Title"
              variant="outlined"
              :rules="[rules.required, rules.minLength]"
              :error-messages="titleError"
            ></v-text-field>

            <v-select
              v-model="tournamentFormat"
              :items="formattedFormatOptions"
              label="Tournament Format"
              variant="outlined"
              :rules="[rules.required]"
              class="format-select"
            ></v-select>

            <v-text-field
              v-model="tournamentStartDate"
              label="Start Date"
              type="datetime-local"
              variant="outlined"
              :rules="[rules.required]"
              :error-messages="dateError"
            ></v-text-field>

            <v-text-field
              v-model="tournamentPrizePool"
              label="Prize Pool (Kitty Kibbles)"
              variant="outlined"
              type="number"
              :rules="[rules.required, rules.minPrize]"
            ></v-text-field>
          </v-form>

          <!-- Step 2: Team Selection -->
          <v-form v-else ref="teamForm">
            <div class="team-slot" v-for="index in getMaxTeams" :key="index">
              <div class="d-flex align-center">
                <v-autocomplete
                  v-if="!isCustomTeam[index - 1]"
                  v-model="selectedTeams[index - 1]"
                  :items="getAvailableTeamsForSlot(index - 1)"
                  item-title="name"
                  item-value="id"
                  :label="`Team ${index}`"
                  variant="outlined"
                  :loading="loadingTeams"
                  clearable
                  class="flex-grow-1 custom-autocomplete"
                  :rules="getTeamRules(index - 1)"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :title="item.raw.name"
                      class="team-list-item"
                    ></v-list-item>
                  </template>
                </v-autocomplete>

                <v-text-field
                  v-else
                  v-model="customTeamNames[index - 1]"
                  :label="`Custom Team ${index}`"
                  variant="outlined"
                  class="flex-grow-1"
                  :rules="getTeamRules(index - 1)"
                ></v-text-field>

                <v-btn
                  icon
                  class="custom-toggle-btn ml-2"
                  @click="toggleCustomTeam(index - 1)"
                  :title="isCustomTeam[index - 1] ? 'Switch to existing teams' : 'Add custom team'"
                  variant="outlined"
                >
                  <v-icon size="20">
                    {{ isCustomTeam[index - 1] ? 'mdi-format-list-bulleted' : 'mdi-plus' }}
                  </v-icon>
                </v-btn>
              </div>
            </div>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="cancel-btn" @click="handleCancel">
            Cancel
          </v-btn>
          <v-btn
            v-if="currentStep === 1"
            class="next-btn"
            @click="handleNext"
            :disabled="!canProceedToTeams"
          >
            Next
          </v-btn>
          <v-btn
            v-else
            class="submit-btn"
            @click="submitTournament"
            :loading="isSubmitting"
            :disabled="!canSubmit"
          >
            Create Tournament
          </v-btn>
        </v-card-actions>
      </div>
    </v-card>
  </v-dialog>
</template>


<script setup lang="ts">
import {ref, computed, onMounted} from "vue";
import { useAuthStore } from '@/stores/auth'
import { API_URL } from '@/config'

// Auth Store
const authStore = useAuthStore()

// Props & Emits
const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'tournament-added'])

// Computed
const showAddTournamentDialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// State
const teamForm = ref(null)
const isSubmitting = ref(false)
const tournamentTitle = ref('')
const tournamentFormat = ref('')
const tournamentStartDate = ref('')
const tournamentPrizePool = ref('')
const selectedTeams = ref<Array<string | null>>(Array(8).fill(null))
const teams = ref([])
const customInputs = ref(Array(8).fill(''))
const isCustomTeam = ref(Array(8).fill(false))
const customTeamNames = ref(Array(8).fill(''))
const currentStep = ref(1)
const loadingTeams = ref(false)
const form = ref(null)


// Errors
const tournamentError = ref('')
const titleError = ref('')
const dateError = ref('')

// Validation Rules
const rules = {
  required: (v: string) => !!v || 'This field is required',
  minLength: (v: string) => v.length >= 3 || 'Title must be at least 3 characters',
  minPrize: (v: number) => v >= 1 || 'Prize pool must be at least 1 Kitty Kibble',
}

const formattedFormatOptions = [
  { title: 'Single Elimination', value: 'single elimination' },
  { title: 'Round Robin', value: 'round robin' },
  { title: 'One-Off Match', value: 'one off match' }
]

// Methods
const resetForm = () => {
  currentStep.value = 1
  tournamentTitle.value = ''
  tournamentFormat.value = ''
  tournamentStartDate.value = ''
  tournamentPrizePool.value = ''
  selectedTeams.value = Array(8).fill(null)
  customInputs.value = Array(8).fill('')
  isCustomTeam.value = Array(8).fill(false)
  customTeamNames.value = Array(8).fill('')
  tournamentError.value = ''
  titleError.value = ''
  dateError.value = ''
}

const getMaxTeams = computed(() => {
  const formatTeamCounts = {
    'single elimination': 8,
    'round robin': 5,
    'one off match': 2
  }
  return formatTeamCounts[tournamentFormat.value] || 0
})

const canProceedToTeams = computed(() => {
  return tournamentTitle.value.length >= 3 &&
         tournamentFormat.value &&
         tournamentStartDate.value &&
         tournamentPrizePool.value >= 1
})

const canSubmit = computed(() => {
  const requiredTeams = {
    'single elimination': 4,
    'round robin': 4,
    'one off match': 2
  }

  const validTeamsCount = selectedTeams.value.reduce((count, team, index) => {
    if (isCustomTeam.value[index]) {
      return customTeamNames.value[index]?.trim() ? count + 1 : count
    } else {
      return team ? count + 1 : count
    }
  }, 0)

  return validTeamsCount >= requiredTeams[tournamentFormat.value]
})

const getAvailableTeamsForSlot = (currentIndex: number) => {
  return teams.value.filter(team => {
    return !selectedTeams.value.some(
      (selectedId, index) => selectedId === team.id && index !== currentIndex
    )
  })
}

const getTeamRules = (index: number) => {
  if (tournamentFormat.value === 'single elimination') {
    return index < 4 ? [rules.required] : []
  } else if (tournamentFormat.value === 'round robin') {
    return index < 4 ? [rules.required] : []
  } else if (tournamentFormat.value === 'one off match') {
    return index < 2 ? [rules.required] : []
  }

  return []
}

const toggleCustomTeam = (index: number) => {
  isCustomTeam.value[index] = !isCustomTeam.value[index]
  if (!isCustomTeam.value[index]) {
    customTeamNames.value[index] = ''
  } else {
    selectedTeams.value[index] = null
  }
}

const handleCancel = () => {
  showAddTournamentDialog.value = false
  resetForm()
}

const handleNext = async () => {
  if (!form.value) return

  titleError.value = ''
  dateError.value = ''
  tournamentError.value = ''
  let hasErrors = false

  try {
    const response = await fetch(`${API_URL}/tournaments?search=${encodeURIComponent(tournamentTitle.value)}`)
    const tournaments = await response.json()
    if (tournaments.some(t => t.title.toLowerCase() === tournamentTitle.value.toLowerCase())) {
      titleError.value = 'A tournament with this name already exists'
      hasErrors = true
    }
  } catch (e) {
    console.error('Error checking tournament title:', e)
  }

  const selectedDate = new Date(tournamentStartDate.value)
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  tomorrow.setHours(selectedDate.getHours(), selectedDate.getMinutes(), selectedDate.getSeconds())
  const now = new Date()

  if (selectedDate < now) {
    dateError.value = 'Tournament start date cannot be in the past'
    hasErrors = true
  } if (selectedDate <= tomorrow) {
    dateError.value = 'Start date must be at least 1 day in the future'
    hasErrors = true
  }
  if (hasErrors) return

  try {
    loadingTeams.value = true
    const response = await fetch(`${API_URL}/teams?is_available=true&offset=0&limit=100`)
    if (!response.ok) throw new Error('Failed to load teams')
    const data = await response.json()
    teams.value = data
  } catch (e) {
    console.error('Error fetching teams:', e)
    tournamentError.value = 'Failed to load teams. Please try again.'
    return
  } finally {
    loadingTeams.value = false
  }

  const { valid } = await form.value.validate()
  if (!valid) return

  currentStep.value = 2
}

const submitTournament = async () => {
  console.log('Starting tournament submission...')
  if (!teamForm.value) return
  const { valid } = await teamForm.value.validate()
  if (!valid) return

  try {
    isSubmitting.value = true
    tournamentError.value = ''

    const formattedDate = new Date(tournamentStartDate.value).toISOString()

    const teamNames = selectedTeams.value.map((selectedTeam, index) => {
      if (isCustomTeam.value[index]) {
        return customTeamNames.value[index]
      }
      const existingTeam = teams.value.find(t => t.id === selectedTeam)
      return existingTeam?.name || ''
    }).filter(name => name !== '')

    console.log('Final team names for submission:', teamNames)

    const params = new URLSearchParams({
      title: tournamentTitle.value,
      tournament_format: tournamentFormat.value,
      start_date: formattedDate,
      prize_pool: tournamentPrizePool.value.toString()
    })

    const response = await fetch(`${API_URL}/tournaments/?${params.toString()}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(teamNames)
    })

    if (!response.ok) {
      const errorData = await response.json()
      if (errorData.detail && Array.isArray(errorData.detail)) {
        const errorMessages = errorData.detail.map((err: any) => {
          return `${err.msg} (${err.loc.join('.')})`
        })
        throw new Error(errorMessages.join('\n'))
      } else {
        throw new Error(errorData.detail || 'Unknown error occurred')
      }
    }

    showAddTournamentDialog.value = false
    const newTournament = await response.json()
    emit('tournament-added', newTournament)
    resetForm()

  } catch (e) {
    console.error('Full error:', e)
    tournamentError.value = e.message
  } finally {
    isSubmitting.value = false
  }
}

const fetchTeams = async () => {
  try {
    loadingTeams.value = true
    const response = await fetch(`${API_URL}/teams?is_available=true&offset=0&limit=100`)
    if (!response.ok) throw new Error('Failed to fetch teams')
    teams.value = await response.json()
  } catch (e) {
    console.error('Error fetching teams:', e)
  } finally {
    loadingTeams.value = false
  }
}

onMounted(async () => {
  await fetchTeams()
})
</script>

<style scoped>
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


.file-upload-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-bottom: 8px;
}

.preview-avatar {
  border: 2px solid #42DDF2FF;
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s;
}

.preview-avatar:hover {
  transform: scale(1.05);
}

.upload-input {
  width: 100%;
}


.team-list-item {
  padding: 8px 16px;
  transition: background-color 0.2s;
  border-radius: 4px;
  margin: 2px 0;
}

.team-list-item:hover {
  background: rgba(66, 221, 242, 0.1);
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

:deep(.v-messages) {
  min-height: 14px;
  padding-top: 2px;
  display: block !important;
}

:deep(.v-text-field) {
  margin-top: 16px;
}

:deep(.v-field__input input) {
  color: white !important;
  -webkit-text-fill-color: white !important;
}

:deep(.v-field__input input::selection) {
  background-color: rgba(66, 221, 242, 0.3) !important;
  color: white !important;
}

:deep(.v-field__input input::-moz-selection) {
  background-color: rgba(66, 221, 242, 0.3) !important;
  color: white !important;
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

.dialog-actions {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.cancel-btn {
  color: #42DDF2FF !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  margin-left: 16px;
}

.upload-input {
  width: 100%;
}

.preview-avatar .v-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

:deep(.v-field__input) {
  color: white !important;
}

:deep(.v-file-input .v-field) {
  border-color: rgba(66, 221, 242, 0.3) !important;
}

:deep(.v-file-input .v-field:hover) {
  border-color: #42ddf2 !important;
}

.dialog-content .v-card-text > div > * {
  margin-top: 0 !important;
}

:deep(.teams-menu) {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 1px solid rgba(66, 221, 242, 0.3);
  max-height: 300px !important;
  overflow-y: auto;
}

:deep(.teams-menu::-webkit-scrollbar) {
  width: 8px;
}

:deep(.teams-menu::-webkit-scrollbar-track) {
  background: transparent;
}

:deep(.teams-menu::-webkit-scrollbar-thumb) {
  background: rgba(66, 221, 242, 0.3);
  border-radius: 4px;
}

:deep(.teams-menu::-webkit-scrollbar-thumb:hover) {
  background: rgba(66, 221, 242, 0.5);
}

:deep(.v-select__selection) {
  color: white !important;
  opacity: 1 !important;
}

:deep(.v-select .v-field__input) {
  min-height: 56px !important;
  opacity: 1 !important;
  color: white !important;
}

:deep(.v-select .v-field) {
  background: transparent !important;
}

:deep(.v-overlay__content) {
  scrollbar-width: thin;
  scrollbar-color: rgba(66, 221, 242, 0.5) transparent;
}

:deep(.v-overlay__content::-webkit-scrollbar) {
  width: 8px;
}

:deep(.v-overlay__content::-webkit-scrollbar-track) {
  background: transparent;
}

:deep(.v-overlay__content::-webkit-scrollbar-thumb) {
  background-color: rgba(66, 221, 242, 0.5);
  border-radius: 4px;
}

:deep(.v-overlay__content::-webkit-scrollbar-thumb:hover) {
  background-color: rgba(66, 221, 242, 0.7);
}

.custom-autocomplete :deep(.v-field__input) {
  color: rgb(255, 255, 255) !important;
}

.custom-autocomplete :deep(.v-field--focused) {
  color: #42DDF2FF !important;
}


.dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 1px solid #42DDF2FF;
  backdrop-filter: blur(10px);
  border-radius: 12px;
}

.dialog-content {
  padding: 20px;
}

.dialog-actions {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: -32px;
}

.dialog-title {
  color: #42ddf2;
  font-size: 1.4rem;
  font-weight: 500;
  text-align: center;
  margin-bottom: 16px;
}

:deep(.v-card-text) {
  padding-bottom: 8px;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 14px;
}

:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

.error-message {
  color: #fed854;
  font-size: 0.9rem;
  margin-top: 8px;
  text-align: center;
}

.cancel-btn {
  color: #42DDF2FF !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  margin-left: 16px;
}

.team-slot {
  margin-bottom: 16px;
}

.team-slot .d-flex {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.team-slot .v-autocomplete,
.team-slot .v-text-field {
  flex: 1;
}

.team-list-item {
  padding: 8px 16px;
  transition: background-color 0.2s;
  border-radius: 4px;
  margin: 2px 0;
}

.team-list-item:hover {
  background: rgba(66, 221, 242, 0.1);
}

.team-list-item--selected {
  background: rgba(66, 221, 242, 0.15);
}

:deep(.v-autocomplete .v-field__input) {
  color: white !important;
  min-height: 56px;
}

:deep(.v-autocomplete .v-field__append-inner) {
  padding-top: 14px;
}

:deep(.v-list-item__content) {
  color: white;
}

:deep(.v-list) {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 1px solid rgba(66, 221, 242, 0.3);
}

:deep(.v-select) {
  background: transparent !important;
}

:deep(.v-text-field),
:deep(.v-select) {
  margin-bottom: 16px;
}

:deep(.filter-select) {
  background: transparent !important;
  color: #ffffff !important;
  border-color: #42DDF2FF !important;
}

:deep(.v-select:focus),
:deep(.v-select--active) {
  background: transparent !important;
  border-color: #42DDF2FF !important;
}

:deep(.v-menu__content) {
  background: transparent !important;
  box-shadow: none !important;
}

:deep(.v-list-item) {
  background: transparent !important;
  color: #ffffff !important;
}

:deep(.v-list-item:hover) {
  background: rgba(66, 221, 242, 0.2) !important;
  color: #42DDF2FF !important;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
  display: block !important;
}

:deep(.v-input input) {
  color: white !important;
}

:deep(.v-field--variant-outlined.v-field--error) {
  border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline) {
  color: #fed854 !important;
}

:deep(.v-text-field .v-field--error) {
  --v-field-border-color: #fed854;
}

:deep(.v-field--error .v-label) {
  color: #FED854FF !important;
}

:deep(.v-field--error .v-field__outline__start),
:deep(.v-field--error .v-field__outline__end),
:deep(.v-field--error .v-field__outline__notch) {
  border-color: #fed854 !important;
}

:deep(.v-field--error input::placeholder),
:deep(.v-field--error .v-label.v-field-label) {
  color: #fed854 !important;
}

:deep(.v-field__outline) {
  color: rgba(66, 221, 242, 0.3) !important;
}

:deep(.v-file-input .v-field__input) {
  color: white !important;
  font-size: 0.9rem;
}

.format-select :deep(.v-select__selection) {
  color: white !important;
}

.team-slot {
  margin-bottom: 16px;
}

.team-slot .d-flex {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}


.custom-toggle-btn {
  margin-top: -22px !important;
  height: 48px !important;
  width: 48px !important;
  color: #42DDF2FF !important;
  border: 2px solid rgba(66, 221, 242, 0.3) !important;
  flex-shrink: 0;
}

.custom-toggle-btn:hover {
  border-color: #42DDF2FF !important;
  background: rgba(66, 221, 242, 0.1) !important;
}

.flex-grow-1 {
  flex-grow: 1;
}

.next-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
}

</style>
