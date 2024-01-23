// https://nuxt.com/docs/api/configuration/nuxt-config

import type { Implementation } from "./types";
import data from '../data/implementations.json';

const getImplRoutes = async () => {
  const implementations: Implementation[] = data.items;
  return implementations.map((i) => `/implementations/${i.uuid}`);
};

export default defineNuxtConfig({
  devtools: { enabled: true },
  ssr: true,
  ui: { icons: ['mdi'] },
  colorMode: { preference: 'light' },
  hooks: {
    async 'nitro:config'(nitroConfig) {
      const slugs = await getImplRoutes();
      if (nitroConfig && nitroConfig.prerender && nitroConfig.prerender.routes){
        nitroConfig.prerender.routes.push(...slugs);
      }
    },
  },
  modules: ["@nuxt/ui"]
})
