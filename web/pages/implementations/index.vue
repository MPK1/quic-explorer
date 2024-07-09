<script setup lang="ts">
import type { Implementation, Feature, Entry } from "~/types";
import type { FormError, FormSubmitEvent } from "#ui/types";

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
    label: "Exclude entry if not set",
  },
  {
    value: "value-or-unset",
    label: "Include entry if not set",
  },
];

function select(row: Implementation) {
  return navigateTo("/implementations/" + row.uuid);
}

const q = ref("");
const { confirming, params } = useConfirm();
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
  console.dir(Object.values(filter));
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

const filteredRows = computed(() =>
  !q.value && !filters.value.length
    ? implementations
    : implementations.filter(
        (i) =>
          Object.entries(i)
            .filter(([key]) => searchableAttributes.includes(key))
            .map(([, value]) => value)
            .some(
              (value) =>
                !q.value ||
                String(value).toLowerCase().includes(q.value.toLowerCase()),
            ) &&
          filters.value.every((filter) => {
            const entry = entries.find(
              (e) =>
                e.implementation_uuid === i.uuid &&
                e.feature_uuid === filter.feature,
            );
            switch (filter.value_type) {
              case "boolean":
                switch (filter.mode) {
                  case "value-or-unset":
                    return !entry || entry.value === filter.value;
                  case "value":
                    return entry && entry.value === filter.value;
                  case "set":
                    return (entry && filter.value) || (!entry && !filter.value);
                }
                break;
              case "array":
                switch (filter.mode) {
                  case "value-or-unset":
                    if (!entry) {
                      return true;
                    }
                  // no break => fall through to 'value' case if entry exists
                  case "value":
                    if (!entry) {
                      return false;
                    }
                    if (filter.arraymode === "contains-all") {
                      return filter.value.every((v: any) =>
                        entry.value.includes(v),
                      );
                    } else if (filter.arraymode === "contains-one") {
                      return filter.value.some((v: any) =>
                        entry.value.includes(v),
                      );
                    }
                    break;
                  case "set":
                    return (entry && filter.value) || (!entry && !filter.value);
                }
                break;
            }
          }),
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
      class="flex justify-between px-3 py-3.5 border-bb border-gray-200 dark:border-gray-700"
    >
      <h1 class="text-2xl font-semibold">Implementations</h1>
      <div class="flex">
        <UButton
          label="Add Filter"
          class="mr-5 hidden md:block"
          @click="modalIsOpen = true"
        />
        <UInput class="" v-model="q" placeholder="Search..." />
      </div>
    </div>
    <div
      v-if="filters.length > 0"
      class="px-3 py-2 border-y border-gray-200 dark:border-gray-700"
    >
      Active Filters (click to remove):
      <UButton
        variant="outline"
        size="2xs"
        v-for="f in filters"
        class="mr-2 my-1"
        :label="f.label"
        @click="removeFilter(f)"
      />
    </div>
    <UTable
      class="mt-8"
      :columns="columns"
      :rows="filteredRows"
      @select="select"
    />
    <UModal v-model="modalIsOpen">
      <UCard
        class=""
        :ui="{
          ring: '',
          divide: 'divide-y divide-gray-100 dark:divide-gray-800',
        }"
      >
        <template #header>
          <h1 class="text-xl">Add Filter</h1>
        </template>

        <UForm
          :validate="validate"
          :state="state"
          class="space-y-4"
          @submit="onFilterCriteriaAdd"
        >
          <UFormGroup label="Feature" name="feature">
            <USelectMenu
              searchable
              searchable-placeholder="Search feature..."
              :search-attributes="['name', 'short_name', 'description']"
              placeholder="Select a feature"
              :options="
                features.filter((f) =>
                  ['boolean', 'array'].includes(f.value_type),
                )
              "
              v-model="state.feature"
              option-attribute="name"
            >
              <template #option="{ option: feature }">
                <span class="truncate font-mono"
                  >[{{ feature.short_name }}]</span
                ><span class="truncate">{{ feature.name }}</span>
              </template>
            </USelectMenu>
          </UFormGroup>

          <UFormGroup label="Mode" name="mode">
            <URadioGroup v-model="state.mode" :options="modes" key="key">
              <template #label="{ option }">
                <p>
                  <span class="font-bold">{{ option.value }}</span>
                  <span class="italic"> ({{ option.label }})</span>
                </p>
              </template>
            </URadioGroup>
          </UFormGroup>

          <UFormGroup
            v-if="state.feature && state.feature.value_type == 'array'"
            label="Array Mode"
            name="arraymode"
          >
            <URadioGroup
              v-model="state.arraymode"
              :options="[
                {
                  value: 'contains-one',
                  label: 'Contains one of the set values',
                },
                { value: 'contains-all', label: 'Contains all set values' },
              ]"
            >
            </URadioGroup>
          </UFormGroup>

          <UFormGroup
            v-if="state.feature && state.feature.value_type == 'boolean'"
            label="Value"
            name="value"
          >
            <URadioGroup
              v-model="state.value"
              :options="[
                { value: 1, label: 'Yes/True' },
                { value: 0, label: 'No/False' },
              ]"
            >
            </URadioGroup>
          </UFormGroup>

          <UFormGroup
            v-if="state.feature && state.feature.value_type == 'array'"
            label="Value"
            name="value"
          >
            <UInput
              placeholder="Enter one or more values, separated by commas"
              v-model="state.value"
            />
          </UFormGroup>

          <div class="flex justify-end space-x-2">
            <UButton color="red" variant="outline" @click="modalIsOpen = false"
              >Cancel</UButton
            >
            <UButton type="submit">Add Filter</UButton>
          </div>
        </UForm>
      </UCard>
    </UModal>
    <UModal v-model="confirming" :ui="{ width: 'sm:max-w-sm' }">
      <UCard>
        <div class="font-semibold mb-2">{{ params.title }}</div>
        <div>{{ params.message }}</div>
        <template #footer>
          <div class="flex justify-end space-x-2">
            <UButton color="white" @click="confirming = false">
              Cancel
            </UButton>
            <UButton color="red" variant="solid" @click="params.action">
              {{ params.label }}</UButton
            >
          </div>
        </template>
      </UCard>
    </UModal>
  </div>
</template>

<style lang="postcss"></style>
