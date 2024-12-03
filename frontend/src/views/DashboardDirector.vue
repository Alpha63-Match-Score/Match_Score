<!--<template>-->
<!--  <div class="home-wrapper">-->
<!--    &lt;!&ndash; Header с fade ефект &ndash;&gt;-->
<!--    <div class="header-image"></div>-->
<!--    <div class="header-overlay"></div>-->

<!--    <div class="content-wrapper">-->
<!--      <v-container>-->
<!--        &lt;!&ndash; Director Welcome Section &ndash;&gt;-->
<!--        <div class="welcome-card">-->
<!--          <div class="welcome-background"></div>-->
<!--          <div class="welcome-content">-->
<!--            <h2 class="welcome-text">Director Dashboard</h2>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; Actions Section &ndash;&gt;-->
<!--        <div class="actions-card">-->
<!--          <div class="actions-background"></div>-->
<!--          <div class="actions-content">-->
<!--            <h3 class="section-title">Available Actions</h3>-->
<!--            <div class="actions-buttons">-->
<!--              <v-btn-->
<!--                class="action-btn"-->
<!--                @click="showCreateTournamentDialog = true"-->
<!--              >-->
<!--                <v-icon left>mdi-trophy</v-icon>-->
<!--                Create Tournament-->
<!--              </v-btn>-->
<!--              <v-btn-->
<!--                class="action-btn"-->
<!--                @click="showUpdatePlayerDialog = true"-->
<!--              >-->
<!--                <v-icon left>mdi-account-edit</v-icon>-->
<!--                Update Player-->
<!--              </v-btn>-->
<!--            </div>-->

<!--            &lt;!&ndash; Display Error for Available Actions &ndash;&gt;-->
<!--            <div v-if="actionsError" class="error-message">-->
<!--              {{ actionsError }}-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; Tournaments Section &ndash;&gt;-->
<!--        <div class="history-card">-->
<!--          <div class="history-background"></div>-->
<!--          <div class="history-content">-->
<!--            <h3 class="section-title">My Tournaments</h3>-->

<!--            &lt;!&ndash; Loading state &ndash;&gt;-->
<!--            <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 200px">-->
<!--              <v-progress-circular indeterminate color="#42DDF2FF"></v-progress-circular>-->
<!--            </div>-->

<!--            &lt;!&ndash; Error state &ndash;&gt;-->
<!--            <div v-else-if="tournamentsError" class="error-message">-->
<!--              {{ tournamentsError }}-->
<!--            </div>-->

<!--            &lt;!&ndash; Tournaments list &ndash;&gt;-->
<!--            <div v-else-if="tournaments.length > 0" class="tournament-list">-->
<!--              <div v-for="tournament in tournaments" :key="tournament.id" class="tournament-item">-->
<!--                <div class="tournament-header">-->
<!--                  <div class="tournament-title">-->
<!--                    <v-icon class="tournament-icon">mdi-trophy</v-icon>-->
<!--                    {{ tournament.title }}-->
<!--                  </div>-->
<!--                  <div :class="['status-tag', `status-${getTournamentStatus(tournament)}`]">-->
<!--                    {{ formatStage(tournament.current_stage) }}-->
<!--                  </div>-->
<!--                </div>-->

<!--                <div class="tournament-details">-->
<!--                  <div class="detail-item">-->
<!--                    <v-icon small class="detail-icon">mdi-calendar</v-icon>-->
<!--                    {{ formatDate(tournament.start_date) }} - {{ formatDate(tournament.end_date) }}-->
<!--                  </div>-->
<!--                  <div class="detail-item">-->
<!--                    <v-icon small class="detail-icon">mdi-account-group</v-icon>-->
<!--                    Teams: {{ tournament.number_of_teams }}-->
<!--                  </div>-->
<!--                  <div class="detail-item">-->
<!--                    <v-icon small class="detail-icon">mdi-format-list-bulleted</v-icon>-->
<!--                    {{ formatTournamentFormat(tournament.tournament_format) }}-->
<!--                  </div>-->
<!--                  <v-btn-->
<!--                    small-->
<!--                    class="edit-btn"-->
<!--                    @click="openUpdateTournament(tournament)"-->
<!--                    :disabled="!canUpdateTournament(tournament)"-->
<!--                  >-->
<!--                    <v-icon left small>mdi-pencil</v-icon>-->
<!--                    Edit-->
<!--                  </v-btn>-->
<!--                </div>-->
<!--              </div>-->
<!--            </div>-->

