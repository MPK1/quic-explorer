<script setup lang="ts">
const route = useRoute();
const host = process.server ? useRequestHeaders().host : window.location.host;

const citation = getCitation();

useHead({
  link: [
    // We use route.path since we don't use query parameters
    { rel: "canonical", href: `https://${host}${route.path}` },
  ],
});
</script>

<template>
  <div>
    <header class="header">
      <nav class="inner" role="navigation">
        <NuxtLink to="/" class="shrink-0">
          <img class="logo" src="/favicon.png" alt="logo" />
          <span class="logo-text hidden sm:inline">QUIC Explorer</span>
        </NuxtLink>

        <div class="spacer"></div>

        <span class="hdr-link-right">
          <a href="/implementations">Implementations</a>
        </span>
        <span class="hdr-link-right hidden md:inline">
          <a href="/features">Features</a>
        </span>
        <span class="hdr-link-right hidden md:inline">
          <UPopover>
            <a rel="noopener banner">Cite</a>
            <template #panel>
              <div class="h-48 w-[28rem] p-4 text-black">
                <UTextarea class="w-full h-full" :rows="7" v-model="citation" />
              </div>
            </template>
          </UPopover>
        </span>
        <span class="hdr-link-right">
          <a
            href="https://github.com/MPK1/quic-explorer"
            target="_blank"
            rel="noopener banner"
          >
            Open on GitHub
          </a>
        </span>
      </nav>
    </header>
    <slot role="main" />
    <footer class="footer">
      <div class="version">
        <VersionInformation />
      </div>
    </footer>
  </div>
</template>

<style lang="postcss">
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
  font-size: 15px;
  background-color: #f4f4f5;
  margin: 0;
  padding: 0;
  color: #18181b;
  overflow-y: scroll;
  padding-bottom: 50px;
}

a {
  color: #18181b;
  text-decoration: none;
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

.appear-active {
  transition: opacity 0.4s ease;
}

.appear {
  opacity: 0;
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
