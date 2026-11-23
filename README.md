# Festas de Portugal — base de dados aberta

Base de dados de festas populares, romarias, arraiais, feiras e festivais em Portugal, com localização, para usar em aplicações e mapas.

## Ficheiros

| ficheiro | para quê |
|---|---|
| [`festas.json`](festas.json) | lista simples de objectos, a mais fácil de ler numa app |
| [`festas.geojson`](festas.geojson) | o mesmo em GeoJSON; o GitHub mostra-o num mapa |
| [`festas.csv`](festas.csv) | para abrir no Excel / Google Sheets (listas separadas por ` \| `) |

Link directo para apps (sempre a versão mais recente):

```
https://raw.githubusercontent.com/YosephAlves/festas-portugal/main/festas.json
https://raw.githubusercontent.com/YosephAlves/festas-portugal/main/festas.geojson
```

## Campos

Valor desconhecido = `null` (no CSV, célula vazia). Nunca há strings vazias nem listas vazias.

| campo | tipo | exemplo |
|---|---|---|
| `id` | texto | `Q10281819` (Wikidata) ou `manual-0001` |
| `nome` | texto | Festa dos Tabuleiros |
| `descricao` | texto \| null | |
| `grupo` | `tradicional` \| `festival` | |
| `tipo` | lista \| null | `["evento", "património cultural imaterial"]` |
| `localidade` | texto \| null | Tomar |
| `concelho` | texto \| null | Tomar |
| `distrito` | texto \| null | Santarém (ilhas: Madeira / Açores) |
| `lat`, `lon` | número \| null | 39.6, -8.41667 (WGS84) |
| `coord_precisao` | `evento` \| `localidade` \| null | `localidade` = centro da vila/freguesia, não o recinto |
| `data_inicio`, `data_fim` | `AAAA-MM-DD` \| null | |
| `recorrencia` | texto \| null | «anual, 3.º fim-de-semana de Agosto» |
| `organizador` | texto \| null | |
| `site` | URL \| null | |
| `entrada_livre` | true \| false \| null | |
| `imagens` | lista de 1–6 URL \| null | links do Wikimedia Commons |
| `commons_categoria` | URL \| null | mais fotos livres da festa |
| `fonte` | URL | de onde veio a informação |
| `licenca_dados` | texto | |
| `licenca_imagens` | texto \| null | |

## Regras para acrescentar festas

1. Um registo por festa (não por edição/ano).
2. Coordenadas: no Google Maps, botão direito no adro/largo da festa → copiar coordenadas; `coord_precisao: "evento"`.
3. Imagens: só com licença livre (Wikimedia Commons) ou com autorização escrita do autor/organizador — indicar em `licenca_imagens`. Fotos de Facebook, câmaras ou jornais **não** servem.
4. Não copiar dados de outras plataformas fechadas (festasportugal.pt, aondevamos.pt, viralagenda…); usar fontes públicas e os próprios organizadores, e indicar sempre a `fonte`.
5. Registos manuais: `id` = `manual-0001`, `manual-0002`, …

## Origem e licenças

- Primeira carga (Novembro de 2026): [Wikidata](https://www.wikidata.org), dados CC0 1.0. Concelho e distrito por geocodificação inversa no [Nominatim / OpenStreetMap](https://nominatim.openstreetmap.org) (© contribuidores do OpenStreetMap, ODbL).
- Imagens: [Wikimedia Commons](https://commons.wikimedia.org); autor e licença na página de cada ficheiro. As tiradas da categoria Commons podem incluir fotos do local e não só da festa — rever.
- Fontes complementares com dados abertos: [lagenda.pt](https://lagenda.pt/dados-abertos.html) (CC BY 4.0, citar «Lagenda (lagenda.pt)»).
