<script setup lang="ts">
import type { GithubRepo } from '~/types';
defineProps<{
  label: string,
  icon: string,
  pending: Boolean,
  gh: GithubRepo | null,
  value: Object | undefined
}>()
</script>
<template>
    <template v-if="pending">
        <USkeleton class="inline-flex text-xs py-1 px-2 mr-2 mb-2 h-8 w-48" />
    </template>
    <template v-else>
        <UButton size="2xs" :icon="icon" class="mr-2 mb-2 cursor-default" color="gray">
            {{ label }} <UBadge color="gray" variant="solid" :ui="{ rounded: 'rounded-full' }">{{ pending || !gh ? "?" : value }}</UBadge>
        </UButton>
    </template>
</template>