<!--            &lt;!&ndash; Empty state &ndash;&gt;-->
<!--            <div v-else class="error-message">-->
<!--              No tournaments found. Start by creating a new tournament!-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->
<!--      </v-container>-->
<!--    </div>-->

<!--    &lt;!&ndash; Create Tournament Dialog &ndash;&gt;-->
<!--    <v-dialog v-model="showCreateTournamentDialog" max-width="600">-->
<!--      <v-card class="dialog-card">-->
<!--        <v-card-title class="dialog-title">Create New Tournament</v-card-title>-->
<!--        <v-card-text>-->
<!--          <v-form ref="createForm" @submit.prevent="submitCreateForm">-->
<!--            &lt;!&ndash; Title &ndash;&gt;-->
<!--            <v-text-field-->
<!--              v-model="createFormData.title"-->
<!--              label="Tournament Title"-->
<!--              :rules="[rules.required, rules.titleLength]"-->
<!--              outlined-->
<!--            ></v-text-field>-->

<!--            &lt;!&ndash; Tournament Format &ndash;&gt;-->
<!--            <v-select-->
<!--              v-model="createFormData.tournament_format"-->
<!--              label="Tournament Format"-->
<!--              :items="tournamentFormats"-->
<!--              outlined-->
<!--              :rules="[rules.required]"-->
<!--            ></v-select>-->

<!--            &lt;!&ndash; Start Date &ndash;&gt;-->
<!--            <v-menu-->
<!--              ref="startDateMenu"-->
<!--              v-model="startDateMenu"-->
<!--              :close-on-content-click="false"-->
<!--              transition="scale-transition"-->
<!--              offset-y-->
<!--              min-width="auto"-->
<!--            >-->
<!--              <template v-slot:activator="{ on, attrs }">-->
<!--                <v-text-field-->
<!--                  v-model="formattedStartDate"-->
<!--                  label="Start Date"-->
<!--                  readonly-->
<!--                  outlined-->
<!--                  v-bind="attrs"-->
<!--                  v-on="on"-->
<!--                  :rules="[rules.required, rules.futureDate]"-->
<!--                ></v-text-field>-->
<!--              </template>-->
<!--              <v-date-picker-->
<!--                v-model="createFormData.start_date"-->
<!--                :min="tomorrow"-->
<!--                @input="startDateMenu = false"-->
<!--              ></v-date-picker>-->
<!--            </v-menu>-->

<!--            &lt;!&ndash; Prize Pool &ndash;&gt;-->
<!--            <v-text-field-->
<!--              v-model.number="createFormData.prize_pool"-->
<!--              label="Prize Pool"-->
<!--              type="number"-->
<!--              outlined-->
<!--              :rules="[rules.required, rules.minPrize]"-->
<!--            ></v-text-field>-->

<!--            &lt;!&ndash; Team Names &ndash;&gt;-->
<!--            <v-card class="teams-card mt-4">-->
<!--              <v-card-title class="teams-title">Teams</v-card-title>-->
<!--              <v-card-text>-->
<!--                <div v-for="(team, index) in createFormData.team_names" :key="index" class="team-input">-->
<!--                  <v-text-field-->
<!--                    v-model="createFormData.team_names[index]"-->
<!--                    :label="`Team ${index + 1}`"-->
<!--                    outlined-->
<!--                    :rules="[rules.required]"-->
<!--                  >-->
<!--                    <template v-slot:append>-->
<!--                      <v-icon-->
<!--                        color="error"-->
<!--                        @click="removeTeam(index)"-->
<!--                        v-if="canRemoveTeams"-->
<!--                      >-->
<!--                        mdi-delete-->
<!--                      </v-icon>-->
<!--                    </template>-->
<!--                  </v-text-field>-->
<!--                </div>-->

