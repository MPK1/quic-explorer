<script setup lang="ts">
import type { Implementation, Feature, Entry } from "~/types";

import features_json from "~/../data/features.json";
import entries_json from "~/../data/entries.json";
import impls_json from "~/../data/implementations.json";

const route = useRoute();
const id = computed(() => route.params.id as string);

const implementations: Implementation[] = impls_json.items;

const features: Feature[] = features_json.items;
const feat: Feature | undefined = features.find(
  (item) => item.uuid === id.value,
);

if (!feat) {
  throw createError({
    statusCode: 404,
    statusMessage: "Feature not found",
    fatal: true,
  });
}

const entries: Entry[] = entries_json.items;
const relevant_entries: Entry[] = entries.filter(
  (item) => item.feature_uuid === id.value,
);
relevant_entries.forEach((entry) => {
  const impl = implementations.find(
    (item) => item.uuid === entry.implementation_uuid,
  );
  if (impl) {
    entry.implementation_name = impl.name;
  }

  entry.last_update = (entry.updated_at || entry.created_at).split("T")[0];
  entry.last_update_by = (entry.updated_by || entry.created_by)
    .split("<")[0]
    .trim();

  if (feat.value_type == "boolean") {
    entry.value_pretty = entry.value ? "✅" : "❌";
  } else if (feat.value_type == "array") {
    entry.value_pretty = entry.value.join(", ");
  } else if (feat.value_type == "object") {
    entry.value_pretty = JSON.stringify(entry.value, null, 2);
  } else {
    entry.value_pretty = entry.value;
  }
});

const created_at = new Date(feat.created_at).toUTCString();
const updated_at = feat.updated_at
  ? new Date(feat.updated_at).toUTCString()
  : undefined;

useHead({
  title: feat.name,
});

const { buildColumns } = useTableColumns();
const sorting = ref<{ id: string; desc: boolean }[]>([]);

const columns = [
  {
    label: "Implementation",
    key: "implementation_name",
    sortable: true,
    class: "w-1/4",
  },
  {
    label: "Value",
    key: "value",
    sortable: true,
  },
  {
    label: "Last Updated",
    key: "last_update",
    sortable: true,
    class: "w-1/4",
  },
  {
    label: "Source",
    key: "source",
    sortable: true,
    class: "w-1",
  },
];
const tableColumns = buildColumns(columns);

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
  {
    label: feat.name,
  },
];
</script>

<template>
  <div class="feat-view view">
    <UBreadcrumb :items="links" class="mb-4" />
    <UCard>
      <template #header>
        <div class="flex justify-between">
          <h1 class="text-3xl font-bold inline-block">{{ feat.name }}</h1>
        </div>
      </template>

      <h2 class="text-xl mb-2">General Information</h2>
      <ul class="meta">
        <li>
          <span class="label">Long Name:</span>
          <UBadge color="neutral" variant="subtle">
            {{ feat.name || "-" }}
          </UBadge>
        </li>
        <li>
          <span class="label">Short Name:</span>
          <UBadge color="neutral" variant="subtle">
            {{ feat.short_name || "-" }}
          </UBadge>
        </li>
        <li>
          <span class="label">Description:</span>
          <UBadge color="neutral" variant="subtle">
            {{ feat.description || "-" }}
          </UBadge>
        </li>
        <li>
          <span class="label">Value Type:</span>
          <UBadge color="neutral" variant="subtle">
            {{ feat.value_type || "-" }}
          </UBadge>
        </li>
        <li>
          <span class="label" v-if="feat.value_meta">Value Meta:</span>
          <pre
            v-if="feat.value_meta"
            class="ring-gray-300 ring-inset ring-1 text-gray-700 bg-gray-50 rounded-md text-xs p-2"
            v-html="JSON.stringify(feat.value_meta, null, 2)"
          ></pre>
        </li>
      </ul>

      <template #footer>
        <ul class="meta">
          <li>
            <span class="label pr-1">Feature created:</span>
            <UBadge class="badge" color="neutral" variant="subtle">
              {{ created_at || "?" }}
            </UBadge>
            by
            <UBadge class="badge" color="neutral" variant="subtle">
              {{ feat.created_by.split("<")[0].trim() || "?" }}
            </UBadge>
          </li>
          <li v-if="updated_at && feat.updated_by">
            <span class="label">Last update:</span>
            <UBadge class="badge" color="neutral" variant="subtle">
              {{ updated_at || "?" }}
            </UBadge>
            by
            <UBadge class="badge" color="neutral" variant="subtle">
              {{ feat.updated_by.split("<")[0].trim() || "?" }}
            </UBadge>
          </li>
        </ul>
      </template>
    </UCard>

    <UCard class="mt-8">
      <template #header>
        <div class="flex justify-between">
          <h1 class="text-2xl font-bold inline-block">Entries</h1>
        </div>
      </template>
      <UTable
        v-model:sorting="sorting"
        :data="relevant_entries"
        :columns="tableColumns"
      >
        <template #implementation_name-cell="{ row }">
          <NuxtLink
            :to="'/implementations/' + row.original.implementation_uuid"
          >
            {{ row.original.implementation_name }}
          </NuxtLink>
        </template>
        <template #source-cell="{ row }">
          {{ row.original.source }}
          <UTooltip :text="row.original.source_url" :content="{ side: 'left' }">
            <UButton
              v-if="row.original.source_url"
              class="ml-2"
              icon="i-mdi-link-variant"
              size="xs"
              color="neutral"
              variant="outline"
              :to="row.original.source_url"
              target="_blank"
            />
          </UTooltip>
        </template>
        <template #last_update-cell="{ row }">
          <UTooltip
            :text="'by ' + row.original.last_update_by"
            :content="{ side: 'right' }"
          >
            {{ row.original.last_update }}
          </UTooltip>
        </template>
        <template #value-cell="{ row }">
          <template v-if="row.original.comment">
            <UPopover mode="hover">
              <span>{{ row.original.value_pretty }}</span
              ><UBadge class="badge ml-2" color="neutral" variant="solid"
                >Hover for more details</UBadge
              >
              <template #content>
                <div class="p-4">
                  {{ row.original.comment }}
                </div>
              </template>
            </UPopover>
          </template>
          <template v-else>
            {{ row.original.value_pretty }}
          </template>
        </template>
      </UTable>
    </UCard>
  </div>
</template>

<style lang="postcss">
.feat-view {
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
</style>
