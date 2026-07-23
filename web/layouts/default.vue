<script setup lang="ts">
// Canonical <link> tags are handled automatically by @nuxtjs/seo (based on
// `site.url` in nuxt.config.ts), so no manual useHead() call is needed here.

const citation = getCitation();
const isFullscreen = useState<boolean>("matrix-fullscreen", () => false);
const citeOpen = ref(false);

const navLinks = [
  { label: "Implementations", to: "/implementations" },
  { label: "Features", to: "/features" },
  { label: "Matrix", to: "/matrix" },
];

const mobileMenuItems = computed(() => [
  ...navLinks.map((l) => ({ label: l.label, to: l.to })),
  { label: "Cite", onSelect: () => (citeOpen.value = true) },
  {
    label: "Open on GitHub",
    to: "https://github.com/MPK1/quic-explorer",
    target: "_blank",
  },
]);
</script>

<template>
  <div>
    <header v-if="!isFullscreen" class="header">
      <nav class="inner" role="navigation">
        <NuxtLink to="/" class="shrink-0">
          <img class="logo" src="/favicon.png" alt="logo" />
          <span class="logo-text hidden sm:inline">QUIC Explorer</span>
        </NuxtLink>

        <div class="spacer"></div>

        <span
          v-for="link in navLinks"
          :key="link.to"
          class="hdr-link-right hidden md:inline"
        >
          <a :href="link.to">{{ link.label }}</a>
        </span>
        <span class="hdr-link-right hidden md:inline">
          <a
            role="button"
            tabindex="0"
            class="cursor-pointer"
            @click="citeOpen = true"
            @keydown.enter="citeOpen = true"
            >Cite</a
          >
        </span>
        <span class="hdr-link-right hidden md:inline">
          <a
            href="https://github.com/MPK1/quic-explorer"
            target="_blank"
            rel="noopener banner"
          >
            Open on GitHub
          </a>
        </span>

        <UDropdownMenu :items="mobileMenuItems" :content="{ align: 'end' }">
          <UButton
            class="md:hidden"
            color="neutral"
            variant="ghost"
            icon="i-lucide-menu"
            aria-label="Open menu"
          />
        </UDropdownMenu>
      </nav>
    </header>
    <slot role="main" />
    <footer v-if="!isFullscreen" class="footer">
      <div class="version">
        <VersionInformation />
      </div>
    </footer>
    <UModal v-model:open="citeOpen" title="Cite QUIC Explorer">
      <template #body>
        <UTextarea class="w-full" :rows="7" :model-value="citation" readonly />
      </template>
    </UModal>
  </div>
</template>

<style lang="postcss">
body {
  font-family:
    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu,
    Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
  font-size: 15px;
  background-color: #f4f4f5;
  margin: 0;
  padding: 0;
  color: #18181b;
  overflow-y: scroll;
  padding-bottom: 50px;
}

.header {
  background-color: #18181b;
  z-index: 999;
  height: 55px;

  .inner {
    max-width: 800px;
    box-sizing: border-box;
    margin: 0px auto;
    padding: 12px 5px;
    display: flex;
    place-items: center;
  }

  .logo-text {
    font-family: "Varela Round", sans-serif;
    font-size: 1.2em;
    white-space: nowrap;
    color: #fff;
    vertical-align: middle;
  }

  & a {
    color: #fff;
    line-height: 24px;
    transition: color 0.15s ease;
    display: inline-block;
    vertical-align: middle;
    font-weight: 300;
    letter-spacing: 0.075em;
    margin-right: 1.8em;

    &:hover {
      color: rgb(var(--color-primary-500));
    }

    &.active {
      color: rgb(var(--color-primary-500));
    }

    &:nth-child(6) {
      margin-right: 0;
    }
  }
  .spacer {
    flex-grow: 1;
  }
  .hdr-link-right {
    color: #fff;
    font-size: 0.9em;
    white-space: nowrap;
    margin: auto;
    margin-left: 1em;
    text-align: right;
    & a {
      margin-right: 0;
    }
  }
}

.logo {
  width: 30px;
  height: 30px;
  margin-right: 10px;
  display: inline-block;
  vertical-align: middle;
}

.view {
  max-width: 1000px;
  margin: 0 auto;
  position: relative;
  background-color: #fff;
  box-sizing: border-box;
  padding: 2em 3em;
}

.footer {
  position: fixed;
  width: 100%;
  font-size: 9pt;
  bottom: 0;
  background-color: #18181b;
  color: #f4f4f5;
  z-index: 999;
  padding: 0.3em 2em;

  & .version {
    float: right;
  }
}

@media (min-width: 1000px) {
  .header .hdr-link-right {
    margin-left: 2em;
  }
}

@media (min-width: 1600px) {
  .view {
    max-width: 1400px;
  }
  .header .inner {
    max-width: 1200px;
  }
  .header .hdr-link-right {
    margin-left: 4em;
  }
}

@media (max-width: 860px) {
  .header .inner {
    padding: 15px 30px;
  }
}

@media (max-width: 600px) {
  .header {
    .inner {
      padding: 15px;
    }

    & a {
      margin-right: 1em;
    }

    .github {
      display: none;
    }
  }
}
</style>
