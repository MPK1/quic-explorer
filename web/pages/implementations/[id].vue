<script setup lang="ts">
import type { Implementation, GithubRepo } from '~/types';

import impls_json from '~/../data/implementations.json';

const route = useRoute();
const id = computed(() => route.params.id as string)

const implementations: Implementation[] = impls_json.items;
const impl: Implementation | undefined = implementations.find(item => item.uuid === id.value);

const created_at = impl ? new Date(impl.created_at).toUTCString() : undefined;
const updated_at = (impl && impl.updated_at) ? new Date(impl.updated_at).toUTCString() : undefined;

const is_github_repo: boolean = impl ? /github\.com/.test(impl.repo_url) : false;
const repo_id = impl ? /[^/]*\/[^/]*$/.exec(impl.repo_url)?.[0] || "" : "";

const { pending: gh_pending, data: gh } = useFetch<GithubRepo>('https://api.github.com/repos/' + repo_id, {
  lazy: true,
  server: false
})

useHead({
  title: impl
        ? 'QUIC Explorer | ' + impl.name
        : 'Impl not found'
})

const links = [{
  label: 'Home',
  icon: 'i-heroicons-home',
  to: '/'
}, {
  label: 'Implementations',
  to: '/implementations'
}, {
  label: impl ? impl.name : ''
}]
</script>

<template>
  <div class="impl-view view">
    <UBreadcrumb v-if="impl" :links="links" class="mb-4"/>
    <template v-if="impl">

      <UCard>
        <template #header>
          <div class="flex justify-between">
            <h1 class="text-4xl font-bold inline-block">{{ impl.name }}</h1>
            <UButton class="justify-end" :to="impl.repo_url" target="_blank" icon="i-mdi-git" label="Go to repository" />
          </div>
        </template>

        <img v-if="impl.logo_url" id="logo" :src="impl.logo_url" />
        <h2 class="text-xl mb-2">General Information</h2>
        <ul class="meta">
          <li>
            <span class="label">Repository:</span> <UBadge color="gray" variant="solid">{{ impl.repo_url || '-' }}</UBadge>
          </li>
          <li>
            <span class="label">Maintainer:</span> <UBadge color="gray" variant="solid">{{ impl.maintainer || '-' }}</UBadge>
          </li>
          <li>
            <span class="label">Language:</span> <UBadge color="gray" variant="solid">{{ impl.language || '-' }}</UBadge>
          </li>
        </ul>
        <h2 class="text-xl my-2">Github Stats</h2>
        <ul class="meta" v-if="is_github_repo">
          <UButton icon="i-mdi-star-outline" class="mr-2 mb-2 cursor-default" color="gray">
            Stars <UBadge color="gray" variant="solid" :ui="{ rounded: 'rounded-full' }">{{ gh_pending || !gh ? "?" : gh.stargazers_count }}</UBadge>
          </UButton>
          <UButton icon="i-mdi-source-fork" class="mr-2 mb-2 cursor-default" color="gray">
            Forks <UBadge color="gray" variant="solid" :ui="{ rounded: 'rounded-full' }">{{ gh_pending || !gh ? "?" : gh.forks_count }}</UBadge>
          </UButton>
          <UButton icon="i-mdi-calendar" class="mr-2 mb-2 cursor-default" color="gray">
            Created <UBadge color="gray" variant="solid" :ui="{ rounded: 'rounded-full' }">{{ gh_pending || !gh ? "?" : new Date(gh.created_at).toUTCString() }}</UBadge>
          </UButton>
        </ul>

        <template #footer>
          <ul class="meta">
            <li>
              <span class="label">Implementation added:</span> <UBadge  class="badge" color="gray" variant="solid">{{ created_at || '?' }}</UBadge> by <UBadge class="badge" color="gray" variant="solid">{{ impl.created_by.split('<')[0].trim() || '?' }}</UBadge>
            </li>
            <li v-if="updated_at && impl.updated_by">
              <span class="label">Last update:</span> <UBadge class="badge" color="gray" variant="solid">{{ updated_at || '?' }}</UBadge> by <UBadge class="badge" color="gray" variant="solid">{{ impl.updated_by.split('<')[0].trim() || '?' }}</UBadge>
            </li>
          </ul>
        </template>
      </UCard>
      
    </template>
    <template v-else>
      <h1 class="text-4xl font-bold inline-block">Implementation not found!</h1>
    </template>
  </div>
</template>

<style lang="postcss">
.impl-view {
  background-color: #fff;
  box-sizing: border-box;
  padding: 2em 3em;
  min-height: 400px;

  .meta {
    list-style-type: none;
    padding: 0;
    margin-left: 0.5em;
  }

  .label {
    display: inline-block;
    font-weight: bold;
    min-width: 8em;
    margin: 0.25em 0;
  }
}

#logo {
  display: none;
  position: relative;
  max-width: 40%;
  min-height: 80px;
  max-height: 140px;
  top: 0;
  right: 0;
  clear: both;
  float: right;
  padding: 5px;
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
}

@media (min-width: 800px) {
  #logo {
    display: block;
  }
}
</style>