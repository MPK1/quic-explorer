<script setup lang="ts">
import type { Implementation, Feature, Entry } from "~/types";
import type { FormError, FormSubmitEvent } from "@nuxt/ui";

import impls_json from "~/../data/implementations.json";
import features_json from "~/../data/features.json";
import entries_json from "~/../data/entries.json";

const route = useRoute();

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

const modes = [
  {
    value: "value",
    label: "value",
    description: "Exclude entry if not set",
  },
  {
    value: "value-or-unset",
    label: "value-or-unset",
    description: "Include entry if not set",
  },
];

function select(row: Implementation) {
  return navigateTo("/implementations/" + row.uuid);
}

const { confirming, params } = useConfirm();
const { filterByFeatures } = useFeatureFilter();
const filters = ref<any[]>([]);
const modalIsOpen = ref(false);

const state = reactive({
  feature: undefined,
  mode: undefined,
  arraymode: undefined,
  value: undefined,
});

const validate = (state: any): FormError[] => {
  const errors = [];
  if (!state.feature) errors.push({ path: "feature", message: "Required" });
  if (!state.mode) errors.push({ path: "mode", message: "Required" });
  if (state.value == undefined)
    errors.push({ path: "value", message: "Required" });
  return errors;
};

async function removeFilter(f: any) {
  useConfirm().confirm("Remove Filter", "Are you sure?", "Remove", () => {
    filters.value = filters.value.filter((filter) => filter !== f);
    confirming.value = false;
  });
}

async function onFilterCriteriaAdd(event: FormSubmitEvent<any>) {
  const { feature, value, arraymode, mode } = event.data;
  const { value_type, name, uuid } = feature;

  let label = "";
  let filter = {
    label: "",
    feature: uuid,
    mode,
    value_type,
    value: null,
  };

  if (value_type === "array") {
    const values = String(value)
      .split(",")
      .map((v) => v.trim());
    label = `${name} contains one of ${values.join(", ")}`;

    if (arraymode === "contains-all") {
      label = `${name} contains all of ${values.join(", ")}`;
    }
    if (mode === "value-or-unset") {
      label += " or is unset";
    }

    filter = {
      ...filter,
      label,
      arraymode,
      value: values,
    };
  } else if (value_type === "boolean") {
    const val = value == 1;
    label = `${name} is ${val}`;

    if (mode === "value-or-unset") {
      label += " or unset";
    }

    filter = {
      ...filter,
      label,
      value: val,
    };
  }
  if (
    !filters.value.some((f) => JSON.stringify(f) === JSON.stringify(filter))
  ) {
    filters.value.push(filter);
  } else {
    alert("Filter already exists! Nothing added.");
  }
  modalIsOpen.value = false;
}

const searchableAttributes = ["name", "maintainer", "language", "repo_url"];

const featureFilteredRows = computed(() =>
  filterByFeatures(implementations, entries, filters.value),
);

useHead({
  title: "Implementations",
});
</script>

<template>
  <div class="view">
    <UBreadcrumb :items="links" class="mb-4" />
    <div
      v-if="filters.length > 0"
      class="px-3 py-2 border-y border-gray-200 dark:border-gray-700"
    >
      Active Filters (click to remove):
      <UButton
        variant="outline"
        color="neutral"
        size="xs"
        v-for="f in filters"
        class="mr-2 my-1"
        :label="f.label"
        @click="removeFilter(f)"
      />
    </div>
    <FilterableTable
      title="Implementations"
      :columns="columns"
      :rows="featureFilteredRows"
      :searchable-attributes="searchableAttributes"
      :select="select"
    >
      <template #actions>
        <UButton
          label="Add Filter"
          class="mr-5 hidden md:block"
          @click="modalIsOpen = true"
        />
      </template>
    </FilterableTable>
    <UModal v-model:open="modalIsOpen" title="Add Filter">
      <template #body>
        <UForm
          :validate="validate"
          :state="state"
          class="space-y-4"
          @submit="onFilterCriteriaAdd"
        >
          <UFormField label="Feature" name="feature">
            <USelectMenu
              :search-input="{ placeholder: 'Search feature...' }"
              placeholder="Select a feature"
              :items="
                features.filter((f) =>
                  ['boolean', 'array'].includes(f.value_type),
                )
              "
              v-model="state.feature"
              label-key="name"
              class="w-full"
            >
              <template #item="{ item: feature }">
                <span class="truncate font-mono"
                  >[{{ feature.short_name }}]</span
                ><span class="truncate">{{ feature.name }}</span>
              </template>
            </USelectMenu>
          </UFormField>

          <UFormField label="Mode" name="mode">
            <URadioGroup v-model="state.mode" :items="modes" />
          </UFormField>

          <UFormField
            v-if="state.feature && state.feature.value_type == 'array'"
            label="Array Mode"
            name="arraymode"
          >
            <URadioGroup
              v-model="state.arraymode"
              :items="[
                {
                  value: 'contains-one',
                  label: 'Contains one of the set values',
                },
                { value: 'contains-all', label: 'Contains all set values' },
              ]"
            />
          </UFormField>

          <UFormField
            v-if="state.feature && state.feature.value_type == 'boolean'"
            label="Value"
            name="value"
          >
            <URadioGroup
              v-model="state.value"
              :items="[
                { value: 1, label: 'Yes/True' },
                { value: 0, label: 'No/False' },
              ]"
            />
          </UFormField>

          <UFormField
            v-if="state.feature && state.feature.value_type == 'array'"
            label="Value"
            name="value"
          >
            <UInput
              placeholder="Enter one or more values, separated by commas"
              v-model="state.value"
              class="w-full"
            />
          </UFormField>

          <div class="flex justify-end space-x-2">
            <UButton
              color="error"
              variant="outline"
              @click="modalIsOpen = false"
              >Cancel</UButton
            >
            <UButton type="submit">Add Filter</UButton>
          </div>
        </UForm>
      </template>
    </UModal>
    <UModal
      v-model:open="confirming"
      :title="params.title"
      :ui="{ content: 'sm:max-w-sm' }"
    >
      <template #body>
        <div>{{ params.message }}</div>
      </template>
      <template #footer>
        <div class="flex justify-end space-x-2 w-full">
          <UButton color="neutral" variant="outline" @click="confirming = false">
            Cancel
          </UButton>
          <UButton color="error" variant="solid" @click="params.action">
            {{ params.label }}</UButton
          >
        </div>
      </template>
    </UModal>
  </div>
</template>

<style lang="postcss"></style>
