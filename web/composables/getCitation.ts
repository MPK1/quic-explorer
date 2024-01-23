export default function () {
  const today = new Date().toISOString().split('T')[0]
  const citation = `@misc{ quic-explorer,
    author = {Marcel Kempf}},
    title = {{QUIC Explorer}},
    url = {https://quic-explorer.net},
    howpublished = {\\url{https://quic-explorer.net}},
    note = {Accessed: ` + today + `}
  }`
  return citation
}