<!--                <v-btn-->
<!--                  v-if="canAddTeams"-->
<!--                  block-->
<!--                  color="primary"-->
<!--                  outlined-->
<!--                  class="mt-2"-->
<!--                  @click="addTeam"-->
<!--                >-->
<!--                  Add Team-->
<!--                </v-btn>-->
<!--              </v-card-text>-->
<!--            </v-card>-->
<!--          </v-form>-->
<!--        </v-card-text>-->

<!--        <v-card-actions>-->
<!--          <v-spacer></v-spacer>-->
<!--          <v-btn-->
<!--            text-->
<!--            class="cancel-btn"-->
<!--            @click="showCreateTournamentDialog = false"-->
<!--            :disabled="isSubmitting"-->
<!--          >-->
<!--            Cancel-->
<!--          </v-btn>-->
<!--          <v-btn-->
<!--            color="primary"-->
<!--            class="submit-btn"-->
<!--            @click="submitCreateForm"-->
<!--            :loading="isSubmitting"-->
<!--            :disabled="isSubmitting"-->
<!--          >-->
<!--            Create Tournament-->
<!--          </v-btn>-->
<!--        </v-card-actions>-->
<!--      </v-card>-->
<!--    </v-dialog>-->

<!--    &lt;!&ndash; Update Tournament Dialog &ndash;&gt;-->
<!--    &lt;!&ndash; Подобен на Create диалога, но с по-малко полета &ndash;&gt;-->
<!--    <v-dialog v-model="showUpdateTournamentDialog" max-width="600">-->
<!--      &lt;!&ndash; Добави Update форма тук &ndash;&gt;-->
<!--    </v-dialog>-->

<!--    &lt;!&ndash; Update Player Dialog &ndash;&gt;-->
<!--    <v-dialog v-model="showUpdatePlayerDialog" max-width="500">-->
<!--      &lt;!&ndash; Добави Player форма тук &ndash;&gt;-->
<!--    </v-dialog>-->

<!--    &lt;!&ndash; Success Alert &ndash;&gt;-->
<!--    <v-snackbar-->
<!--      v-model="showSuccessAlert"-->
<!--      :timeout="3000"-->
<!--      color="success"-->
<!--    >-->
<!--      {{ successMessage }}-->
<!--      <template v-slot:action="{ attrs }">-->
<!--        <v-btn-->
<!--          text-->
<!--          v-bind="attrs"-->
<!--          @click="showSuccessAlert = false"-->
<!--        >-->
<!--          Close-->
<!--        </v-btn>-->
<!--      </template>-->
<!--    </v-snackbar>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--import { format, addDays } from 'date-fns'-->

