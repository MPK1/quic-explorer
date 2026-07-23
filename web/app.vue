<script setup>
useSeoMeta({
  ogImage: "/favicon.png",
});
useHead({
  link: [{ rel: "icon", type: "image/png", href: "/favicon.png" }],
});
</script>
<template>
  <UApp>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>
