export default function () {
  const today = new Date().toISOString().split('T')[0]
  const citation = `@misc{quic-explorer,
    title = {{QUIC Explorer}},
    author = {Marcel Kempf}},
    url = {https://quic-explorer.net},
    howpublished = {\\url{https://quic-explorer.net}},
    note = {Accessed: ` + today + `}
  }`
  return citation
}
