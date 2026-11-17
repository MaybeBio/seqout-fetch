"""Column definitions and row renderers for the two seqout.org tables.

The column order and formatting follow the website:

- https://seqout.org/technology/single-cell
- https://seqout.org/technology/spatial
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .render import (
    DASH,
    availability,
    badge_or_dash,
    humanize,
    matrix_cell,
    organism_cell,
    tag_list,
    year_cell,
)

CELL_LABELS = {"single-nucleus": "nucleus", "single-cell": "cell"}

DATA_AVAILABILITY = {
    "both": "matrix + FASTQ",
    "matrix_only": "matrix only",
    "fastq_only": "FASTQ only",
    "neither": "neither",
}

SINGLE_CELL_COLUMNS = (
    "Study",
    "Title",
    "Modality",
    "Cell / nucleus",
    "Perturbation",
    "Chemistry",
    "Organism",
    "Tissue",
    "Samples",
    "Matrix",
    "FASTQ",
    ".sra",
    "Long-read",
    "Year",
)

SPATIAL_COLUMNS = (
    "Study",
    "Title",
    "Platform",
    "Resolution",
    "Technology",
    "Readout",
    "Organism",
    "Samples",
    "Data",
    "Cells",
    "FASTQ",
    "Long-read",
    "Year",
)

SINGLE_CELL_RAW_COLUMNS = (
    "study_accession",
    "title",
    "organism",
    "organisms",
    "tissues",
    "single_cell_modality",
    "chemistries",
    "cell_or_nucleus",
    "assay_l1",
    "n_samples",
    "has_matrix",
    "n_cells",
    "n_cells_source",
    "has_fastq",
    "n_fastq_runs",
    "has_sra",
    "n_runs",
    "is_long_read",
    "perturbation_method",
    "intervention_kind",
    "is_pooled",
    "country",
    "pmid",
    "year",
)

SPATIAL_RAW_COLUMNS = (
    "study_accession",
    "title",
    "organism",
    "organisms",
    "tissues",
    "single_cell_modality",
    "is_long_read",
    "assay_l1",
    "readout_assays",
    "cell_lines",
    "sample_types",
    "n_samples",
    "n_cells",
    "has_matrix",
    "has_fastq",
    "has_sra",
    "n_fastq_runs",
    "n_runs",
    "data_availability",
    "platforms",
    "resolution",
    "technology",
    "country",
    "pmid",
    "year",
)

SINGLE_CELL_FACET_KEYS = (
    "modality",
    "cell_or_nucleus",
    "perturbation_method",
    "intervention_kind",
    "chemistry",
    "organism",
    "tissue",
    "assay_l1",
    "year",
    "has_matrix",
    "has_fastq",
    "is_long_read",
)

SPATIAL_FACET_KEYS = (
    "platform",
    "resolution",
    "technology",
    "data_availability",
    "organism",
    "tissue",
    "readout_assay",
    "cell_line",
    "sample_type",
    "year",
    "has_matrix",
    "has_fastq",
    "is_long_read",
)


def _study(record: Mapping[str, Any]) -> str:
    return record.get("study_accession") or DASH


def _title(record: Mapping[str, Any]) -> str:
    return record.get("title") or DASH


def single_cell_row(record: Mapping[str, Any]) -> dict[str, str]:
    """Render one ``/single-cell/projects`` record like the website table."""
    return {
        "Study": _study(record),
        "Title": _title(record),
        "Modality": record.get("single_cell_modality") or DASH,
        "Cell / nucleus": tag_list(record.get("cell_or_nucleus"), CELL_LABELS),
        "Perturbation": tag_list(record.get("perturbation_method")),
        "Chemistry": tag_list(record.get("chemistries")),
        "Organism": organism_cell(record),
        "Tissue": tag_list(record.get("tissues")),
        "Samples": humanize(record.get("n_samples")),
        "Matrix": matrix_cell(record),
        "FASTQ": availability(record.get("has_fastq"), record.get("n_fastq_runs")),
        ".sra": availability(record.get("has_sra"), record.get("n_runs")),
        "Long-read": "long-read" if record.get("is_long_read") else DASH,
        "Year": year_cell(record),
    }


def spatial_row(record: Mapping[str, Any]) -> dict[str, str]:
    """Render one ``/spatial/projects`` record like the website table."""
    return {
        "Study": _study(record),
        "Title": _title(record),
        "Platform": tag_list(record.get("platforms")),
        "Resolution": badge_or_dash(record.get("resolution")),
        "Technology": badge_or_dash(record.get("technology")),
        "Readout": tag_list(record.get("readout_assays")),
        "Organism": organism_cell(record),
        "Samples": humanize(record.get("n_samples")),
        "Data": DATA_AVAILABILITY.get(record.get("data_availability"), DASH),
        "Cells": humanize(record.get("n_cells")),
        "FASTQ": availability(record.get("has_fastq"), record.get("n_fastq_runs")),
        "Long-read": "long-read" if record.get("is_long_read") else DASH,
        "Year": year_cell(record),
    }


@dataclass(frozen=True)
class Dataset:
    """Everything the CLI needs to know about one seqout.org table."""

    name: str
    columns: tuple[str, ...]
    row: Callable[[Mapping[str, Any]], dict[str, str]]
    facet_keys: tuple[str, ...]
    raw_columns: tuple[str, ...]
    default_out: str


DATASETS = {
    "single-cell": Dataset(
        name="single-cell",
        columns=SINGLE_CELL_COLUMNS,
        row=single_cell_row,
        facet_keys=SINGLE_CELL_FACET_KEYS,
        raw_columns=SINGLE_CELL_RAW_COLUMNS,
        default_out="seqout_single_cell.csv",
    ),
    "spatial": Dataset(
        name="spatial",
        columns=SPATIAL_COLUMNS,
        row=spatial_row,
        facet_keys=SPATIAL_FACET_KEYS,
        raw_columns=SPATIAL_RAW_COLUMNS,
        default_out="seqout_spatial.csv",
    ),
}
