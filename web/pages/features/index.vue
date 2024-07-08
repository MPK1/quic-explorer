<script setup lang="ts">
import type { Feature } from "~/types";

import data from "~/../data/features.json";

const route = useRoute();

const features: Feature[] = data.items;

const links = [
  {
    label: "Home",
    icon: "i-heroicons-home",
    to: "/",
  },
  {
    label: "Features",
    to: "/features",
  },
];

const columns = [
  {
    label: "Key",
    key: "short_name",
    sortable: true,
  },
  {
    label: "Feature Name",
    key: "name",
    sortable: true,
  },
  {
    label: "Description",
    key: "description",
    sortable: false,
  },
];

function select(row: Feature) {
  return navigateTo("/features/" + row.uuid);
}

const q = ref("");

const filteredRows = computed(() => {
  if (!q.value) {
    return features;
  }

  return features.filter((f) => {
    return Object.values(f).some((value) => {
      return String(value).toLowerCase().includes(q.value.toLowerCase());
    });
  });
});

useHead({
  title: "QUIC Explorer | Features",
});
</script>

<template>
  <div class="view">
    <UBreadcrumb :links="links" class="mb-4" />
    <div
      class="flex justify-between px-3 py-3.5 border-b border-gray-200 dark:border-gray-700"
    >
      <h1 class="text-2xl font-semibold">Features</h1>
      <UInput class="" v-model="q" placeholder="Filter..." />
    </div>
    <UTable :columns="columns" :rows="filteredRows" @select="select" />
  </div>
</template>

<style lang="postcss"></style>