<!--export default {-->
<!--  name: 'DirectorDashboard',-->

<!--  data() {-->
<!--    return {-->
<!--      tournaments: [],-->
<!--      isLoading: true,-->
<!--      isSubmitting: false,-->
<!--      tournamentsError: null,-->
<!--      actionsError: null,-->
<!--      createError: null,-->
<!--      updateError: null,-->
<!--      playerError: null,-->

<!--      // Dialog controls-->
<!--      showCreateTournamentDialog: false,-->
<!--      showUpdateTournamentDialog: false,-->
<!--      showUpdatePlayerDialog: false,-->
<!--      showSuccessAlert: false,-->
<!--      successMessage: '',-->

<!--      // Date pickers-->
<!--      startDateMenu: false,-->
<!--      endDateMenu: false,-->

<!--      // Form data-->
<!--      createFormData: {-->
<!--        title: '',-->
<!--        tournament_format: null,-->
<!--        start_date: '',-->
<!--        prize_pool: null,-->
<!--        team_names: ['', '']-->
<!--      },-->

<!--      // Tournament formats-->
<!--      tournamentFormats: [-->
<!--        { text: 'Single Elimination', value: 'SINGLE_ELIMINATION' },-->
<!--        { text: 'Round Robin', value: 'ROUND_ROBIN' },-->
<!--        { text: 'One Off Match', value: 'ONE_OFF_MATCH' }-->
<!--      ],-->

<!--      // Validation rules-->
<!--      rules: {-->
<!--        required: v => !!v || 'This field is required',-->
<!--        titleLength: v => (v && v.length >= 3 && v.length <= 50) || 'Title must be between 3 and 50 characters',-->
<!--        futureDate: v => {-->
<!--          if (!v) return true-->
<!--          const date = new Date(v)-->
<!--          const today = new Date()-->
<!--          return date > today || 'Start date must be in the future'-->
<!--        },-->
<!--        minPrize: v => !v || v >= 1 || 'Prize pool must be at least 1'-->
<!--      }-->
<!--    }-->
<!--  },-->

<!--  computed: {-->
<!--    tomorrow() {-->
<!--      return format(addDays(new Date(), 1), 'yyyy-MM-dd')-->
<!--    },-->

<!--    formattedStartDate() {-->
<!--      if (!this.createFormData.start_date) return ''-->
<!--      return format(new Date(this.createFormData.start_date), 'dd MMM yyyy')-->
<!--    },-->

<!--    canAddTeams() {-->
<!--      const format = this.createFormData.tournament_format-->
<!--      if (!format) return false-->

<!--      const currentCount = this.createFormData.team_names.length-->
<!--      if (format === 'ONE_OFF_MATCH') return currentCount < 2-->
<!--      if (format === 'ROUND_ROBIN') return currentCount < 5-->
<!--      return currentCount < 16 // SINGLE_ELIMINATION-->
<!--    },-->

<!--    canRemoveTeams() {-->
<!--      return this.createFormData.team_names.length > this.getMinTeams()-->
<!--    }-->
<!--  },-->

<!--  methods: {-->
<!--    formatDate(date) {-->
<!--      return format(new Date(date), 'dd MMM yyyy')-->
<!--    },-->

<!--    formatStage(stage) {-->
<!--      return stage.split('_').map(word =>-->
<!--        word.toLowerCase().charAt(0).toUpperCase() + word.toLowerCase().slice(1)-->
<!--      ).join(' ')-->
<!--    },-->

<!--    formatTournamentFormat(format) {-->
<!--      return format.split('_').map(word =>-->
<!--        word.toLowerCase().charAt(0).toUpperCase() + word.toLowerCase().slice(1)-->
<!--      ).join(' ')-->
<!--    },-->

<!--    getTournamentStatus(tournament) {-->
<!--      const now = new Date()-->
<!--      const startDate = new Date(tournament.start_date)-->
<!--      const endDate = new Date(tournament.end_date)-->

<!--      if (tournament.current_stage === 'FINISHED') return 'finished'-->
<!--      if (now < startDate) return 'pending'-->
<!--      if (now >= startDate && now <= endDate) return 'active'-->
<!--      return 'finished'-->
<!--    },-->

<!--    canUpdateTournament(tournament) {-->
<!--      return this.getTournamentStatus(tournament) !== 'finished'-->
<!--    },-->

<!--    getMinTeams() {-->
<!--      const format = this.createFormData.tournament_format-->
<!--      if (format === 'ONE_OFF_MATCH') return 2-->
<!--      if (format === 'ROUND_ROBIN') return 4-->
<!--      return 4 // SINGLE_ELIMINATION-->
<!--    },-->

<!--    addTeam() {-->
<!--      this.createFormData.team_names.push('')-->
<!--    },-->

<!--    removeTeam(index) {-->
<!--      this.createFormData.team_names.splice(index, 1)-->
<!--    },-->

<!--    async fetchTournaments() {-->
<!--      try {-->
<!--        this.isLoading = true-->
<!--        this.tournamentsError = null-->

<!--        const response = await fetch(-->
<!--          `${process.env.VUE_APP_API_URL}/tournaments/?author_id=${this.$store.state.auth.userId}&offset=0&limit=10`,-->
<!--          {-->
<!--            method: 'GET',-->
<!--            headers: {-->
<!--              'Authorization': `Bearer ${this.$store.state.auth.token}`,-->
<!--            },-->
<!--          }-->
<!--        )-->

<!--        if (!response.ok) {-->
<!--          const errorData = await response.json()-->
<!--          throw new Error(errorData.message || 'Failed to fetch tournaments')-->
<!--        }-->

<!--        const data = await response.json()-->
<!--        this.tournaments = data-->

<!--      } catch (e) {-->
<!--        console.error('Error fetching tournaments:', e)-->
<!--        this.tournamentsError = 'Failed to load tournaments. Please try again later.'-->
<!--      } finally {-->
<!--        this.isLoading = false-->
<!--      }-->
<!--    },-->

<!--    async submitCreateForm() {-->
<!--      if (!this.$refs.createForm.validate()) {-->
<!--        this.createError = 'Please fill in all required fields correctly'-->
<!--        return-->
<!--      }-->

<!--      try {-->
<!--        this.isSubmitting = true-->
<!--        this.createError = ''-->

<!--        const response = await fetch(`${process.env.VUE_APP_API_URL}/tournaments/`, {-->
<!--          method: 'POST',-->
<!--          headers: {-->
<!--            'Authorization': `Bearer ${this.$store.state.auth.token}`,-->
<!--            'Content-Type': 'application/json'-->
<!--          },-->
<!--          body: JSON.stringify(this.createFormData)-->
<!--        })-->

<!--        if (!response.ok) {-->
<!--          const error = await response.json()-->
<!--          throw new Error(error.message || 'Failed to create tournament')-->
<!--        }-->

<!--        this.showCreateTournamentDialog = false-->
<!--        this.showSuccessAlert = true-->
<!--        this.successMessage = 'Tournament created successfully!'-->
<!--        await this.fetchTournaments()-->

<!--      } catch (error) {-->
<!--        console.error('Error creating tournament:', error)-->
<!--        this.createError = error.message || 'Failed to create tournament'-->
<!--      } finally {-->
<!--        this.isSubmitting = false-->
<!--      }-->
<!--    }-->
<!--  },-->
<!--  async openUpdateTournament(tournament) {-->
<!--      this.updateFormData = {-->
<!--        id: tournament.id,-->
<!--        title: tournament.title,-->
<!--        end_date: tournament.end_date,-->
<!--        prize_pool: tournament.prize_pool,-->
<!--        start_date: tournament.start_date-->
<!--      }-->
<!--      this.showUpdateTournamentDialog = true-->
<!--    },-->

<!--    async submitUpdateForm() {-->
<!--      if (!this.$refs.updateForm.validate()) {-->
<!--        this.updateError = 'Please fill in all required fields correctly'-->
<!--        return-->
<!--      }-->

<!--      try {-->
<!--        this.isSubmitting = true-->
<!--        this.updateError = ''-->

<!--        const response = await fetch(-->
<!--          `${process.env.VUE_APP_API_URL}/tournaments/${this.updateFormData.id}`,-->
<!--          {-->
<!--            method: 'PUT',-->
<!--            headers: {-->
<!--              'Authorization': `Bearer ${this.$store.state.auth.token}`,-->
<!--              'Content-Type': 'application/json'-->
<!--            },-->
<!--            body: JSON.stringify({-->
<!--              title: this.updateFormData.title,-->
<!--              end_date: this.updateFormData.end_date,-->
<!--              prize_pool: this.updateFormData.prize_pool-->
<!--            })-->
<!--          }-->
<!--        )-->

<!--        if (!response.ok) {-->
<!--          const error = await response.json()-->
<!--          throw new Error(error.message || 'Failed to update tournament')-->
<!--        }-->

<!--        this.showUpdateTournamentDialog = false-->
<!--        this.showSuccessAlert = true-->
<!--        this.successMessage = 'Tournament updated successfully!'-->
<!--        await this.fetchTournaments()-->

<!--      } catch (error) {-->
<!--        console.error('Error updating tournament:', error)-->
<!--        this.updateError = error.message || 'Failed to update tournament'-->
<!--      } finally {-->
<!--        this.isSubmitting = false-->
<!--      }-->
<!--    },-->

<!--    async submitPlayerUpdate() {-->
<!--      if (!this.$refs.playerForm.validate()) {-->
<!--        this.playerError = 'Please fill in all required fields correctly'-->
<!--        return-->
<!--      }-->

<!--      try {-->
<!--        this.isSubmitting = true-->
<!--        this.playerError = ''-->

<!--        const response = await fetch(-->
<!--          `${process.env.VUE_APP_API_URL}/players/${this.playerFormData.id}`,-->
<!--          {-->
<!--            method: 'PUT',-->
<!--            headers: {-->
<!--              'Authorization': `Bearer ${this.$store.state.auth.token}`,-->
<!--              'Content-Type': 'application/json'-->
<!--            },-->
<!--            body: JSON.stringify(this.playerFormData)-->
<!--          }-->
<!--        )-->

<!--        if (!response.ok) {-->
<!--          const error = await response.json()-->
<!--          throw new Error(error.message || 'Failed to update player')-->
<!--        }-->

<!--        this.showUpdatePlayerDialog = false-->
<!--        this.showSuccessAlert = true-->
<!--        this.successMessage = 'Player updated successfully!'-->

<!--      } catch (error) {-->
<!--        console.error('Error updating player:', error)-->
<!--        this.playerError = error.message || 'Failed to update player'-->
<!--      } finally {-->
<!--        this.isSubmitting = false-->
<!--      }-->
<!--    },-->
<!--    mounted() {-->
<!--    this.fetchTournaments()-->
<!--  }-->
<!--}-->
<!--</script>-->

