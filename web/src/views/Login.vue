<template>
  <main class="flex min-h-full w-full flex-col items-center justify-center gap-4 px-4 py-8">
    <Error v-if="errorMessage" class="w-full md:w-3xl">
      <span class="whitespace-pre">{{ errorMessage }}</span>
      <span v-if="errorDescription" class="mt-1 whitespace-pre">{{ errorDescription }}</span>
      <a
        v-if="errorUri"
        :href="errorUri"
        target="_blank"
        class="text-wp-link-100 hover:text-wp-link-200 mt-1 cursor-pointer"
      >
        <span>{{ errorUri }}</span>
      </a>
    </Error>

    <Card class="w-full max-w-sm items-center gap-5 p-8 text-center">
      <span class="bg-wp-control-ok-200 grid size-12 place-items-center rounded-xl">
        <WoodpeckerLogo class="size-9" />
      </span>
      <h1 class="text-xl font-semibold tracking-tight">{{ $t('login_to_woodpecker_with') }}</h1>
      <div class="flex w-full flex-col gap-2">
        <Button
          v-for="forge in forgesWithNameAndFavicon"
          :key="forge.id"
          :start-icon="forge.type === 'addon' ? 'repo' : forge.type"
          class="whitespace-normal!"
          @click="authenticate(forge.id)"
        >
          <div class="mr-2 w-4">
            <img
              v-if="forge.favicon && !failedForgeFavicons.has(forge.id)"
              :src="forge.favicon"
              :alt="$t('login_to_woodpecker_with', { forge: forge.name })"
              @error="() => failedForgeFavicons.add(forge.id)"
            />
            <Icon v-else :name="forge.type === 'addon' ? 'repo' : forge.type" />
          </div>

          {{ forge.name }}
        </Button>
      </div>
    </Card>
  </main>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';

import WoodpeckerLogo from '~/assets/logo.svg?component';
import Button from '~/components/atomic/Button.vue';
import Error from '~/components/atomic/Error.vue';
import Icon from '~/components/atomic/Icon.vue';
import Card from '~/components/ui/card/Card.vue';
import useApiClient from '~/compositions/useApiClient';
import useAuthentication from '~/compositions/useAuthentication';
import { useWPTitle } from '~/compositions/useWPTitle';
import type { Forge } from '~/lib/api/types';

const route = useRoute();
const { authenticate } = useAuthentication();
const i18n = useI18n();
const apiClient = useApiClient();

const forges = ref<Forge[]>([]);

const authErrorMessages = {
  oauth_error: i18n.t('oauth_error'),
  internal_error: i18n.t('internal_error'),
  registration_closed: i18n.t('registration_closed'),
  access_denied: i18n.t('access_denied'),
  invalid_state: i18n.t('invalid_state'),
  org_access_denied: i18n.t('org_access_denied'),
};

const errorMessage = ref<string>();
const errorDescription = ref<string>(route.query.error_description as string);
// only link http(s) URIs, anything else (e.g. javascript:) could run code on click
const errorUri = computed(() => {
  const uri = route.query.error_uri as string | undefined;
  return uri?.startsWith('http') ? uri : undefined;
});

onMounted(async () => {
  forges.value = (await apiClient.getForges()) ?? [];

  if (route.query.error) {
    const error = route.query.error as keyof typeof authErrorMessages;
    errorMessage.value = authErrorMessages[error] ?? error;
  }
});

useWPTitle(computed(() => [i18n.t('login')]));

const failedForgeFavicons = ref(new Set<number>()); // Track which favicons failed to load

const forgesWithNameAndFavicon = computed(() =>
  forges.value.map((forge) => {
    let name = forge.type.charAt(0).toUpperCase() + forge.type.slice(1);
    let favicon: null | string = null;

    if (forge.url || forge.oauth_host) {
      const url = new URL(forge.oauth_host || forge.url);
      name = url.hostname;
      favicon = `${url.origin}/favicon.ico`;
    }

    return {
      ...forge,
      name,
      favicon,
    };
  }),
);
</script>
