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
# from pypi
pip install seqout-fetch

# OR clone the repo and install in editable mode
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
pytest
```

## Usage

```bash
❯ seqout-fetch --help
                                                                                                                                                                                            
 Usage: seqout-fetch [OPTIONS] COMMAND [ARGS]...                                                                                                                                            
                                                                                                                                                                                            
 Filter the seqout.org single-cell and spatial study tables and export them as CSV.                                                                                                         
                                                                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version          Show the version and exit.                                                                                                                                            │
│ --help             Show this message and exit.                                                                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ single-cell  Studies from https://seqout.org/technology/single-cell.                                                                                                                     │
│ spatial      Studies from https://seqout.org/technology/spatial.                                                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

```
seqout-fetch single-cell [FILTERS] [OPTIONS]
seqout-fetch spatial     [FILTERS] [OPTIONS]
```

Every filter is optional; combine as many as you need.

> Do not worry, you can always run `seqout-fetch <subcommand> --facets` to see the valid values for every filter.

e.g.

```bash
❯ seqout-fetch single-cell --facets

== modality (6) ==
  scRNA-seq                                               34627
  snRNA-seq                                               3896
  Spatial Transcriptomics                                 1828
  Multiome                                                1633
  scATAC-seq                                              577
  snATAC-seq                                              167

== cell_or_nucleus (2) ==
  single-cell                                             5476
  single-nucleus                                          4139

== perturbation_method (6) ==
  Perturb-seq                                             194
  CROP-seq                                                98
  ECCITE-seq                                              18
  Mosaic-seq                                              15
  sci-Plex                                                11
  CRISPR-detect                                           1

== intervention_kind (2) ==
  genetic                                                 315
  chemical                                                11

== chemistry (12) ==
  10x Chromium 3' v3                                      6829
  10x Chromium 3' v2 or 10x Chromium 5' v1 or v2          1864
  10x Chromium 3' v4 (GEM-X)                              962
  10x Chromium 3' v2                                      888
  10x Chromium 5' v1 or v2                                492
  10x Chromium 3' v1                                      324
  Single-cell, chemistry not in the 10x/Drop-seq registry 231
  10x Chromium 3' v2 or 10x Chromium 5' v1                95
  10x Chromium 5' v1                                      66
  10x Chromium 5' v3                                      65
  ATAC (chromatin accessibility)                          14
  10x Chromium 5' v2                                      4

== organism (1444) ==
  Mus musculus                                            27498
  Homo sapiens                                            21154
  Danio rerio                                             951
  Rattus norvegicus                                       606
  Drosophila melanogaster                                 483
  Sus scrofa                                              362
  Macaca mulatta                                          312
  Gallus gallus                                           265
  Arabidopsis thaliana                                    217
  Macaca fascicularis                                     186
  Bos taurus                                              181
  synthetic construct                                     102
  Mus                                                     101
  Caenorhabditis elegans                                  87
  Canis lupus familiaris                                  87
  Zea mays                                                78
  Ovis aries                                              74
  Schmidtea mediterranea                                  61
  Callithrix jacchus                                      56
  Oryctolagus cuniculus                                   53
  Pan troglodytes                                         52
  Saccharomyces cerevisiae                                46
  Capra hircus                                            41
  Oryza sativa                                            40
  Mustela putorius furo                                   38
  Ambystoma mexicanum                                     37
  Mesocricetus auratus                                    37
  Escherichia coli                                        36
  mixed sample                                            35
  Xenopus laevis                                          32
  Plasmodium falciparum                                   30
  Nematostella vectensis                                  30
  Pleurodeles waltl                                       28
  Solanum lycopersicum                                    27
  Heterocephalus glaber                                   27
  Bos grunniens                                           26
  Ciona robusta                                           24
  Oryza sativa Japonica Group                             22
  Equus caballus                                          22
  Felis catus                                             21
  ... 1404 more

== tissue (9062) ==
  brain                                                   4767
  blood                                                   4398
  lung                                                    3577
  liver                                                   2445
  bone marrow                                             2216
  spleen                                                  1795
  zone of skin                                            1528
  kidney                                                  1527
  heart                                                   1523
  pancreas                                                1159
  colon                                                   1020
  breast                                                  979
  Tumor                                                   976
  embryo                                                  781
  lymph node                                              776
  Pbmc                                                    686
  retina                                                  681
  Ammon's horn                                            589
  thymus                                                  542
  testis                                                  529
  ovary                                                   511
  intestine                                               489
  muscle organ                                            446
  small intestine                                         426
  spinal cord                                             398
  prostate gland                                          383
  peripheral blood mononuclear cell                       313
  aorta                                                   310
  adipose tissue                                          308
  Embryonic Stem Cell                                     305
  cortex                                                  291
  T cell                                                  258
  pleural effusion                                        257
  bone element                                            239
  skeletal muscle tissue                                  222
  stomach                                                 220
  placenta                                                214
  adrenal gland                                           199
  mammary gland                                           199
  cerebellum                                              187
  ... 9022 more

== assay_l1 (15) ==
  Single Cell                                             39279
  Transcriptomic                                          15496
  Spatial                                                 1771
  Chromatin Binding                                       1663
  Other                                                   1569
  Genomic Sequencing                                      685
  Chromatin Accessibility                                 642
  Targeted Sequencing                                     415
  DNA Methylation                                         197
  Microarray                                              173
  Chromatin Conformation                                  27
  Genotyping                                              24
  RNA Binding                                             8
  Proteomic                                               4
  Functional Genomics                                     4

== year (22) ==
  2026                                                    9128
  2025                                                    8904
  2024                                                    6694
  2023                                                    5635
  2022                                                    4320
  2021                                                    3392
  2020                                                    2537
  2019                                                    1463
  2018                                                    876
  2017                                                    382
  2016                                                    363
  2013                                                    154
  2015                                                    126
  2014                                                    66
  2012                                                    19
  2011                                                    12
  2010                                                    12
  2009                                                    11
  2008                                                    6
  2007                                                    5
  2006                                                    1
  2005                                                    1

== has_matrix (2) ==
  true                                                    33983
  false                                                   28307

== has_fastq (2) ==
  true                                                    47872
  false                                                   4038

== is_long_read (2) ==
  false                                                   61857
  true                                                    433
```

