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
  return navigateTo("/features/" + row.slug);
}

const searchableAttributes = ["name", "short_name", "description"];

useHead({
  title: "Features",
});
useSeoMeta({
  description: `Browse ${features.length} QUIC protocol features and extensions — see which open-source implementations have tracked data for each.`,
});

useSchemaOrg([
  defineBreadcrumb({
    itemListElement: links.map((l) => ({ name: l.label, item: l.to })),
  }),
]);
</script>

<template>
  <div class="view">
    <UBreadcrumb :items="links" class="mb-4" />
    <FilterableTable
      title="Features"
      :columns="columns"
      :rows="features"
      :searchable-attributes="searchableAttributes"
      :select="select"
    >
      <template #short_name-cell="{ row }">
        <span class="font-mono">{{ row.original.short_name }}</span>
      </template>
      <template #value_type-cell="{ row }">
        <span class="font-mono">{{ row.original.value_type }}</span>
      </template>
    </FilterableTable>
  </div>
</template>

<style lang="postcss"></style>
