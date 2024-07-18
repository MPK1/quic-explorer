export default function () {
  const today = new Date().toISOString().split("T")[0];
  const { data: commitHash } = useAsyncData("commitHash", async () => {
    return useRuntimeConfig().gitCommitHash;
  });
  return (
    `@misc{quic-explorer,
    title = {{QUIC Explorer}},
    author = {Marcel Kempf},
    url = {https://quic-explorer.net},
    howpublished = {\\url{https://quic-explorer.net}},
    note = {Accessed: ` +
    today +
    ` (Commit ` +
    commitHash.value +
    `)}
  }`
  );
}
