<script setup lang="ts">

useHead({
  title: 'QUIC Explorer'
})
</script>

<template>
  <div class="view">
    <div class="w-full block">
      <img class="w-1/6 m-auto mb-6" src="public/favicon.png">
    </div>
    <h1 class="text-4xl font-bold text-center mb-6">Welcome to QUIC Explorer!</h1>
    QUIC Explorer helps you finding the right QUIC library for your project or research.
    <br><br>This website is still in beta stage and not all features are available right now.
    <br>We are working on it and will add more features soon™️.
    <br class="mb-4">
    <h1 class="text-xl font-bold my-2">How To Use</h1>
    If you want to browse a list of available open-source QUIC implementations, check out the
    <UButton class="cursor-pointer" to="/implementations" size="xs" color="gray" variant="outline">implementations table</UButton>
    .
    <br class="mb-4">
    If you are searching for a QUIC implementation with support for a specific extension or feature, check out the
    <UButton class="cursor-pointer" to="/features" size="xs" color="gray" variant="outline">features list</UButton>
    .
    <br class="mb-4">
    <h1 class="text-xl font-bold my-2">Contribution</h1>
    If you want to contribute, feel free to check out the <UButton to="https://github.com/MPK1/quic-explorer" target="_blank" size="xs" color="gray" variant="outline">GitHub repository</UButton> .
  </div>
</template>

<style lang="postcss">
</style>
