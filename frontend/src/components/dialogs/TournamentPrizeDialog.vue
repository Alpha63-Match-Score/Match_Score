<template>
  <v-dialog
    :modelValue="modelValue"
    @update:modelValue="$emit('update:modelValue', $event)"
    max-width="500px"
  >
    <v-card class="dialog-card">
      <div class="dialog-content">
        <v-card-title class="dialog-title">Edit Prize Pool</v-card-title>
        <v-card-text>
          <v-alert
            v-if="prizeError"
            type="error"
            variant="tonal"
            class="mb-4 error-alert"
            closable
            @click:close="prizeError = ''"
          >
            {{ prizeError }}
          </v-alert>
          <v-text-field
            v-model="editedPrizePool"
            label="Prize Pool (Kitty Kibbles)"
            type="number"
            variant="outlined"
            :error="!!prizeError"
            :error-messages="prizeError"
          ></v-text-field>
        </v-card-text>
        <v-card-actions class="dialog-actions">
          <v-spacer></v-spacer>
          <v-btn
            class="cancel-btn"
            variant="text"
            @click="$emit('update:modelValue', false)"
          >
            Cancel
          </v-btn>
          <v-btn
            class="submit-btn"
            @click="updatePrizePool"
            :disabled="!editedPrizePool"
          >
            Save
          </v-btn>
        </v-card-actions>
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Props {
  modelValue: boolean
  currentPrizePool: number
  error?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'save', newPrizePool: number): void
}>()

const editedPrizePool = ref(props.currentPrizePool)
const prizeError = ref('')

watch(() => props.currentPrizePool, (newValue) => {
  editedPrizePool.value = newValue
})

watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    editedPrizePool.value = props.currentPrizePool
  }
})

watch(() => props.error, (newError) => {
  if (newError) {
    prizeError.value = newError
  }
})

const updatePrizePool = () => {
  const prizePool = Number(editedPrizePool.value)

  if (!prizePool || prizePool <= 0) {
    prizeError.value = 'Prize pool must be a positive number'
    return
  }

  emit('save', prizePool)
}
</script>

<style scoped>
.dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
  border-radius: 12px;
}

.dialog-content {
  padding: 24px;
}

.dialog-title {
  color: #42ddf2;
  font-size: 1.4rem;
  font-weight: 500;
  text-align: center;
  margin-bottom: 16px;
}

.dialog-actions {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: -32px;
}

/* Button Styles */
.cancel-btn {
  color: #42DDF2FF !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  margin-left: 16px;
}

/* Error Alert */
.error-alert {
  width: 100%;
  margin: 0 auto;
  background-color: rgba(255, 215, 0, 0.12) !important;
  color: #ffd700 !important;
  border-color: #ffd700 !important;
  border-radius: 8px;
}

.error-alert :deep(.v-alert__close-button),
.error-alert :deep(.v-alert__prepend) {
  color: #ffd700 !important;
}

/* Vuetify Field Overrides */
:deep(.v-field) {
  background: rgba(45, 55, 75, 0.8) !important;
}

:deep(.v-field__input),
:deep(.v-input input) {
  color: white !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
}

/* Error State Styles */
:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline),
:deep(.v-field--error .v-label),
:deep(.v-field--error input::placeholder),
:deep(.v-field--error .v-field__outline__start),
:deep(.v-field--error .v-field__outline__end),
:deep(.v-field--error .v-field__outline__notch) {
  border-color: #fed854 !important;
  color: #fed854 !important;
}

:deep(.v-field__outline) {
  color: rgba(66, 221, 242, 0.3) !important;
}
</style>
