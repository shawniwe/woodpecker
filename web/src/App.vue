<template>
  <div class="app bg-wp-background-200 text-card-foreground m-auto flex h-full w-full flex-col">
    <router-view v-if="layout === 'blank'" />
    <div v-else class="flex min-h-0 flex-1">
      <Sidebar v-if="user" :user="user" :compact="compact" :section="section" />
      <div
        class="bg-card flex min-w-0 flex-1 flex-col"
        :class="{ 'border-border md:my-2 md:mr-2 md:overflow-hidden md:rounded-xl md:border md:shadow-xs': user }"
      >
        <Navbar :user="user" :compact="compact" :section="section" @toggle-sidebar="compact = !compact" />
        <main class="relative flex min-h-0 flex-1">
          <div id="scroll-component" class="flex min-w-0 grow flex-col overflow-y-auto">
            <router-view />
          </div>
          <transition name="slide-right">
            <PipelineFeedSidebar
              class="border-border bg-card absolute inset-y-0 right-0 w-full max-w-80 border-l shadow-lg xl:max-w-96"
            />
          </transition>
        </main>
      </div>
    </div>
    <notifications position="bottom right" />
  </div>
</template>

<script lang="ts" setup>
import { useStorage } from '@vueuse/core';
import { computed, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';

import Navbar from '~/components/layout/header/Navbar.vue';
import Sidebar from '~/components/layout/header/Sidebar.vue';
import PipelineFeedSidebar from '~/components/pipeline-feed/PipelineFeedSidebar.vue';
import useApiClient from '~/compositions/useApiClient';
import useAuthentication from '~/compositions/useAuthentication';
import useConfig from '~/compositions/useConfig';
import useNotifications from '~/compositions/useNotifications';

const route = useRoute();
const { user } = useAuthentication();
const { rootPath } = useConfig();
const compact = useStorage('woodpecker-sidebar-compact', false);
const section = computed(() => route.path.slice(rootPath?.length ?? 0).split('/')[1] ?? '');
const apiClient = useApiClient();
const { notify } = useNotifications();
const i18n = useI18n();

// eslint-disable-next-line promise/prefer-await-to-callbacks
apiClient.setErrorHandler((err) => {
  if (err.status === 404) {
    notify({ title: i18n.t('errors.not_found'), type: 'error' });
    return;
  }
  notify({ title: err.message || i18n.t('unknown_error'), type: 'error' });
});

const layout = computed(() => route.meta.layout ?? 'default');

const { locale } = useI18n();
watch(
  locale,
  () => {
    document.documentElement.setAttribute('lang', locale.value);
  },
  { immediate: true },
);
</script>

<style scoped>
.app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#scroll-component {
  scrollbar-gutter: stable;
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s ease;
}
.slide-right-enter-from,
.slide-right-leave-to {
  transform: translate(100%, 0);
}
</style>
