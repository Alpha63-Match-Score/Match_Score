<template>
  <div class="admin-dashboard">
    <header class="dashboard-header">
      <h1>Admin Dashboard</h1>
    </header>

    <div class="dashboard-content">
      <div class="actions-section">
        <h2>Available Actions</h2>
        <div class="action-buttons">
          <button class="action-btn" @click="openTournamentDialog">
            Add Tournament
          </button>
          <button class="action-btn" @click="openMatchDialog">
            Add Match
          </button>
          <button class="action-btn" @click="openPlayerDialog">
            Add Player
          </button>
          <button class="action-btn" @click="openTeamAssignmentDialog">
            Assign Player to Team
          </button>
        </div>
      </div>

      <div class="requests-section">
        <h2>Request History</h2>
        <div class="requests-filter">
          <label>
            Filter by Status:
            <select v-model="selectedStatus">
              <option value="">All</option>
              <option value="pending">Pending</option>
              <option value="accepted">Accepted</option>
              <option value="rejected">Rejected</option>
            </select>
          </label>
          <label>
            Filter by Admin:
            <select v-model="selectedAdmin">
              <option value="">All</option>
              <option v-for="admin in admins" :value="admin.id">
                {{ admin.name }}
              </option>
            </select>
          </label>
        </div>
        <div class="requests-list">
          <div v-for="request in filteredRequests" :key="request.id" class="request-item">
            <div class="request-header">
              <div class="request-type">
                <i :class="getRequestTypeIcon(request.type)"></i>
                {{ formatRequestType(request.type) }}
              </div>
              <div :class="['status-tag', `status-${request.status}`]">
                {{ formatStatus(request.status) }}
              </div>
            </div>
            <div class="request-details">
              <div class="detail-item">
                <i class="detail-icon mdi mdi-email"></i>
                {{ request.email }}
              </div>
              <div class="detail-item">
                <i class="detail-icon mdi mdi-calendar"></i>
                {{ formatDate(request.requestDate) }}
              </div>
              <div v-if="request.responseDate" class="detail-item">
                <i class="detail-icon mdi mdi-calendar-check"></i>
                {{ formatDate(request.responseDate) }}
              </div>
              <div v-if="request.adminId" class="detail-item">
                <i class="detail-icon mdi mdi-account"></i>
                {{ getAdminName(request.adminId) }}
              </div>
              <div v-if="request.username" class="detail-item">
                <i class="detail-icon mdi mdi-account"></i>
                Player: {{ request.username }}
              </div>
            </div>
            <div class="request-actions" v-if="request.status === 'pending'">
              <button class="action-btn accept-btn" @click="acceptRequest(request)">
                Accept
              </button>
              <button class="action-btn reject-btn" @click="rejectRequest(request)">
                Reject
              </button>
            </div>
          </div>
          <div v-if="filteredRequests.length === 0" class="empty-state">
            No requests found.
          </div>
        </div>
      </div>
    </div>

    <v-dialog v-model="showTournamentDialog" max-width="500">
      <!-- Tournament dialog content -->
    </v-dialog>

    <v-dialog v-model="showMatchDialog" max-width="500">
      <!-- Match dialog content -->
    </v-dialog>

    <v-dialog v-model="showPlayerDialog" max-width="500">
      <!-- Player dialog content -->
    </v-dialog>

    <v-dialog v-model="showTeamAssignmentDialog" max-width="500">
      <!-- Team assignment dialog content -->
    </v-dialog>
  </div>
</template>

<script>
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default {
  data() {
    return {
      selectedStatus: '',
      selectedAdmin: '',
      requests: [],
      admins: [],
      showTournamentDialog: false,
      showMatchDialog: false,
      showPlayerDialog: false,
      showTeamAssignmentDialog: false
    }
  },
  computed: {
    filteredRequests() {
      return this.requests.filter(request => {
        if (this.selectedStatus && request.status !== this.selectedStatus) {
          return false
        }
        if (this.selectedAdmin && request.adminId !== this.selectedAdmin) {
          return false
        }
        return true
      })
    }
  },
  methods: {
    formatRequestType(type) {
      return type.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
    },
    formatStatus(status) {
      return status.charAt(0).toUpperCase() + status.slice(1)
    },
    formatDate(date) {
      return new Date(date).toLocaleString()
    },
    getRequestTypeIcon(type) {
      return type === 'promote user to director' ? 'mdi-shield-account' : 'mdi-account-plus'
    },
    getAdminName(id) {
      const admin = this.admins.find(a => a.id === id)
      return admin ? admin.name : 'Unknown'
    },
    acceptRequest(request) {
      // Logic to accept the request
    },
    rejectRequest(request) {
      // Logic to reject the request
    },
    openTournamentDialog() {
      this.showTournamentDialog = true
    },
    openMatchDialog() {
      this.showMatchDialog = true
    },
    openPlayerDialog() {
      this.showPlayerDialog = true
    },
    openTeamAssignmentDialog() {
      this.showTeamAssignmentDialog = true
    }
  },
  mounted() {
    // Fetch requests and admin data
    this.fetchRequests()
    this.fetchAdmins()
  }
}
</script>

<style scoped>
.admin-dashboard {
  background-color: #171c26;
  color: white;
  padding: 24px;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 32px;
}

.actions-section,
.requests-section {
  background-color: rgba(45, 55, 75, 0.8);
  border: 2px solid #42DDF2FF;
  border-radius: 10px;
  padding: 24px;
  margin-bottom: 24px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.action-btn {
  background-color: #42DDF2FF !important;
  color: #171c26 !important;
  font-weight: bold;
  padding: 12px 24px !important;
  border-radius: 6px;
  cursor: pointer;
}

.action-btn:hover {
  background-color: #FED854FF !important;
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.3);
}

.requests-filter {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 16px;
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.request-item {
  background-color: rgba(45, 55, 75, 0.8);
  border: 1px solid rgba(8, 87, 144, 0.2);
  border-radius: 10px;
  padding: 16px;
  transition: all 0.2s;
}

.request-item:hover {
  background-color: rgb(45, 55, 75);
  border-color: #42DDF2FF;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(8, 117, 176, 0.2);
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.request-type {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.request-icon {
  color: #42DDF2FF !important;
}

.status-tag {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.9rem;
}

.status-pending {
  background-color: rgba(254, 216, 84, 0.1);
  color: #FED854FF;
  border: 1px solid rgba(254, 216, 84, 0.3);
}

.status-accepted {
  background-color: rgba(0, 255, 157, 0.1);
  color: #00ff9d;
  border: 1px solid rgba(0, 255, 157, 0.3);
}

.status-rejected {
  background-color: rgba(255, 99, 99, 0.1);
  color: #ff6363;
  border: 1px solid rgba(255, 99, 99, 0.3);
}

.request-details {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.detail-icon {
  color: #42DDF2FF !important;
}

.request-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 16px;
}

.accept-btn {
  background-color: rgba(0, 255, 157, 0.1) !important;
  color: #00ff9d !important;
  border: 1px solid rgba(0, 255, 157, 0.3);
}

.reject-btn {
  background-color: rgba(255, 99, 99, 0.1) !important;
  color: #ff6363 !important;
  border: 1px solid rgba(255, 99, 99, 0.3);
}

.empty-state {
  text-align: center;
  color: rgba(255, 255, 255, 0.5);
  padding: 32px 0;
}
</style>
