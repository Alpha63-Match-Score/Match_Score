<template>
  <v-app>

    <!-- Navigation Drawer -->
    <v-navigation-drawer
      expand-on-hover
      rail
      class="transparent-drawer">

      <!-- Avatar/Logo -->
      <v-list-item
        prepend-icon="mdi-cat"
        title="Kitten Strike"
      ></v-list-item>

      <!-- Search bar -->
      <v-list-item>
        <v-text-field
          density="compact"
          variant="outlined"
          prepend-icon="mdi-magnify"
          placeholder="Search..."
          hide-details
          rounded
          class="mt-2"
        ></v-text-field>
      </v-list-item>

      <v-divider></v-divider>

      <v-list nav>
        <v-list-item
          v-for="(item, index) in menuItems.slice(0, 4)"
          :key="index"
          :to="item.path"
          :prepend-icon="item.icon"
          link
        >
          {{ item.title }}
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <!-- If logged in -> dashboard and logout button -->
      <div v-if="authStore.isAuthenticated">
        <v-list-item
          @click="handleLogout"
          prepend-icon="mdi-logout"
          link
          color="error"
        >
          Logout
        </v-list-item>

      <v-list nav>
        <v-list-item
          v-for="(item, index) in menuItems.slice(4)"
          :key="index"
          :to="item.path"
          :prepend-icon="item.icon"
          link
        >
          {{ item.title }}
        </v-list-item>
      </v-list>
      </div>

      <!-- If not logged in -> login and register button -->
      <div v-else>
      <v-list nav>
        <v-list-item
          v-for="(item, index) in menuItems.slice(5, 7)"
          :key="index"
          :to="item.path"
          :prepend-icon="item.icon"
          link
        >
          {{ item.title }}
        </v-list-item>
      </v-list>
      </div>


      <v-divider></v-divider>

      <v-list nav>
        <v-list-item
          v-for="(item, index) in menuItems.slice(7)"
          :key="index"
          :to="item.path"
          :prepend-icon="item.icon"
          link
        >
          {{ item.title }}
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <router-view></router-view>
    </v-main>

    <!-- Footer -->
    <v-footer class="app-footer">
      <div class="footer-content">
        <div class="footer-left">
          <span class="footer-text">© 2024 Kitten Strike. All rights reserved.</span>
        </div>

        <div class="footer-right">
          <v-btn icon variant="text">
            <v-icon>mdi-github</v-icon>
          </v-btn>
        </div>
      </div>
    </v-footer>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()
const menuItems = ref([
  { title: 'Home', path: '/', icon: 'mdi-home' },
  { title: 'Events', path: '/events', icon: 'mdi-trophy' },
  { title: 'Matches', path: '/matches', icon: 'mdi-gamepad-variant' },
  { title: 'Teams', path: '/teams', icon: 'mdi-account-group' },
  { title: 'Dashboard', path: '/dashboard', icon: 'mdi-paw' },
  { title: 'Login', path: '/login', icon: 'mdi-account' },
  { title: 'Register', path: '/register', icon: 'mdi-account-plus' },
  { title: 'About', path: '/about', icon: 'mdi-information' },

])

const handleLogout = async () => {
  const success = await authStore.logout()

  if (success) {
    await router.push('/')
  } else {
    console.error('Failed to logout')
  }
}
</script>

<style>

#app {
  min-height: 100vh;
  min-width: 100vw;
  background: #171c26;
  padding: 0 0 0 0 !important;
}

.v-application {
    background-color: #171c26 !important;
    display: flex;
    min-height: 100vh !important;
    width: 120vw !important;
    flex-direction: column;
    overflow-x: hidden;
}

.v-main {
  min-height: calc(100vh - 64px) !important;
  height: auto !important;
  overflow-y: auto;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 64px); /* Adjust 64px based on your footer height */
}

.v-navigation-drawer {
  height: 100vh !important;
}

.transparent-drawer {
  background-color: rgba(206, 214, 225, 0) !important;
  backdrop-filter: blur(10px);
  color: white !important;
}

.transparent-drawer .v-list {
  background-color: transparent !important;
  color: white !important;
}

.transparent-drawer .v-list-item {
  background-color: transparent !important;
  color: white !important;
}

.transparent-drawer .v-list-item__prepend > .v-icon {
  color: white !important;
}

.transparent-drawer .v-list-item-title {
  color: white !important;
}

.v-text-field {
  width: 100%;
  color: white !important;
}

.v-text-field input {
  font-size: 0.9rem;
  color: white !important;
}

.v-text-field input::placeholder {
  color: rgba(255, 255, 255, 0.7) !important;
}

.transparent-drawer .v-text-field .v-field__outline {
  color: rgba(255, 255, 255, 0.7) !important;
}

.transparent-drawer .v-divider {
  opacity: 0.5;
  border-color: rgba(255, 255, 255, 0.1) !important;
}

.transparent-drawer .v-list-item--active {
  color: #fed854 !important;
}

.transparent-drawer .v-list-item--active .v-icon {
  color: #fed854 !important;
}
/* Search bar */
.v-text-field {
  width: 100%;
}

/* Input for search bar */
.v-text-field input {
  font-size: 0.9rem;
}


.app-footer {
  background: rgba(45, 55, 75, 0.5) !important;
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(8, 117, 176, 0.4);
  min-height: 64px !important;
  padding: 12px 24px !important;
  position: relative;
  z-index: 1000;
  width: 100vw !important;
}

.footer-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-left: 70px;
  margin-right: 20px;
}

.footer-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.footer-right {
  display: flex;
  gap: 8px;
}

.footer-right .v-btn {
  color: rgba(255, 255, 255, 0.7) !important;
  transition: color 0.2s;
}

.footer-right .v-btn:hover {
  color: #fed854 !important;
}
</style>
