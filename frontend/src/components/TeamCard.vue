<template>
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
                size="40"
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
        VIEW DETAILS
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import type { Player, Team } from '@/types/types'

interface Props {
  team: Team
}
const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  (e: 'player-click', playerId: string): void
}>()

// Methods
const handlePlayerClick = (playerId: string) => {
  emit('player-click', playerId)
}
</script>

<style scoped>

.team-card {
  height: 450px;
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  background: rgba(45, 55, 75, 0.4);
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  width: 500px;
}

.team-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0 20px rgba(8, 117, 176, 0.4);
}

.team-content {
  position: relative;
  z-index: 3;
  height: 100%;
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.team-header {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.team-left-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.team-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.team-title {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.5rem;
  margin: 0;
  font-weight: 600;
  font-family: Orbitron, sans-serif;
  text-align: center;
}

.team-avatar {
  width: 80px;
  height: 80px;
  border: 2px solid #42ddf2;
  background: rgba(8, 87, 144, 0.1);
  margin-bottom: 8px;
}

.player-info p {
  margin: 4px 0;
}

.players-avatars {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  align-items: center;
  width: 260px;
  height: 110px;
  padding: 8px;
  border-radius: 12px;
  border: 2px solid rgba(66, 221, 242, 0.2);
}

.player-avatar {
  width: 50px;
  height: 40px;
  border: 1px solid rgba(66, 221, 242, 0.3);
  background: rgba(8, 87, 144, 0.1);
  transition: all 0.2s ease;
  cursor: pointer;
}

.player-avatar:hover {
  transform: scale(1.5);
}

.team-right-section {
  width: 100%;
  padding: 16px 0;
}

.progress-wrapper {
  position: relative;
  width: 60%;
  display: flex;
  align-items: center;
  justify-self: center;
  gap: 12px;
  padding: 8px 0;
  margin-top: -15px;
}

.progress-bar {
  flex-grow: 1;
  border-radius: 8px;
  overflow: hidden;
  background: rgba(8, 87, 144, 0.2);
}

.win-ratio {
  color: #42ddf2;
  font-size: 1rem;
  font-weight: 500;
  min-width: 45px;
}

.view-details-btn {
  margin-top: auto;
  color: #42DDF2FF !important;
  border-color: #42DDF2FF !important;
  border-radius: 50px;
  width: 60%;
  align-self: center;
}

.view-details-btn:hover {
  color: #42DDF2FF !important;
  background: rgba(66, 221, 242, 0.1);
}
</style>
