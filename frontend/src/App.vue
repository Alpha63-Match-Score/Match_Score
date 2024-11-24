<template>
  <v-app>
    <!-- App Bar for opening drawer -->
    <v-app-bar>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Kitten Strike</v-toolbar-title>
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
          :title="item.title"
          :to="item.path"
          :prepend-icon="item.icon"
          link
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface MenuItem {
  title: string
  path: string
  icon: string
}

const drawer = ref<boolean | null>(null)

const menuItems = ref<MenuItem[]>([
  {
    title: 'Home',
    path: '/',
    icon: 'mdi-home'
  },
  {
    title: 'About',
    path: '/about',
    icon: 'mdi-information'
  },
])
</script>