<!--<style scoped>-->
<!--.header-image {-->
<!--  position: fixed;-->
<!--  top: 0;-->
<!--  left: 0;-->
<!--  width: 100%;-->
<!--  height: 400px;-->
<!--  background-image: url('@/assets/top-image.png');-->
<!--  background-size: cover;-->
<!--  background-position: center;-->
<!--  z-index: 1;-->
<!--  opacity: 0.6;-->
<!--}-->

<!--.header-overlay {-->
<!--  position: fixed;-->
<!--  top: 0;-->
<!--  left: 0;-->
<!--  width: 100%;-->
<!--  height: 400px;-->
<!--  background: linear-gradient(-->
<!--    to bottom,-->
<!--    rgba(23, 28, 38, 0) 0%,-->
<!--    rgba(23, 28, 38, 0.8) 80%,-->
<!--    rgba(23, 28, 38, 1) 100%-->
<!--  );-->
<!--  z-index: 2;-->
<!--}-->

<!--.content-wrapper {-->
<!--  position: relative;-->
<!--  z-index: 3;-->
<!--  padding-top: 200px;-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--  gap: 20px;-->
<!--  width: 100vw !important;-->
<!--  margin-bottom: 100px;-->
<!--}-->

<!--.welcome-card,-->
<!--.actions-card,-->
<!--.history-card {-->
<!--  background: rgba(45, 55, 75, 0.8);-->
<!--  border-radius: 20px;-->
<!--  border: 2px solid #42DDF2FF;-->
<!--  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);-->
<!--  backdrop-filter: blur(2px);-->
<!--  position: relative;-->
<!--  overflow: hidden;-->
<!--  margin-bottom: 24px;-->
<!--  padding: 24px;-->
<!--  width: 55%;-->
<!--  margin-left: auto;-->
<!--  margin-right: auto;-->
<!--}-->

