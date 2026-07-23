<script setup lang="ts">
import type { Implementation, Feature, Entry } from "~/types";

import impls_json from "~/../data/implementations.json";
import features_json from "~/../data/features.json";
import entries_json from "~/../data/entries.json";

const implementations: Implementation[] = impls_json.items;
const features: Feature[] = features_json.items;
const entries: Entry[] = entries_json.items;

const links = [
  {
    label: "Home",
    icon: "i-heroicons-home",
    to: "/",
  },
  {
    label: "Matrix",
    to: "/matrix",
  },
];

useHead({
  title: "Feature Matrix",
});
useSeoMeta({
  description: `A feature-support matrix for ${implementations.length} QUIC implementations across ${features.length} tracked features, with sourced data for every entry.`,
});

useSchemaOrg([
  defineBreadcrumb({
    itemListElement: links.map((l) => ({ name: l.label, item: l.to })),
  }),
]);

const entryLookup = new Map<string, Entry>();
for (const entry of entries) {
  entryLookup.set(`${entry.implementation_uuid}__${entry.feature_uuid}`, entry);
}

type CellStatus = "yes" | "no" | "unknown";

const symbols: Record<CellStatus, string> = {
  yes: "✅",
  no: "❌",
  unknown: "❓",
};

interface Cell {
  status: CellStatus;
  entry?: Entry;
  title: string;
  advanced: boolean;
}

function describeCell(
  impl: Implementation,
  feature: Feature,
  entry: Entry | undefined,
  status: CellStatus,
): string {
  if (!entry) {
    return `${impl.name} — ${feature.name}: no data yet`;
  }
  const parts: string[] = [`${impl.name} — ${feature.name}`];
  if (feature.value_type === "array") {
    const values = entry.value as any[];
    parts.push(values && values.length ? values.join(", ") : "none known");
  } else {
    parts.push(status === "yes" ? "Supported" : "Not supported");
  }
  if (entry.comment) {
    parts.push(entry.comment);
  }
  parts.push(`Source: ${entry.source}`);
  return parts.join("\n");
}

function getCell(impl: Implementation, feature: Feature): Cell {
  const entry = entryLookup.get(`${impl.uuid}__${feature.uuid}`);
  let status: CellStatus = "unknown";
  if (entry) {
    if (feature.value_type === "array") {
      const values = entry.value as any[];
      status = values && values.length ? "yes" : "no";
    } else {
      status = entry.value ? "yes" : "no";
    }
  }
  const advanced = !!entry && (feature.value_type === "array" || !!entry.comment);
  return {
    status,
    entry,
    title: describeCell(impl, feature, entry, status),
    advanced,
  };
}

function arrayValues(entry: Entry): any[] {
  const values = entry.value as any[];
  return Array.isArray(values) ? values : [];
}

const selectedImplementations = ref<Implementation[]>([...implementations]);
const selectedFeatures = ref<Feature[]>([...features]);

const visibleImplementations = computed(() => {
  const selected = new Set(selectedImplementations.value.map((i) => i.uuid));
  return implementations.filter((impl) => selected.has(impl.uuid));
});

const visibleFeatures = computed(() => {
  const selected = new Set(selectedFeatures.value.map((f) => f.uuid));
  return features.filter((feature) => selected.has(feature.uuid));
});

const isFiltered = computed(
  () =>
    visibleImplementations.value.length < implementations.length ||
    visibleFeatures.value.length < features.length,
);

function selectAllImplementations() {
  selectedImplementations.value = [...implementations];
}
function deselectAllImplementations() {
  selectedImplementations.value = [];
}
function selectAllFeatures() {
  selectedFeatures.value = [...features];
}
function deselectAllFeatures() {
  selectedFeatures.value = [];
}

const showArraysInline = ref(false);
const showImplementationMetadata = ref(false);

const isFullscreen = useState<boolean>("matrix-fullscreen", () => false);

onBeforeRouteLeave(() => {
  isFullscreen.value = false;
});

const matrix = computed(() =>
  visibleImplementations.value.map((impl) => ({
    impl,
    cells: visibleFeatures.value.map((feature) => ({
      feature,
      cell: getCell(impl, feature),
    })),
  })),
);
</script>

