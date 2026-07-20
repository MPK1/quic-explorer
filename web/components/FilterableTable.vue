<script setup lang="ts">
const props = defineProps<{
  title: string;
  columns: any[];
  rows: { [key: string]: any }[];
  searchableAttributes: string[];
  select?: (row: any) => any;
}>();

const q = ref("");

const filteredRows = computed(() => {
  if (!q.value) {
    return props.rows;
  }
  const needle = q.value.toLowerCase();
  return props.rows.filter((row) =>
    props.searchableAttributes.some((attr) =>
      String(row[attr] ?? "")
        .toLowerCase()
        .includes(needle),
    ),
  );
});
</script>

<template>
  <div>
    <div
      class="flex justify-between px-3 py-3.5 border-b border-gray-200 dark:border-gray-700"
    >
      <h1 class="text-2xl font-semibold">{{ title }}</h1>
      <div class="flex">
        <slot name="actions" />
        <UInput v-model="q" placeholder="Search..." />
      </div>
    </div>
    <UTable :columns="columns" :rows="filteredRows" @select="select">
      <template v-for="(_, name) in $slots" #[name]="slotProps">
        <slot :name="name" v-bind="slotProps ?? {}" />
      </template>
    </UTable>
  </div>
</template>

<style></style>
