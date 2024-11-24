<template>
  <v-app>
    <!-- App Bar -->
    <v-app-bar flat>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-app-bar-title>Kitten Strike</v-app-bar-title>
    </v-app-bar>

    <!-- Navigation Drawer -->
    <v-navigation-drawer v-model="drawer">
      <v-list-item
        title="Kitten Strike"
        subtitle="Welcome!"
      ></v-list-item>

      <v-divider></v-divider>

      <v-list nav>
        <v-list-item
          v-for="(item, index) in menuItems"
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
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const drawer = ref(true)
const menuItems = ref([
  { title: 'Home', path: '/', icon: 'mdi-home' },
  { title: 'About', path: '/about', icon: 'mdi-information' }
])
</script>

<style>
.v-application {
  height: 100vh;
}

.v-main {
  height: calc(100vh - 64px); /* 64px е височината на app bar */
  padding-top: 0 !important;
}

.v-navigation-drawer {
  top: 64px !important; /* Започва след app bar */
  height: calc(100vh - 64px) !important;
}
</style>
