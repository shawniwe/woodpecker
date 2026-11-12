<template>
  <aside
    id="workspace-navigation"
    class="text-card-foreground hidden shrink-0 flex-col overflow-y-auto px-2 py-3 md:flex"
    :class="compact ? 'w-14' : 'w-55'"
  >
    <router-link
      :to="{ name: 'home' }"
      aria-label="Woodpecker"
      class="sidebar-link mb-5 gap-2.5"
      :class="{ 'justify-center px-0!': compact }"
    >
      <span class="bg-card border-border grid size-8 shrink-0 place-items-center rounded-lg border shadow-xs">
        <WoodpeckerLogo class="size-5" />
      </span>
      <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
      <span v-if="!compact" class="truncate text-sm font-semibold tracking-tight">Woodpecker</span>
    </router-link>

    <nav :aria-label="$t('navigation')" class="flex flex-col gap-1">
      <router-link
        :to="{ name: 'repos' }"
        class="sidebar-link"
        :class="{ 'sidebar-active': section === 'repos', 'justify-center px-0!': compact }"
        :title="$t('repositories.title')"
        :aria-label="$t('repositories.title')"
        :aria-current="section === 'repos' ? 'location' : undefined"
      >
        <Icon name="repo" />
        <span v-if="!compact">{{ $t('repositories.title') }}</span>
      </router-link>
      <router-link
        v-if="user.admin"
        :to="{ name: 'admin-settings' }"
        class="sidebar-link"
        :class="{ 'sidebar-active': section === 'admin', 'justify-center px-0!': compact }"
        :title="$t('admin.settings.settings')"
        :aria-label="$t('admin.settings.settings')"
        :aria-current="section === 'admin' ? 'location' : undefined"
      >
        <Icon name="settings-outline" />
        <span v-if="!compact" class="truncate">{{ $t('admin.settings.settings') }}</span>
        <span v-if="version?.needsUpdate && !compact" class="bg-wp-error-100 ml-auto size-1.5 rounded-full" />
      </router-link>
    </nav>

    <div class="mt-auto flex flex-col gap-1 pt-4">
      <a
        href="https://woodpecker-ci.org/"
        target="_blank"
        rel="noopener noreferrer"
        class="sidebar-link"
        :class="{ 'justify-center px-0!': compact }"
        :title="$t('docs')"
        :aria-label="$t('docs')"
      >
        <Icon name="question" />
        <span v-if="!compact">{{ $t('docs') }}</span>
      </a>
      <a
        v-if="enableSwagger"
        :href="apiUrl"
        target="_blank"
        rel="noopener noreferrer"
        class="sidebar-link"
        :class="{ 'justify-center px-0!': compact }"
        :title="$t('api')"
        :aria-label="$t('api')"
      >
        <Icon name="console" />
        <span v-if="!compact">{{ $t('api') }}</span>
      </a>
      <router-link
        :to="{ name: 'user' }"
        class="sidebar-link border-border mt-2 border"
        :class="{ 'sidebar-active': section === 'user', 'justify-center px-0!': compact }"
        :title="$t('user.settings.settings')"
        :aria-label="$t('user.settings.settings')"
      >
        <img v-if="user.avatar_url" :src="user.avatar_url" class="size-6 shrink-0 rounded-md object-cover" alt="" />
        <Icon v-else name="user" />
        <span v-if="!compact" class="truncate font-medium">{{ user.login }}</span>
        <Icon v-if="!compact" name="chevron-right" class="ml-auto" />
      </router-link>
    </div>
  </aside>
</template>

<script setup lang="ts">
import WoodpeckerLogo from '~/assets/logo.svg?component';
import Icon from '~/components/atomic/Icon.vue';
import useConfig from '~/compositions/useConfig';
import { useVersion } from '~/compositions/useVersion';
import type { User } from '~/lib/api/types';

defineProps<{
  user: User;
  compact: boolean;
  section: string;
}>();

const version = useVersion();
const { enableSwagger, rootPath } = useConfig();
const apiUrl = `${rootPath ?? ''}/swagger/index.html`;
</script>

<style scoped>
@reference '~/tailwind.css';

.sidebar-link {
  @apply hover:bg-wp-control-neutral-100 focus-visible:outline-wp-link-100 flex min-h-9 min-w-0 items-center gap-2 rounded-md px-2 text-sm focus-visible:outline-2 focus-visible:-outline-offset-2;
}

.sidebar-active {
  @apply bg-wp-control-neutral-100 font-semibold;
}

.sidebar-link :deep(svg) {
  @apply size-4 shrink-0;
}
</style>
