<script setup lang="ts">

useHead({
  title: 'QUIC Explorer'
})
</script>

<template>
  <div class="view">
    <h1 class="text-3xl mb-6">Welcome to QUIC Explorer!</h1>
    This website is still in beta stage and only a few features are available right now.
    However, we are working on it and will add more features soon.
    <br class="mb-4">
    You can already check out the
    <NuxtLink to="/implementations">
      <UButton color="gray" variant="outline">implementations table</UButton>
    </NuxtLink>
  </div>
</template>

<style lang="postcss">
</style>