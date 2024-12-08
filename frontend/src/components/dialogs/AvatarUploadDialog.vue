<template>
  <v-dialog v-model="showAvatarDialog" max-width="500">
    <v-card class="edit-dialog">
      <v-card-title>Update Avatar</v-card-title>
      <v-card-text>
        <v-alert
          v-if="avatarError"
          type="error"
          variant="tonal"
          class="mb-4"
        >
          {{ avatarError }}
        </v-alert>

        <v-file-input
          v-model="avatarFile"
          accept="image/*"
          label="Choose avatar"
          prepend-icon="mdi-camera"
          variant="outlined"
          @change="handleAvatarPreview"
        ></v-file-input>

        <div v-if="avatarPreview" class="avatar-preview">
          <img :src="avatarPreview" alt="Avatar preview" />
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
        class="cancel-btn"
        @click="closeDialog"
      >
        Cancel
      </v-btn>
      <v-btn
        class="submit-btn"
        @click="uploadAvatar"
        :loading="isUploading"
        :disabled="!avatarFile"
      >
        Upload
      </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { API_URL } from '@/config'
import type { Player } from '@/types/types'

const props = defineProps<{
  modelValue: boolean
  player: Player | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'avatar-updated'): void
}>()

const authStore = useAuthStore()
const avatarFile = ref<File | null>(null)
const avatarPreview = ref<string | null>(null)
const avatarError = ref('')
const isUploading = ref(false)

const showAvatarDialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const handleAvatarPreview = (file: File) => {
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    avatarPreview.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
}

const closeDialog = () => {
  showAvatarDialog.value = false
  avatarFile.value = null
  avatarPreview.value = null
  avatarError.value = ''
}

const uploadAvatar = async () => {
  if (!props.player || !avatarFile.value) return

  try {
    isUploading.value = true
    avatarError.value = ''

    const formData = new FormData()
    formData.append('avatar', avatarFile.value)

    const response = await fetch(`${API_URL}/players/${props.player.id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      },
      body: formData
    })

    if (!response.ok) {
      const errorData = await response.json()
      avatarError.value = errorData.detail || 'Failed to upload avatar'
      throw new Error(avatarError.value)
    }

    showAvatarDialog.value = false
    emit('avatar-updated')
  } catch (e) {
    console.error('Upload error:', e)
    if (!avatarError.value) {
      avatarError.value = 'Failed to upload avatar'
    }
  } finally {
    isUploading.value = false
  }
}
</script>

<style scoped>
/* Dialog base styles */
.edit-dialog, .dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
}

/* Avatar preview */
.avatar-preview {
  margin-top: 16px;
  text-align: center;
}

.avatar-preview img {
  max-width: 200px;
  border-radius: 50%;
  border: 2px solid #42DDF2FF;
}

/* Common layout */
.dialog-content {
  padding: 24px;
}

.dialog-actions {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: -32px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

/* Buttons */
.cancel-btn, .submit-btn {
  border-radius: 50px !important;
  padding: 0 24px !important;
  height: 40px !important;
  text-transform: none !important;
}

.cancel-btn {
  background: transparent !important;
  color: #42DDF2FF !important;
  border: 2px solid #42DDF2FF !important;
}

.cancel-btn:hover {
  background: rgba(66, 221, 242, 0.1) !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
}

.submit-btn:hover {
  background: #FED854FF !important;
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.3);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: rgba(66, 221, 242, 0.5) !important;
}

/* Error message */
.error-message {
  text-align: center;
  color: #fed854;
  padding: 16px;
}

/* Deep selectors for Vuetify components */
:deep(.v-card-title) {
  color: #42DDF2FF !important;
  font-size: 1.4rem;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(66, 221, 242, 0.2);
}

:deep(.v-card-text) {
  padding: 24px;
}

:deep(.v-card-actions) {
  padding: 16px 24px;
  border-top: 1px solid rgba(66, 221, 242, 0.2);
}

:deep(.v-text-field) {
  margin-top: 24px;
}

/* Input fields */
:deep(.v-field),
:deep(.v-field__input),
:deep(.v-text-field input),
:deep(.v-select .v-field__input) {
  color: white !important;
}

:deep(.v-field__outline) {
  color: rgba(66, 221, 242, 0.3) !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

/* Alerts */
:deep(.v-alert) {
  background-color: rgba(254, 216, 84, 0.1) !important;
  color: #fed854 !important;
  border-color: #fed854 !important;
}

:deep(.v-alert__close-button),
:deep(.v-alert__prepend) {
  color: #fed854 !important;
}

/* Error states */
:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
  display: block !important;
}

:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline) {
  color: #fed854 !important;
}

/* Icon colors */
:deep(.v-icon),
.detail-icon {
  color: rgba(255, 255, 255, 0.7) !important;
}

.detail-icon {
  color: #42DDF2FF !important;
}
</style>
