<script setup lang="ts">

useHead({
  title: 'QUIC Explorer'
})
</script>

<template>
  <div class="view">
    <h1 class="text-3xl mb-6">Welcome to QUIC Explorer!</h1>
    This website is still in beta stage and not all features are available right now.
    However, we are working on it and will add more features soon™️.
    <br class="mb-4">
    You can already check out the
    <NuxtLink to="/implementations">
      <UButton size="xs" color="gray" variant="outline">implementations table</UButton>
    </NuxtLink>
    and the 
    <NuxtLink to="/features">
      <UButton size="xs" color="gray" variant="outline">features list</UButton>
    </NuxtLink>
    . Click on a row to see more details.
  </div>
</template>

<style lang="postcss">
</style>
