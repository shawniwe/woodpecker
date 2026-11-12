<template>
  <router-link
    v-if="repo"
    :to="{ name: 'repo', params: { repoId: repo.id } }"
    class="focus-visible:outline-wp-link-100 block min-w-0 rounded-xl focus-visible:outline-2 focus-visible:outline-offset-2"
  >
    <Card class="group hover:border-wp-background-500 hover:bg-wp-background-200 gap-0 p-4 transition-colors">
      <div class="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-x-3 gap-y-2">
        <div class="truncate text-sm font-semibold">
          <span class="text-wp-text-alt-100 font-normal">{{ repo.owner }} / </span>{{ repo.name }}
        </div>
        <div class="text-wp-text-100 ml-auto">
          <div
            v-if="repo.visibility === RepoVisibility.Private"
            :title="`${$t('repo.visibility.visibility')}: ${$t(`repo.visibility.private.private`)}`"
          >
            <Icon name="visibility-private" />
          </div>
          <div
            v-else-if="repo.visibility === RepoVisibility.Internal"
            :title="`${$t('repo.visibility.visibility')}: ${$t(`repo.visibility.internal.internal`)}`"
          >
            <Icon name="visibility-internal" />
          </div>
        </div>

        <div class="text-wp-text-alt-100 col-span-2 flex min-w-0 gap-x-4 text-sm">
          <template v-if="lastPipeline">
            <div class="flex min-w-0 flex-1 items-center gap-x-1">
              <PipelineStatusIcon v-if="lastPipeline" :status="lastPipeline.status" />
              <RenderMarkdown
                class="overflow-hidden pl-1 text-ellipsis whitespace-nowrap"
                :title="message"
                :content="shortMessage"
                inline
              />
            </div>

            <div class="ml-auto flex shrink-0 items-center gap-x-1">
              <Icon name="since" />
              <span>{{ since }}</span>
            </div>
          </template>

          <div v-else class="flex gap-x-2">
            <span>{{ $t('repo.pipeline.no_pipelines') }}</span>
          </div>
        </div>
      </div>
    </Card>
  </router-link>
</template>

<script lang="ts" setup>
import { computed } from 'vue';

import Icon from '~/components/atomic/Icon.vue';
import RenderMarkdown from '~/components/atomic/RenderMarkdown.vue';
import PipelineStatusIcon from '~/components/repo/pipeline/PipelineStatusIcon.vue';
import Card from '~/components/ui/card/Card.vue';
import usePipeline from '~/compositions/usePipeline';
import type { Repo } from '~/lib/api/types';
import { RepoVisibility } from '~/lib/api/types';

const props = defineProps<{
  repo: Repo;
}>();

const lastPipeline = computed(() => props.repo.last_pipeline);
const { since, shortMessage, message } = usePipeline(lastPipeline);
</script>
