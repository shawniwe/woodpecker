<template>
  <nav
    class="border-border bg-card text-card-foreground z-20 flex min-h-15 shrink-0 items-center gap-3 border-b px-3 sm:gap-5 sm:px-6"
  >
    <div class="flex min-w-0 items-center gap-1 sm:gap-2">
      <router-link
        :to="{ name: 'home' }"
        aria-label="Woodpecker"
        class="navbar-brand mr-1 flex shrink-0 items-center gap-2 rounded-md pr-1 sm:mr-3"
      >
        <span class="bg-wp-control-ok-200 grid size-8 shrink-0 place-items-center rounded-lg">
          <WoodpeckerLogo class="size-6" />
        </span>
        <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
        <span class="hidden text-sm font-semibold tracking-tight sm:inline">Woodpecker</span>
        <span
          v-if="version?.currentShort"
          class="border-border text-wp-text-alt-100 hidden rounded border px-1.5 py-0.5 font-mono text-[11px] lg:inline"
          :title="version.current"
        >
          {{ version.currentShort }}
        </span>
      </router-link>
      <router-link
        v-if="user"
        :to="{ name: 'repos' }"
        class="navbar-link"
        :class="{ 'navbar-selected': inRepositories }"
      >
        <span class="flex md:hidden">{{ $t('repos') }}</span>
        <span class="hidden md:flex">{{ $t('repositories.title') }}</span>
      </router-link>
      <a
        href="https://woodpecker-ci.org/"
        target="_blank"
        rel="noopener noreferrer"
        class="navbar-link hidden! md:flex!"
      >
        {{ $t('docs') }}
      </a>
      <a
        v-if="enableSwagger"
        :href="apiUrl"
        target="_blank"
        rel="noopener noreferrer"
        class="navbar-link hidden! md:flex!"
      >
        {{ $t('api') }}
      </a>
    </div>
    <div class="ml-auto flex shrink-0 items-center gap-1">
      <IconButton
        v-if="user?.admin"
        class="navbar-icon relative"
        :title="$t('settings')"
        :to="{ name: 'admin-settings' }"
      >
        <Icon name="settings" />
        <div v-if="version?.needsUpdate" class="bg-wp-error-100 absolute top-2 right-2 h-3 w-3 rounded-full" />
      </IconButton>

      <ActivePipelines v-if="user" class="navbar-icon p-1.5!" />
      <IconButton v-if="user" :to="{ name: 'user' }" :title="$t('user.settings.settings')" class="navbar-icon p-1.5!">
        <img v-if="user && user.avatar_url" class="size-full rounded-full object-cover" :src="user.avatar_url" alt="" />
        <span v-else class="bg-wp-background-200 grid size-full place-items-center rounded-full text-xs">
          {{ user.login.slice(0, 1).toUpperCase() }}
        </span>
      </IconButton>
      <Button v-else :text="$t('login')" :to="{ name: 'login' }" class="h-8" @click="saveRedirect" />
    </div>
  </nav>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

import WoodpeckerLogo from '~/assets/logo.svg?component';
import Button from '~/components/atomic/Button.vue';
import Icon from '~/components/atomic/Icon.vue';
import IconButton from '~/components/atomic/IconButton.vue';
import useAuthentication from '~/compositions/useAuthentication';
import useConfig from '~/compositions/useConfig';
import useUserConfig from '~/compositions/useUserConfig';
import { useVersion } from '~/compositions/useVersion';

import ActivePipelines from './ActivePipelines.vue';

const version = useVersion();
const config = useConfig();
const userConfig = useUserConfig();
const route = useRoute();
const authentication = useAuthentication();
const { user } = authentication;
const inRepositories = computed(() => /^\/repos(?:\/|$)/.test(route.path.slice(config.rootPath?.length ?? 0)));
const apiUrl = `${config.rootPath ?? ''}/swagger/index.html`;

const { enableSwagger } = config;

function saveRedirect() {
  userConfig.setUserConfig('redirectUrl', route.fullPath);
}
</script>

<style scoped>
@reference '~/tailwind.css';

.navbar-icon {
  @apply size-8 p-1.5;
}

.navbar-icon :deep(svg) {
  @apply size-full;
}

.navbar-link {
  @apply text-wp-text-alt-100 hover:bg-wp-background-200 hover:text-card-foreground flex h-8 items-center rounded-md px-2 text-sm font-medium whitespace-nowrap sm:px-3;
}

.navbar-selected {
  @apply bg-wp-background-200 text-card-foreground;
}

.navbar-link:focus-visible,
.navbar-brand:focus-visible {
  @apply outline-wp-link-100 outline-2 outline-offset-2;
}
</style>
