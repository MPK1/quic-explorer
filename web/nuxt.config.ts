// https://nuxt.com/docs/api/configuration/nuxt-config

import * as childProcess from "child_process";
import type { Implementation, Feature } from "./types";
import implementationsJson from "../data/implementations.json";
import featuresJson from "../data/features.json";

const getGitCommitHash = () => {
  var commitHash = "";
  try {
    commitHash = childProcess
      .execSync("git rev-parse --short HEAD")
      .toString()
      .trim();
  } catch (e) {
    console.error(e);
  }
  return commitHash;
};
const gitCommitHash = getGitCommitHash();

const getAllRoutes = async () => {
  const implementations: Implementation[] = implementationsJson.items;
  const impl_routes = implementations.map((i) => `/implementations/${i.uuid}`);
  const features: Feature[] = featuresJson.items;
  const feature_routes = features.map((f) => `/features/${f.uuid}`);
  return impl_routes.concat(feature_routes);
};

export default defineNuxtConfig({
  devtools: { enabled: true },
  ssr: true,
  ui: { icons: ["mdi"] },
  colorMode: { preference: "light" },
  runtimeConfig: {
    gitCommitHash: gitCommitHash,
  },
  hooks: {
    async "nitro:config"(nitroConfig) {
      const slugs = await getAllRoutes();
      if (
        nitroConfig &&
        nitroConfig.prerender &&
        nitroConfig.prerender.routes
      ) {
        nitroConfig.prerender.routes.push(...slugs);
      }
    },
  },
  modules: ["@nuxt/ui"],
});
