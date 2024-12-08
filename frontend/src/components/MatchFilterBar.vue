<template>
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
</template>

<script setup lang="ts">
import { ref, watch, defineEmits, defineProps } from 'vue'
import type { FilterOption } from '@/types/types'

const props = defineProps<{
  teams: FilterOption[]
}>()

const emit = defineEmits(['update:stage', 'update:status', 'update:team'])

const selectedStage = ref<string | null>(null)
const selectedIsFinished = ref<string | null>(null)
const selectedTeam = ref<string | null>(null)

watch(selectedStage, (newValue) => {
  emit('update:stage', newValue)
})

watch(selectedIsFinished, (newValue) => {
  emit('update:status', newValue)
})

watch(selectedTeam, (newValue) => {
  emit('update:team', newValue)
})

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
</script>

<style scoped>
/* Filter row styling */
.filter-row {
  display: flex;
  justify-content: center;
  margin-bottom: 8px;
}

.filter-row .v-col {
  max-width: 300px;
}

/* Custom deep selectors for Vuetify components */
:deep(.v-card-title) {
  color: #42DDF2FF !important;
}
</style>