<template>
  <div
    :class="
      isFullscreen
        ? 'fixed inset-0 z-50 overflow-auto bg-white dark:bg-gray-900'
        : 'view'
    "
  >
    <template v-if="!isFullscreen">
      <UBreadcrumb :items="links" class="mb-4" />
      <div
        class="flex justify-between px-3 py-3.5 border-b border-gray-200 dark:border-gray-700"
      >
        <h1 class="text-2xl font-semibold">Feature Matrix</h1>
        <UButton
          variant="outline"
          color="neutral"
          size="sm"
          icon="i-heroicons-arrows-pointing-out"
          label="Fullscreen"
          class="print:hidden"
          @click="isFullscreen = true"
        />
      </div>
    </template>
    <div v-if="!isFullscreen" class="flex flex-wrap items-start gap-4 px-3 py-3.5">
      <div class="min-w-[220px] flex-1">
        <div class="mb-1 flex items-center justify-between">
          <label class="block text-xs font-medium text-gray-500 dark:text-gray-400">
            Implementations
          </label>
          <div class="flex gap-2 text-xs">
            <button
              type="button"
              class="text-primary-500 hover:underline"
              @click="selectAllImplementations"
            >
              Select all
            </button>
            <button
              type="button"
              class="text-primary-500 hover:underline"
              @click="deselectAllImplementations"
            >
              Deselect all
            </button>
          </div>
        </div>
        <USelectMenu
          v-model="selectedImplementations"
          :items="implementations"
          label-key="name"
          multiple
          :search-input="{ placeholder: 'Search implementations...' }"
          placeholder="None selected"
          class="w-full"
        />
      </div>
      <div class="min-w-[220px] flex-1">
        <div class="mb-1 flex items-center justify-between">
          <label class="block text-xs font-medium text-gray-500 dark:text-gray-400">
            Features
          </label>
          <div class="flex gap-2 text-xs">
            <button
              type="button"
              class="text-primary-500 hover:underline"
              @click="selectAllFeatures"
            >
              Select all
            </button>
            <button
              type="button"
              class="text-primary-500 hover:underline"
              @click="deselectAllFeatures"
            >
              Deselect all
            </button>
          </div>
        </div>
        <USelectMenu
          v-model="selectedFeatures"
          :items="features"
          label-key="name"
          multiple
          :search-input="{ placeholder: 'Search features...' }"
          placeholder="None selected"
          class="w-full"
        >
          <template #item="{ item: feature }">
            <span class="truncate font-mono">[{{ feature.short_name }}]</span>
            <span class="truncate">{{ feature.name }}</span>
          </template>
        </USelectMenu>
      </div>
    </div>
    <div v-if="!isFullscreen" class="flex flex-col gap-1 px-3 py-1">
      <UCheckbox
        v-model="showArraysInline"
        label="Show list values inline instead of ℹ️"
      />
      <UCheckbox
        v-model="showImplementationMetadata"
        label="Show implementation metadata in matrix"
      />
    </div>
    <p v-if="!isFullscreen" class="px-3 py-3 text-sm text-gray-500 dark:text-gray-400">
      Legend: ✅ Supported &nbsp;·&nbsp; ❌ Not supported &nbsp;·&nbsp; ❓ No data yet.
      <br>
      Hover a cell for details, click it to jump to its source.
      <span v-if="isFiltered">
        &nbsp;·&nbsp; Showing {{ visibleImplementations.length }} of
        {{ implementations.length }} implementations,
        {{ visibleFeatures.length }} of {{ features.length }} features.
      </span>
    </p>
    <UButton
      v-if="isFullscreen"
      class="sticky left-3 top-3 z-20 m-3 print:hidden"
      variant="solid"
      color="neutral"
      size="sm"
      icon="i-heroicons-arrows-pointing-in"
      label="Exit fullscreen"
      @click="isFullscreen = false"
    />
    <div class="overflow-x-auto px-3 pb-6">
      <table class="w-full border-collapse text-sm">
        <thead>
          <tr>
            <th
              class="sticky left-0 z-10 border border-gray-200 bg-gray-50 px-3 py-2 text-left dark:border-gray-700 dark:bg-gray-800"
            >
              Implementation
            </th>
            <template v-if="showImplementationMetadata">
              <th
                class="border border-gray-200 bg-gray-50 px-3 py-2 text-left dark:border-gray-700 dark:bg-gray-800"
              >
                Language
              </th>
              <th
                class="border border-gray-200 bg-gray-50 px-3 py-2 text-left dark:border-gray-700 dark:bg-gray-800"
              >
                License
              </th>
            </template>
            <th
              v-for="feature in visibleFeatures"
              :key="feature.uuid"
              :title="feature.name + ': ' + feature.description"
              class="border border-gray-200 bg-gray-50 px-2 py-2 font-mono text-xs dark:border-gray-700 dark:bg-gray-800"
            >
              {{ feature.short_name }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in matrix" :key="row.impl.uuid">
            <th
              class="sticky left-0 z-10 border border-gray-200 bg-white px-3 py-1.5 text-left font-medium dark:border-gray-700 dark:bg-gray-900"
            >
              <NuxtLink
                :to="'/implementations/' + row.impl.uuid"
                class="hover:underline"
              >
                {{ row.impl.name }}
              </NuxtLink>
            </th>
            <template v-if="showImplementationMetadata">
              <td
                class="border border-gray-200 px-3 py-1.5 text-left whitespace-nowrap dark:border-gray-700"
              >
                {{ row.impl.language }}
              </td>
              <td
                class="border border-gray-200 px-3 py-1.5 text-left whitespace-nowrap dark:border-gray-700"
              >
                {{ row.impl.license }}
              </td>
            </template>
            <td
              v-for="c in row.cells"
              :key="c.feature.uuid"
              class="border border-gray-200 text-center dark:border-gray-700"
            >
              <a
                v-if="
                  showArraysInline &&
                  c.feature.value_type === 'array' &&
                  c.cell.entry
                "
                :href="c.cell.entry.source_url"
                target="_blank"
                rel="noopener noreferrer"
                :title="c.cell.title"
                class="inline-block w-full whitespace-normal px-2 py-1 text-xs hover:bg-gray-100 dark:hover:bg-gray-800"
              >
                {{
                  arrayValues(c.cell.entry).length
                    ? arrayValues(c.cell.entry).join(", ")
                    : "—"
                }}
              </a>
              <UPopover
                v-else-if="c.cell.advanced"
                mode="hover"
                :content="{ side: 'top' }"
              >
                <a
                  :href="c.cell.entry!.source_url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="inline-block w-full px-2 py-1 hover:bg-gray-100 dark:hover:bg-gray-800"
                >
                  {{ c.feature.value_type === "array" ? "ℹ️" : symbols[c.cell.status] }}
                </a>
                <template #content>
                  <div class="max-w-xs p-3 text-left text-sm">
                    <div class="mb-1 font-semibold">{{ c.feature.name }}</div>
                    <ul
                      v-if="
                        c.feature.value_type === 'array' &&
                        arrayValues(c.cell.entry!).length
                      "
                      class="mb-2 list-inside list-disc"
                    >
                      <li v-for="v in arrayValues(c.cell.entry!)" :key="v">
                        {{ v }}
                      </li>
                    </ul>
                    <div
                      v-else-if="c.feature.value_type === 'array'"
                      class="mb-2 italic text-gray-500"
                    >
                      No values recorded
                    </div>
                    <div v-else class="mb-2">
                      {{ c.cell.entry!.value ? "Supported" : "Not supported" }}
                    </div>
                    <div
                      v-if="c.cell.entry!.comment"
                      class="mb-2 text-gray-500"
                    >
                      {{ c.cell.entry!.comment }}
                    </div>
                    <a
                      :href="c.cell.entry!.source_url"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="text-xs text-primary-500 hover:underline"
                      >Source: {{ c.cell.entry!.source }}</a
                    >
                  </div>
                </template>
              </UPopover>
              <a
                v-else-if="c.cell.entry"
                :href="c.cell.entry.source_url"
                target="_blank"
                rel="noopener noreferrer"
                :title="c.cell.title"
                class="inline-block w-full px-2 py-1 hover:bg-gray-100 dark:hover:bg-gray-800"
              >
                {{ symbols[c.cell.status] }}
              </a>
              <span
                v-else
                :title="c.cell.title"
                class="inline-block w-full px-2 py-1 text-gray-300 dark:text-gray-600"
              >
                {{ symbols[c.cell.status] }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style lang="postcss"></style>
