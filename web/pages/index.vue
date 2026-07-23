<script setup lang="ts">
useHead({
  title: "Home",
});
useSeoMeta({
  description:
    "Compare open-source QUIC implementations by language, maintainer, license, and feature support — built for QUIC implementers and researchers.",
});

const { data: commitHash } = useCommitHash();

useSchemaOrg([
  defineDataset({
    name: "QUIC Explorer Dataset",
    description:
      "A curated, citable dataset of QUIC protocol implementations, their trackable features, and sourced entries linking the two.",
    keywords: [
      "QUIC",
      "HTTP/3",
      "protocol implementations",
      "feature support",
    ],
    license: "https://spdx.org/licenses/MIT.html",
    creator: definePerson({ name: "Marcel Kempf" }),
    citation: getCitation(),
    distribution: [
      {
        contentUrl: `https://raw.githubusercontent.com/MPK1/quic-explorer/${commitHash.value}/data/implementations.json`,
        encodingFormat: "application/json",
      },
      {
        contentUrl: `https://raw.githubusercontent.com/MPK1/quic-explorer/${commitHash.value}/data/features.json`,
        encodingFormat: "application/json",
      },
      {
        contentUrl: `https://raw.githubusercontent.com/MPK1/quic-explorer/${commitHash.value}/data/entries.json`,
        encodingFormat: "application/json",
      },
    ],
  }),
]);
</script>

<template>
  <div class="view">
    <div class="w-full block">
      <img class="w-1/6 m-auto mb-6" src="/favicon.png" />
    </div>

    <h1 class="text-4xl font-bold text-center mb-6">
      Welcome to QUIC Explorer!
    </h1>
    <p class="mb-4">
      QUIC Explorer helps you finding the right QUIC library for your project or
      research.
    </p>
    <p class="mb-4">
      This website is still in beta stage and not all features are available
      right now. <br />We are working on it and will add more features soon™️.
    </p>

    <h1 class="text-xl font-bold my-2">How To Use</h1>
    <p class="mb-4">
      If you want to browse a list of available open-source QUIC
      implementations, check out the
      <UButton
        class="cursor-pointer"
        to="/implementations"
        size="xs"
        color="neutral"
        variant="outline"
        >implementations table</UButton
      >
      .
    </p>
    <p class="mb-4">
      If you are searching for a QUIC implementation with support for a specific
      extension or feature, check out the
      <UButton
        class="cursor-pointer"
        to="/features"
        size="xs"
        color="neutral"
        variant="outline"
        >features list</UButton
      >
      .
    </p>

    <h1 class="text-xl font-bold my-2">Contribution</h1>
    <p class="mb-4">
      If you want to contribute, feel free to check out the
      <UButton
        to="https://github.com/MPK1/quic-explorer"
        target="_blank"
        size="xs"
        color="neutral"
        variant="outline"
        >GitHub repository</UButton
      >
      .
    </p>
  </div>
</template>

<style lang="postcss"></style>
