<script setup lang="ts">
import type { Implementation } from "~/types";

import data from "~/../data/implementations.json";

const route = useRoute();

const implementations: Implementation[] = data.items;

const links = [
  {
    label: "Home",
    icon: "i-heroicons-home",
    to: "/",
  },
  {
    label: "Implementations",
    to: "/implementations",
  },
];

const columns = [
  {
    label: "Name",
    key: "name",
    sortable: true,
  },
  {
    label: "Repository",
    key: "repo_url",
    sortable: true,
  },
  {
    label: "Maintainer",
    key: "maintainer",
    sortable: true,
  },
  {
    label: "Language",
    key: "language",
    sortable: true,
  },
];

function select(row: Implementation) {
  return navigateTo("/implementations/" + row.uuid);
}

const q = ref("");

const filteredRows = computed(() =>
  !q.value
    ? implementations
    : implementations
        .map(({ name, maintainer, language, repo_url }) => ({
          name,
          maintainer,
          language,
          repo_url,
        }))
        .filter((i) =>
          Object.values(i).some((value) =>
            String(value).toLowerCase().includes(q.value.toLowerCase()),
          ),
        ),
);

useHead({
  title: "QUIC Explorer | Implementations",
});
</script>

<template>
  <div class="view">
    <UBreadcrumb :links="links" class="mb-4" />
    <div
      class="flex justify-between px-3 py-3.5 border-b border-gray-200 dark:border-gray-700"
    >
      <h1 class="text-2xl font-semibold">Implementations</h1>
      <UInput class="" v-model="q" placeholder="Search..." />
    </div>
    <UTable :columns="columns" :rows="filteredRows" @select="select" />
  </div>
</template>

<style lang="postcss"></style>
