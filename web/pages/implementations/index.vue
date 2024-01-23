<script setup lang="ts">
import type { Implementation } from '~/types';

import data from '~/../data/implementations.json';

const route = useRoute()

const implementations: Implementation[] = data.items;

const links = [{
  label: 'Home',
  icon: 'i-heroicons-home',
  to: '/'
}, {
  label: 'Implementations',
  to: '/implementations'
}]

const columns = [
  {
    label: 'Name',
    key: 'name',
    sortable: true
  },
  {
    label: 'Repository',
    key: 'repo_url',
    sortable: true
  },
  {
    label: 'Maintainer',
    key: 'maintainer',
    sortable: true
  },
  {
    label: 'Language',
    key: 'language',
    sortable: true
  }
]

function select (row: Implementation) {
  return navigateTo('/implementations/' + row.uuid)
}

useHead({
  title: 'QUIC Explorer | Implementations'
})
</script>

<template>
  <div class="view">
    <UBreadcrumb :links="links" class="mb-4"/>
    <UTable :columns="columns" :rows="implementations" @select="select" />
  </div>
</template>

<style lang="postcss">
</style>