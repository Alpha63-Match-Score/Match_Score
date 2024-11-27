<!--<template>-->
<!--  <div>-->
<!--    <div v-if="!currentComponent">Loading...</div>-->
<!--    <component v-else :is="currentComponent" />-->
<!--  </div>-->
<!--</template>-->

<!--<script setup lang="ts">-->
<!--import { ref, watch, defineAsyncComponent } from 'vue';-->
<!--import { useAuthStore } from '@/stores/auth';-->

<!--const authStore = useAuthStore();-->
<!--const currentComponent = ref(null);-->

<!--// Map roles to components-->
<!--const roleToComponentMap = {-->
<!--  USER: () => import('@/views/DashboardUser.vue'),-->
<!--  ADMIN: () => import('@/views/DashboardAdmin.vue'),-->
<!--  PLAYER: null,-->
<!--  DIRECTOR: null,-->
<!--};-->

<!--// Watch for changes in userRole-->
<!--watch(() => authStore.userRole, (newRole) => {-->
<!--  if (newRole) {-->
<!--    // Dynamically select the component loader based on the role-->
<!--    const componentLoader = roleToComponentMap[newRole] || (() =>-->
<!--      Promise.resolve({-->
<!--        template: '<div>Unauthorized Access</div>',-->
<!--      })-->
<!--    );-->

<!--    currentComponent.value = defineAsyncComponent({-->
<!--      loader: componentLoader,-->
<!--      loadingComponent: {-->
<!--        template: '<div>Loading...</div>',-->
<!--      },-->
<!--      errorComponent: {-->
<!--        template: '<div>Error loading component</div>',-->
<!--      },-->
<!--    });-->
<!--  }-->
<!--}, { immediate: true });-->
<!--</script>-->
