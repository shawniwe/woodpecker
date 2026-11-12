<template>
  <header
    class="border-border bg-card text-card-foreground flex min-h-12 shrink-0 items-center gap-2 border-b px-3 sm:px-4"
  >
    <template v-if="user">
      <IconButton
        class="hidden! md:flex!"
        :title="$t('toggle_sidebar')"
        aria-controls="workspace-navigation"
        :aria-expanded="!compact"
        @click="$emit('toggleSidebar')"
      >
        <SvgIcon :path="mdiDockLeft" size="1.15rem" />
      </IconButton>
      <router-link
        :to="{ name: 'repos' }"
        class="focus-visible:outline-wp-link-100 flex size-8 shrink-0 items-center justify-center rounded-md focus-visible:outline-2 md:hidden"
        :aria-label="$t('repositories.title')"
      >
        <WoodpeckerLogo class="size-6" />
      </router-link>
      <span class="border-border ml-1 hidden h-4 border-l md:block" />
      <span class="min-w-0 truncate text-sm font-medium">{{ sectionTitle }}</span>
    </template>
    <router-link v-else :to="{ name: 'home' }" class="flex items-center gap-2 font-semibold" aria-label="Woodpecker">
      <WoodpeckerLogo class="size-6" />
      <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
      <span>Woodpecker</span>
    </router-link>

    <div class="ml-auto flex shrink-0 items-center gap-1">
      <span
        v-if="version?.currentShort"
        class="text-wp-text-alt-100 hidden px-2 font-mono text-xs sm:inline"
        :title="version.current"
      >
        {{ version.currentShort }}
      </span>
      <ActivePipelines v-if="user" class="size-8" />
      <IconButton
        v-if="user?.admin"
        class="md:hidden!"
        icon="settings-outline"
        :title="$t('admin.settings.settings')"
        :to="{ name: 'admin-settings' }"
      />
      <IconButton
        v-if="user"
        class="md:hidden!"
        icon="user"
        :title="$t('user.settings.settings')"
        :to="{ name: 'user' }"
      />
      <Button v-else :text="$t('login')" :to="{ name: 'login' }" @click="saveRedirect" />
    </div>
  </header>
</template>

<script lang="ts" setup>
import { mdiDockLeft } from '@mdi/js';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';

import WoodpeckerLogo from '~/assets/logo.svg?component';
import Button from '~/components/atomic/Button.vue';
import IconButton from '~/components/atomic/IconButton.vue';
import SvgIcon from '~/components/atomic/SvgIcon.vue';
import useUserConfig from '~/compositions/useUserConfig';
import { useVersion } from '~/compositions/useVersion';
import type { User } from '~/lib/api/types';

import ActivePipelines from './ActivePipelines.vue';

const props = defineProps<{
  user: User | null;
  compact: boolean;
  section: string;
}>();

defineEmits<{ toggleSidebar: [] }>();

const { t } = useI18n();
const route = useRoute();
const userConfig = useUserConfig();
const version = useVersion();
const sectionTitle = computed(() => {
  if (props.section === 'admin') return t('admin.settings.settings');
  if (props.section === 'user') return t('user.settings.settings');
  if (props.section === 'org' || props.section === 'orgs') return t('admin.settings.orgs.orgs');
  return t('repositories.title');
});

function saveRedirect() {
  userConfig.setUserConfig('redirectUrl', route.fullPath);
}
</script>
