<template>
  <div>
    <component :is="currentComponent" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, defineAsyncComponent } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const role = ref<string | null>(null);
const currentComponent = ref(null);

onMounted(() => {
  role.value = authStore.userRole;

  // Dynamically load the component based on the role
  if (role.value === 'User') {
    currentComponent.value = defineAsyncComponent(() => import('@/views/DashboardUser.vue'));
  } else if (role.value === 'Admin') {
    currentComponent.value = defineAsyncComponent(() => import('@/components/AdminDashboard.vue'));
  } else if (role.value === 'Director') {
    currentComponent.value = defineAsyncComponent(() => import('@/components/DirectorDashboard.vue'));
  } else if (role.value === 'Player') {
    currentComponent.value = defineAsyncComponent(() => import('@/components/PlayerDashboard.vue'));
  } else {
    currentComponent.value = () => 'Unauthorized Access';
  }
});
</script>
