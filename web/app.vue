<script setup>
useSeoMeta({
  ogImage: "/og-banner.png",
  ogImageWidth: 1200,
  ogImageHeight: 630,
  ogImageAlt:
    "QUIC Explorer — a curated, citable reference of QUIC protocol implementations and their feature support",
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
