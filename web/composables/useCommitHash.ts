export default function () {
  return useAsyncData("commitHash", async () => useRuntimeConfig().gitCommitHash);
}
