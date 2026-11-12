<template>
  <Scaffold v-model:search="search">
    <template #title>
      {{ $t('repositories.title') }}
    </template>

    <template #headerActions>
      <Button
        :to="{ name: 'repo-add' }"
        start-icon="plus"
        :text="$t('repo.add')"
        class="bg-card-foreground! text-card! h-9 hover:opacity-85"
      />
      <Button
        start-icon="refresh"
        :is-loading="isRefreshing"
        :title="$t('repo.refresh')"
        :aria-label="$t('repo.refresh')"
        class="h-9"
        @click="refreshRepositories"
      />
    </template>

    <Transition name="fade" mode="out-in">
      <div v-if="search === '' && repos.length > 0" class="grid gap-7">
        <div v-if="reposLastAccess.length > 0 && repos.length > 4" class="flex flex-col gap-4">
          <div>
            <h2 class="text-sm font-semibold">{{ $t('repositories.last.title') }}</h2>
          </div>
          <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
            <RepoItem v-for="repo in reposLastAccess" :key="repo.id" :repo="repo" />
          </div>
        </div>

        <div class="flex flex-col gap-4">
          <h2 v-if="reposLastAccess.length > 0 && repos.length > 4" class="text-sm font-semibold">
            {{ $t('repositories.all.title') }}
          </h2>
          <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
            <RepoItem v-for="repo in reposLastActivity" :key="repo.id" :repo="repo" />
          </div>
        </div>
      </div>
      <div v-else class="flex flex-col">
        <div v-if="reposLastActivity.length > 0" class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
          <RepoItem v-for="repo in reposLastActivity" :key="repo.id" :repo="repo" />
        </div>
        <span v-else class="text-wp-text-100 text-center text-lg">{{ $t('no_search_results') }}</span>
      </div>
    </Transition>
  </Scaffold>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import Button from '~/components/atomic/Button.vue';
import Scaffold from '~/components/layout/scaffold/Scaffold.vue';
import RepoItem from '~/components/repo/RepoItem.vue';
import { useAsyncAction } from '~/compositions/useAsyncAction';
import useRepos from '~/compositions/useRepos';
import { useRepoSearch } from '~/compositions/useRepoSearch';
import { useWPTitle } from '~/compositions/useWPTitle';
import { useRepoStore } from '~/store/repos';

const repoStore = useRepoStore();

const { sortReposByLastAccess, sortReposByLastActivity, repoWithLastPipeline } = useRepos();
const repos = computed(() => Object.values(repoStore.ownedRepos).map((r) => repoWithLastPipeline(r)));

const reposLastAccess = computed(() => sortReposByLastAccess(repos.value || []).slice(0, 4));

const search = ref('');
const { searchedRepos } = useRepoSearch(repos, search);
const reposLastActivity = computed(() => sortReposByLastActivity(searchedRepos.value || []));

const { doSubmit: refreshRepositories, isLoading: isRefreshing } = useAsyncAction(async () => {
  await repoStore.refreshRepos();
  await repoStore.loadRepos();
});

onMounted(async () => {
  await repoStore.loadRepos();
});

const { t } = useI18n();
useWPTitle(computed(() => [t('repositories.title')]));
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