<!--.welcome-content,-->
<!--.actions-content,-->
<!--.history-content {-->
<!--  position: relative;-->
<!--  z-index: 2;-->
<!--}-->

<!--.welcome-text {-->
<!--  color: #42DDF2FF;-->
<!--  font-size: 1.8rem;-->
<!--  text-align: center;-->
<!--  margin: 0;-->
<!--}-->

<!--.section-title {-->
<!--  color: #42DDF2FF;-->
<!--  font-size: 1.4rem;-->
<!--  margin-bottom: 24px;-->
<!--  text-align: center;-->
<!--}-->

<!--.actions-buttons {-->
<!--  display: flex;-->
<!--  gap: 16px;-->
<!--  justify-content: center;-->
<!--}-->

<!--.action-btn {-->
<!--  background: #42DDF2FF !important;-->
<!--  color: #171c26 !important;-->
<!--  font-weight: bold;-->
<!--  padding: 20px 32px !important;-->
<!--  text-align: center;-->
<!--  display: flex;-->
<!--  align-items: center;-->
<!--  justify-content: center;-->
<!--}-->

<!--.action-btn:hover {-->
<!--  background: #FED854FF !important;-->
<!--  box-shadow: 0 0 15px rgba(254, 216, 84, 0.3);-->
<!--}-->

