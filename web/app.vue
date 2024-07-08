<script setup>
useSeoMeta({
  ogImage: "/favicon.png",
});
useHead({
  link: [{ rel: "icon", type: "image/png", href: "/favicon.png" }],
});
</script>
<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