### Single-cell filters

```bash
❯ seqout-fetch single-cell --help
                                                                                                                                                                                            
 Usage: seqout-fetch single-cell [OPTIONS]                                                                                                                                                  
                                                                                                                                                                                            
 Studies from https://seqout.org/technology/single-cell.                                                                                                                                    
                                                                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --modality                     <str>    Declared assay type, e.g. scRNA-seq.                                                                                                             │
│ --cell-or-nucleus              <str>    single-cell or single-nucleus.                                                                                                                   │
│ --perturbation-method          <str>    Perturb-seq, CROP-seq, ...                                                                                                                       │
│ --intervention-kind            <str>    genetic or chemical.                                                                                                                             │
│ --chemistry                    <str>    e.g. "10x Chromium 3' v3".                                                                                                                       │
│ --organism                     <str>    Organism name, e.g. "Homo sapiens".                                                                                                              │
│ --tissue                       <str>    Tissue term, e.g. kidney.                                                                                                                        │
│ --assay-l1                     <str>    Assay level-1 category.                                                                                                                          │
│ --year                         <str>    Publication year.                                                                                                                                │
│ --has-matrix                   <str>    true or false.                                                                                                                                   │
│ --has-fastq                    <str>    true or false.                                                                                                                                   │
│ --has-sra                      <str>    true or false.                                                                                                                                   │
│ --is-long-read                 <str>    true or false.                                                                                                                                   │
│ --query                -q      <str>    Free-text keyword search.                                                                                                                        │
│ --sort                         <str>    Sort field. [default: year]                                                                                                                      │
│ --order                        <str>    asc or desc. [default: desc]                                                                                                                     │
│ --limit                        <int>    Records per page. [default: 100]                                                                                                                 │
│ --max-records                  <int>    Stop after N records (0 = all). [default: 0]                                                                                                     │
│ --sleep                        <float>  Seconds between pages. [default: 0.5]                                                                                                            │
│ --raw                                   Export every API field instead of the website columns.                                                                                           │
│ --out                  -o      <path>   Output CSV path (default: seqout_single_cell.csv).                                                                                               │
│ --facets                                Print valid filter values and exit.                                                                                                              │
│ --help                                  Show this message and exit.                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```


