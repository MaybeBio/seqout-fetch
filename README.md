<div align="center">

# seqout-fetch

<img src="figs/logo.svg" alt="seqout-fetch logo" width="112" />

**Filter the seqout.org study tables and export them as CSV.**

<p>
  <strong>Scope: single-cell and spatial transcriptomics only.</strong><br/>
  Two tables, two subcommands, no bulk RNA-seq and no general-purpose GEO browsing.
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![Data source](https://img.shields.io/badge/Data-seqout.org-2ea44f)](https://seqout.org)
[![Scope](https://img.shields.io/badge/Scope-single--cell%20%7C%20spatial-f59e0b)](#scope)
[![Interface](https://img.shields.io/badge/Interface-CLI-0366d6)](#usage)

<p>
  <a href="https://seqout.org/technology/single-cell">Single-cell table</a> ·
  <a href="https://seqout.org/technology/spatial">Spatial table</a> ·
  <a href="#install">Install</a> ·
  <a href="#usage">Usage</a> ·
  <a href="#output-columns">Columns</a>
</p>

</div>

---

## Scope

`seqout-fetch` wraps exactly two public seqout.org endpoints. Everything else is
out of scope by design.

| | Single-cell | Spatial |
| --- | --- | --- |
| Web page | [technology/single-cell](https://seqout.org/technology/single-cell) | [technology/spatial](https://seqout.org/technology/spatial) |
| API | `GET /api/single-cell/projects` | `GET /api/spatial/projects` |
| Command | `seqout-fetch single-cell` | `seqout-fetch spatial` |
| Corpus | ~62,000 studies | ~1,800 studies |
| Filters | modality, cell/nucleus, chemistry, organism, tissue, matrix, FASTQ, SRA, long-read | platform, resolution, technology, readout, data availability, organism, tissue, cell line, sample type |

Deliberately **not** included:

- Bulk RNA-seq, microarray, or whole-genome studies outside these two tables.
- General GEO/SRA/ENA search — use the [seqout frontend](https://seqout.org) or the official `seqout` package for that.
- Downloading FASTQ or count matrices themselves. This tool exports the *index*; use the accessions it produces to fetch the data.

## Install

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
pytest
```

## Usage

```
seqout-fetch single-cell [FILTERS] [OPTIONS]
seqout-fetch spatial     [FILTERS] [OPTIONS]
```

Every filter is optional; combine as many as you need.

### Single-cell filters

`--modality`, `--cell-or-nucleus`, `--perturbation-method`, `--intervention-kind`,
`--chemistry`, `--organism`, `--tissue`, `--assay-l1`, `--year`,
`--has-matrix`, `--has-fastq`, `--has-sra`, `--is-long-read`, `-q/--query`

### Spatial filters

`--platform`, `--resolution`, `--technology`, `--data-availability`,
`--organism`, `--tissue`, `--readout-assay`, `--cell-line`, `--sample-type`,
`--year`, `--has-matrix`, `--has-fastq`, `--is-long-read`, `-q/--query`

Boolean filters take the literal strings `true` or `false`.

### Common options

| Option | Default | Meaning |
| --- | --- | --- |
| `--sort` | `year` | Sort field |
| `--order` | `desc` | `asc` or `desc` |
| `--limit` | `100` | Records per page |
| `--max-records` | `0` | Stop after N records (0 = all) |
| `--sleep` | `0.5` | Seconds between pages |
| `--raw` | off | Export every API field instead of the website columns |
| `-o/--out` | `seqout_<dataset>.csv` | Output path |
| `--facets` | off | Print valid filter values and exit |
| `--version` | | Print the version and exit |

### Examples

```bash
# Human kidney single-cell studies that ship a count matrix
seqout-fetch single-cell --organism "Homo sapiens" --tissue kidney --has-matrix true

# Human kidney spatial studies on a named platform
seqout-fetch spatial --tissue kidney --platform Xenium

# Single-cell resolution spatial studies with raw FASTQ
seqout-fetch spatial --resolution single-cell --has-fastq true

# Discover the valid values for every filter
seqout-fetch spatial --facets

# Export all API fields instead of the website columns
seqout-fetch single-cell --tissue kidney --raw -o kidney_raw.csv
```

## Output columns

Single-cell (14 columns):

```
Study  Title  Modality  Cell / nucleus  Perturbation  Chemistry  Organism
Tissue  Samples  Matrix  FASTQ  .sra  Long-read  Year
```

Spatial (13 columns):

```
Study  Title  Platform  Resolution  Technology  Readout  Organism
Samples  Data  Cells  FASTQ  Long-read  Year
```

Formatting rules mirror the website:

- Missing values render as `—`.
- List values show the first two entries followed by `+N`; in CSV they are joined with `; `.
- `Matrix` renders `yes (1.2M cells)`, `yes`, `no`, or `no (≈N cells from reads)`.
- `FASTQ` / `.sra` render `yes (4)`, `yes`, `no`, or `—` when unknown.
- Counts use `K` / `M` / `B` suffixes.
- Spatial `Data` maps `data_availability` to `matrix + FASTQ`, `matrix only`, `FASTQ only`, or `neither`.

## Behaviour

- Progress and diagnostics go to stderr, so stdout stays clean.
- Failed requests are retried three times with exponential backoff; the CLI exits with status 1 and prints the failing URL.
- A query with zero matches still writes the CSV header.
- The tool is read-only: it never writes to seqout.org.

## Layout

```
src/seqout_fetch/
├── cli.py        Typer commands and CSV writing
├── client.py     HTTP, retries, pagination
├── render.py     Formatting helpers matching the web frontend
└── schema.py     Column definitions and row renderers
```

## Licence

MIT
