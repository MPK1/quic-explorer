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
    label: "Type",
    key: "value_type",
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

const searchableAttributes = ["name", "short_name", "description"];

useHead({
  title: "QUIC Explorer | Features",
});
</script>

<template>
  <div class="view">
    <UBreadcrumb :links="links" class="mb-4" />
    <FilterableTable
      title="Features"
      :columns="columns"
      :rows="features"
      :searchable-attributes="searchableAttributes"
      :select="select"
    >
      <template #short_name-data="{ row }">
        <span class="font-mono">{{ row.short_name }}</span>
      </template>
      <template #value_type-data="{ row }">
        <span class="font-mono">{{ row.value_type }}</span>
      </template>
    </FilterableTable>
  </div>
</template>

<style lang="postcss"></style>
