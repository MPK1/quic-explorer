<script setup lang="ts">
import type { Feature, Entry } from '~/types';

import features_json from '~/../data/features.json';
import entries_json from '~/../data/entries.json';
import impls_json from '~/../data/implementations.json';

const route = useRoute();
const id = computed(() => route.params.id as string)

const implementations: Implementation[] = impls_json.items;

const features: Feature[] = features_json.items;
const feat: Feature | undefined = features.find(item => item.uuid === id.value);

const entries: Entry[] = entries_json.items;
const relevant_entries: Entry[] = entries.filter(item => item.feature_uuid === id.value);
relevant_entries.forEach(entry => {
  const impl = implementations.find(item => item.uuid === entry.implementation_uuid);
  if (impl) {
    entry.implementation_name = impl.name;
  }
  const last_update = entry.updated_at || entry.created_at;
  entry.last_update = last_update.split('T')[0];
  if (feat.value_type == 'boolean') {
    entry.value_pretty = entry.value ? '✅' : '❌';
  } else if (feat.value_type == 'array') {
    entry.value_pretty = entry.value.join(', ');
  } else if (feat.value_type == 'object') {
    entry.value_pretty = JSON.stringify(entry.value, null, 2);
  } else {
    entry.value_pretty = entry.value;
  }
})

const created_at = feat ? new Date(feat.created_at).toUTCString() : undefined;
const updated_at = (feat && feat.updated_at) ? new Date(feat.updated_at).toUTCString() : undefined;

useHead({
  title: feat
        ? 'QUIC Explorer | ' + feat.name
        : 'Feat not found'
})

const columns = [
  {
    label: 'Implementation',
    key: 'implementation_name',
    sortable: true,
    class: "w-1/4"
  },
  {
    label: 'Value',
    key: 'value',
    sortable: true
  },
  {
    label: 'Last Updated',
    key: 'last_update',
    sortable: true,
    class: "w-1/4"
  },
  {
    label: 'Source',
    key: 'source',
    sortable: true,
    class: "w-1"
  }
]

const links = [{
  label: 'Home',
  icon: 'i-heroicons-home',
  to: '/'
}, {
  label: 'Features',
  to: '/features'
}, {
  label: feat ? feat.name : ''
}]
</script>

<template>
  <div class="feat-view view">
    <UBreadcrumb v-if="feat" :links="links" class="mb-4"/>
    <template v-if="feat">

      <UCard>
        <template #header>
          <div class="flex justify-between">
            <h1 class="text-3xl font-bold inline-block">{{ feat.name }}</h1>
          </div>
        </template>

        <h2 class="text-xl mb-2">General Information</h2>
        <ul class="meta">
          <li>
            <span class="label">Long Name:</span> <UBadge color="gray" variant="solid">{{ feat.name || '-' }}</UBadge>
          </li>
          <li>
            <span class="label">Short Name:</span> <UBadge color="gray" variant="solid">{{ feat.short_name || '-' }}</UBadge>
          </li>
          <li>
            <span class="label">Description:</span> <UBadge color="gray" variant="solid">{{ feat.description || '-' }}</UBadge>
          </li>
          <li>
            <span class="label">Value Type:</span> <UBadge color="gray" variant="solid">{{ feat.value_type || '-' }}</UBadge>
          </li>
          <li>
            <span class="label" v-if="feat.value_meta">Value Meta:</span> <pre v-if="feat.value_meta" class="ring-gray-300 ring-inset ring-1 text-gray-700 bg-gray-50 rounded-md text-xs p-2" v-html="JSON.stringify(feat.value_meta, null, 2)"></pre>
          </li>
        </ul>

        <template #footer>
          <ul class="meta">
            <li>
              <span class="label">Feature created:</span> <UBadge  class="badge" color="gray" variant="solid">{{ created_at || '?' }}</UBadge> by <UBadge class="badge" color="gray" variant="solid">{{ feat.created_by.split('<')[0].trim() || '?' }}</UBadge>
            </li>
            <li v-if="updated_at && feat.updated_by">
              <span class="label">Last update:</span> <UBadge class="badge" color="gray" variant="solid">{{ updated_at || '?' }}</UBadge> by <UBadge class="badge" color="gray" variant="solid">{{ feat.updated_by.split('<')[0].trim() || '?' }}</UBadge>
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
        <UTable :rows="relevant_entries" :columns="columns">
        <template #implementation_name-data="{ row }">
          <NuxtLink :to="'/implementations/' + row.implementation_uuid">{{ row.implementation_name }}</NuxtLink>
        </template>
        <template #source-data="{ row }">
          {{ row.source }}
          <UTooltip :text="row.source_url" :popper="{ placement: 'left' }">
            <UButton
              v-if="row.source_url"
              class="ml-2"
              icon="i-mdi-link-variant"
              size="2xs" color="gray"
              variant="outline"
              :to="row.source_url" target="_blank"
            />
          </UTooltip>
        </template>
        <template #value-data="{ row }">
          <template v-if="row.comment">
            <UPopover mode="hover">
              <span>{{ row.value_pretty }}</span><UBadge class="badge ml-2" color="gray" variant="solid">Hover for more details</UBadge>
              <template #panel>
                <div class="p-4">
                  {{ row.comment }}
                </div>
              </template>
            </UPopover>
          </template>
          <template v-else>
            {{ row.value_pretty }}
          </template>
        </template>
        </UTable>
      </UCard>
      
    </template>
    <template v-else>
      <h1 class="text-4xl font-bold inline-block">Feature not found!</h1>
    </template>
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