<!--/* Tournament List Styles */-->
<!--.tournament-list {-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--  gap: 16px;-->
<!--}-->

<!--.tournament-item {-->
<!--  background: rgba(45, 55, 75, 0.8);-->
<!--  border: 1px solid rgba(8, 87, 144, 0.2);-->
<!--  border-radius: 10px;-->
<!--  padding: 16px;-->
<!--  transition: all 0.2s;-->
<!--}-->

<!--.tournament-item:hover {-->
<!--  background: rgb(45, 55, 75);-->
<!--  border-color: #42DDF2FF;-->
<!--  transform: translateY(-2px);-->
<!--  box-shadow: 0 4px 8px rgba(8, 117, 176, 0.2);-->
<!--}-->

<!--.tournament-header {-->
<!--  display: flex;-->
<!--  justify-content: space-between;-->
<!--  align-items: center;-->
<!--  margin-bottom: 12px;-->
<!--}-->

<!--.tournament-title {-->
<!--  display: flex;-->
<!--  align-items: center;-->
<!--  gap: 8px;-->
<!--  color: white;-->
<!--  font-weight: 500;-->
<!--  font-size: 1.1rem;-->
<!--}-->

<!--.tournament-icon {-->
<!--  color: #42DDF2FF !important;-->
<!--}-->

<!--.status-tag {-->
<!--  padding: 4px 12px;-->
<!--  border-radius: 12px;-->
<!--  font-size: 0.9rem;-->
<!--}-->

<!--.status-pending {-->
<!--  background: rgba(254, 216, 84, 0.1);-->
<!--  color: #FED854FF;-->
<!--  border: 1px solid rgba(254, 216, 84, 0.3);-->
<!--}-->

<!--.status-active {-->
<!--  background: rgba(66, 221, 242, 0.1);-->
<!--  color: #42DDF2FF;-->
<!--  border: 1px solid rgba(66, 221, 242, 0.3);-->
<!--}-->

<!--.status-finished {-->
<!--  background: rgba(255, 99, 99, 0.1);-->
<!--  color: #ff6363;-->
<!--  border: 1px solid rgba(255, 99, 99, 0.3);-->
<!--}-->

<!--.tournament-details {-->
<!--  display: flex;-->
<!--  gap: 24px;-->
<!--  align-items: center;-->
<!--  flex-wrap: wrap;-->
<!--}-->

<!--.detail-item {-->
<!--  display: flex;-->
<!--  align-items: center;-->
<!--  gap: 8px;-->
<!--  color: rgba(255, 255, 255, 0.7);-->
<!--  font-size: 0.9rem;-->
<!--}-->

<!--.detail-icon {-->
<!--  color: #42DDF2FF !important;-->
<!--}-->

