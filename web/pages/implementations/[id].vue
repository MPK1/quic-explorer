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

const gh_pending_1 = ref(true);
const gh_pending_2 = ref(true);
const gh_pending = ref(gh_pending_1 || gh_pending_2);

const { data: gh } = is_github_repo ? useFetch<GithubRepo>('https://api.github.com/repos/' + repo_id, {
  lazy: true,
  server: false,
  onResponse({ response }) {
    useFetch<GithubRepo>(response._data.commits_url.replace("{/sha}", "/" + response._data.default_branch), {
      server: false,
      onResponse({ response }) {
        const last_commit_date = new Date(response._data.commit.committer.date);
        if (gh.value) gh.value.last_commit = getRelativeTimeDiff(last_commit_date);
        gh_pending_1.value = false;
      },
    });
    useFetch<GithubRepo>(response._data.contributors_url + "?per_page=1", {
      server: false,
      onResponse({ response }) {
        if (response.ok && response.headers.get('link')) {
          if (gh.value) gh.value.contributors_count =  parseInt(response.headers.get('link').split(',').pop().split(';')[0].match(/.*page=(.*)>/)[1]);
        }
        gh_pending_2.value = false;
      }
    });
  }
}) : { data: ref(undefined) };

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
        <h2 class="text-xl my-2">Github Stats <span class="align-super text-xs">LIVE</span></h2>
        <ul class="meta flex flex-wrap" v-if="is_github_repo">
          <GithubBadge label="Stars" icon="i-mdi-star-outline" :pending="gh_pending" :gh="gh" :value="gh?.stargazers_count" />
          <GithubBadge label="Forks" icon="i-mdi-source-fork" :pending="gh_pending" :gh="gh" :value="gh?.forks_count" />
          <GithubBadge label="Contributors" icon="i-mdi-account-multiple" :pending="gh_pending" :gh="gh" :value="gh?.contributors_count" />
          <GithubBadge label="Last commit on default branch" icon="i-mdi-source-commit-end" :pending="gh_pending" :gh="gh" :value="gh?.last_commit" />
          <GithubBadge label="Created" icon="i-mdi-calendar" :pending="gh_pending" :gh="gh" :value="gh ? new Date(gh.created_at).toUTCString(): ''" />
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