<script setup lang="ts">
const { data: renderDateTime } = useAsyncData('renderDateTime', async () => {
  const dateTime = new Date().toUTCString()
  return dateTime
})
const { data: commitHash } = useAsyncData('commitHash', async () => {
  return useRuntimeConfig().gitCommitHash
})
</script>
<template>
Version Information: Commit <a class="text-white" target="_blank" :href="'https://github.com/MPK1/quic-explorer/tree/' + commitHash"><code>{{ commitHash }}</code></a> rendered on {{ renderDateTime }}
</template>