<!--.edit-btn {-->
<!--  background: #42DDF2FF !important;-->
<!--  color: #171c26 !important;-->
<!--  margin-left: auto;-->
<!--}-->

<!--.edit-btn:disabled {-->
<!--  background: rgba(66, 221, 242, 0.3) !important;-->
<!--  color: rgba(23, 28, 38, 0.5) !important;-->
<!--}-->

<!--/* Dialog Styles */-->
<!--.dialog-card {-->
<!--  background: rgba(45, 55, 75, 0.95) !important;-->
<!--  border: 2px solid #42DDF2FF;-->
<!--  backdrop-filter: blur(10px);-->
<!--}-->

<!--.dialog-content {-->
<!--  padding: 24px;-->
<!--}-->

<!--.dialog-title {-->
<!--  color: #42DDF2FF;-->
<!--  font-weight: bold;-->
<!--  font-size: 1.25rem;-->
<!--  text-align: center;-->
<!--  margin-bottom: 16px;-->
<!--}-->

<!--.teams-card {-->
<!--  background: rgba(45, 55, 75, 0.5) !important;-->
<!--  border: 1px solid #42DDF2FF;-->
<!--  margin-top: 24px;-->
<!--}-->

<!--.teams-title {-->
<!--  color: #42DDF2FF;-->
<!--  font-size: 1.1rem;-->
<!--}-->

<!--.team-input {-->
<!--  margin-bottom: 8px;-->
<!--}-->

<!--:deep(.v-field) {-->
<!--  color: white !important;-->
<!--  border-color: rgba(66, 221, 242, 0.3) !important;-->
<!--}-->

<!--:deep(.v-field:hover) {-->
<!--  border-color: #42DDF2FF !important;-->
<!--}-->

<!--:deep(.v-label) {-->
<!--  color: rgba(255, 255, 255, 0.7) !important;-->
<!--}-->

<!--:deep(.v-field__input) {-->
<!--  color: white !important;-->
<!--}-->

<!--:deep(.v-text-field__details) {-->
<!--  color: #fed854 !important;-->
<!--}-->

<!--:deep(.v-messages__message) {-->
<!--  color: #fed854 !important;-->
<!--}-->

<!--.cancel-btn {-->
<!--  color: #42DDF2FF !important;-->
<!--}-->

<!--.submit-btn {-->
<!--  background: #42DDF2FF !important;-->
<!--  color: #171c26 !important;-->
<!--  margin-left: 16px;-->
<!--}-->

<!--.error-message {-->
<!--  color: #fed854;-->
<!--  font-size: 0.9rem;-->
<!--  text-align: center;-->
<!--  padding: 16px;-->
<!--}-->

<!--/* Loading State */-->
<!--.v-progress-circular {-->
<!--  width: 70px !important;-->
<!--  height: 70px !important;-->
<!--}-->

<!--/* Responsive Styles */-->
<!--@media (max-width: 960px) {-->
<!--  .welcome-card,-->
<!--  .actions-card,-->
<!--  .history-card {-->
<!--    width: 80%;-->
<!--  }-->

<!--  .tournament-details {-->
<!--    flex-direction: column;-->
<!--    align-items: flex-start;-->
<!--    gap: 12px;-->
<!--  }-->

<!--  .edit-btn {-->
<!--    margin-left: 0;-->
<!--    width: 100%;-->
<!--  }-->

<!--  .actions-buttons {-->
<!--    flex-direction: column;-->
<!--  }-->

<!--  .action-btn {-->
<!--    width: 100%;-->
<!--  }-->
<!--}-->

<!--@media (max-width: 600px) {-->
<!--  .welcome-card,-->
<!--  .actions-card,-->
<!--  .history-card {-->
<!--    width: 95%;-->
<!--  }-->

<!--  .welcome-text {-->
<!--    font-size: 1.5rem;-->
<!--  }-->

<!--  .section-title {-->
<!--    font-size: 1.2rem;-->
<!--  }-->
<!--}-->
<!--</style>-->