`--modality`, `--cell-or-nucleus`, `--perturbation-method`, `--intervention-kind`,
`--chemistry`, `--organism`, `--tissue`, `--assay-l1`, `--year`,
`--has-matrix`, `--has-fastq`, `--has-sra`, `--is-long-read`, `-q/--query`

### Spatial filters

```bash
❯ seqout-fetch spatial --help
                                                                                                                                                                                            
 Usage: seqout-fetch spatial [OPTIONS]                                                                                                                                                      
                                                                                                                                                                                            
 Studies from https://seqout.org/technology/spatial.                                                                                                                                        
                                                                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --platform                   <str>    Visium, Xenium, MERFISH, CosMx, ...                                                                                                                │
│ --resolution                 <str>    single-cell, spot or roi.                                                                                                                          │
│ --technology                 <str>    imaging, sequencing or hybrid.                                                                                                                     │
│ --data-availability          <str>    both, matrix_only, fastq_only or neither.                                                                                                          │
│ --organism                   <str>    Organism name, e.g. "Homo sapiens".                                                                                                                │
│ --tissue                     <str>    Tissue term, e.g. kidney.                                                                                                                          │
│ --readout-assay              <str>    e.g. Spatial Transcriptomics.                                                                                                                      │
│ --cell-line                  <str>    Cell line name.                                                                                                                                    │
│ --sample-type                <str>    e.g. primary tissue, organoid.                                                                                                                     │
│ --year                       <str>    Publication year.                                                                                                                                  │
│ --has-matrix                 <str>    true or false.                                                                                                                                     │
│ --has-fastq                  <str>    true or false.                                                                                                                                     │
│ --is-long-read               <str>    true or false.                                                                                                                                     │
│ --query              -q      <str>    Free-text keyword search.                                                                                                                          │
│ --sort                       <str>    Sort field. [default: year]                                                                                                                        │
│ --order                      <str>    asc or desc. [default: desc]                                                                                                                       │
│ --limit                      <int>    Records per page. [default: 100]                                                                                                                   │
│ --max-records                <int>    Stop after N records (0 = all). [default: 0]                                                                                                       │
│ --sleep                      <float>  Seconds between pages. [default: 0.5]                                                                                                              │
│ --raw                                 Export every API field instead of the website columns.                                                                                             │
│ --out                -o      <path>   Output CSV path (default: seqout_spatial.csv).                                                                                                     │
│ --facets                              Print valid filter values and exit.                                                                                                                │
│ --help                                Show this message and exit.                                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


```

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

e.g.
```bash
# 1️⃣ we just want kidney single cell RNA sequencing data, whatever
❯ seqout-fetch single-cell --modality scRNA-seq --tissue kidney --out kidney_scRNA-seq_collected.csv
querying single-cell (modality=scRNA-seq, tissue=kidney)
  fetched 100/749
  fetched 200/749
  fetched 300/749
  fetched 400/749
  fetched 500/749
  fetched 600/749
  fetched 700/749
  fetched 749/749
  matched 749 studies
wrote kidney_scRNA-seq_collected.csv (749 rows, 14 columns)


# 2️⃣ or single nucleus + kidney, whatever
❯ seqout-fetch single-cell --modality snRNA-seq --tissue kidney --out kidney_snRNA-seq_collected.csv
querying single-cell (modality=snRNA-seq, tissue=kidney)
  fetched 100/145
  fetched 145/145
  matched 145 studies
wrote kidney_snRNA-seq_collected.csv (145 rows, 14 columns)


# 3️⃣ or spatial kidney
# we can do it in single-cell mode, but the spatial table has more relevant columns
❯ seqout-fetch spatial --tissue kidney --out kidney_spatial_collected_1.csv
querying spatial (tissue=kidney)
  fetched 77/77
  matched 77 studies
wrote kidney_spatial_collected_1.csv (77 rows, 13 columns)

# we can also try it in single-cell mode
❯ seqout-fetch single-cell --modality "Spatial Transcriptomics"   --tissue kidney --out kidney_spatial_collected_2.csv
querying single-cell (modality=Spatial Transcriptomics, tissue=kidney)
  fetched 77/77
  matched 77 studies
wrote kidney_spatial_collected_2.csv (77 rows, 14 columns)

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

## Notes

> It's a good idea to couple `seqout-fetch` with [geofetch](https://github.com/pepkit/geofetch) to fetch the actual data files.

## Licence

MIT
