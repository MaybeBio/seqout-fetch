"""Rendering tests using rows copied from the seqout.org tables."""

from __future__ import annotations

from seqout_fetch.render import (
    availability,
    badge_or_dash,
    humanize,
    matrix_cell,
    organism_cell,
    tag_list,
)
from seqout_fetch.schema import spatial_row, single_cell_row


def test_humanize() -> None:
    assert humanize(None) == "—"
    assert humanize(725) == "725"
    assert humanize(3200) == "3.2K"
    assert humanize(184900) == "184.9K"
    assert humanize(1173739) == "1.2M"
    assert humanize(1_000_000_000) == "1B"


def test_availability() -> None:
    assert availability(None, None) == "—"
    assert availability(True, None) == "yes"
    assert availability(True, 4) == "yes (4)"
    assert availability(False, None) == "no"


def test_tag_list_preview() -> None:
    assert tag_list(None) == "—"
    assert tag_list(["Visium"]) == "Visium"
    assert tag_list(["blood", "gill"]) == "blood; gill"
    assert tag_list(["a", "b", "c"]) == "a; b +1"
    assert tag_list("single-nucleus", {"single-nucleus": "nucleus"}) == "nucleus"


def test_badge_or_dash() -> None:
    assert badge_or_dash(None) == "—"
    assert badge_or_dash("spot") == "spot"


def test_matrix_cell() -> None:
    assert matrix_cell({"has_matrix": True, "n_cells": 184900}) == "yes (184.9K cells)"
    assert matrix_cell({"has_matrix": True}) == "yes"
    assert matrix_cell({"has_matrix": False}) == "no"
    assert (
        matrix_cell({"has_matrix": False, "n_cells": 500, "n_cells_source": "reads"})
        == "no (≈500 cells from reads)"
    )


def test_organism_cell() -> None:
    assert organism_cell({"organism": "Homo sapiens"}) == "Homo sapiens"
    assert (
        organism_cell(
            {
                "organism": "Lethenteron camtschaticum",
                "organisms": ["Lethenteron camtschaticum", "Eptatretus burgeri"],
            }
        )
        == "Lethenteron camtschaticum +1"
    )


# Row copied from the single-cell table screenshot (SRP674058).
SINGLE_CELL_RECORD = {
    "study_accession": "SRP674058",
    "title": "Single-cell Characterization of Leukocytes from PBMCs, Kidney, and Gill",
    "single_cell_modality": "scRNA-seq",
    "cell_or_nucleus": None,
    "perturbation_method": None,
    "chemistries": ["10x Chromium 3' v3", "10x Chromium 5' v1 or v2"],
    "organism": "Lethenteron camtschaticum",
    "organisms": ["Lethenteron camtschaticum", "Eptatretus burgeri"],
    "tissues": ["blood", "gill"],
    "n_samples": 7,
    "has_matrix": False,
    "n_cells": None,
    "n_cells_source": None,
    "has_fastq": True,
    "n_fastq_runs": 4,
    "has_sra": False,
    "n_runs": None,
    "is_long_read": False,
    "year": 2026,
}


def test_single_cell_row_matches_website() -> None:
    row = single_cell_row(SINGLE_CELL_RECORD)
    assert row["Study"] == "SRP674058"
    assert row["Modality"] == "scRNA-seq"
    assert row["Cell / nucleus"] == "—"
    assert row["Perturbation"] == "—"
    assert row["Chemistry"] == "10x Chromium 3' v3; 10x Chromium 5' v1 or v2"
    assert row["Organism"] == "Lethenteron camtschaticum +1"
    assert row["Tissue"] == "blood; gill"
    assert row["Samples"] == "7"
    assert row["Matrix"] == "no"
    assert row["FASTQ"] == "yes (4)"
    assert row[".sra"] == "no"
    assert row["Long-read"] == "—"
    assert row["Year"] == "2026"


# Rows copied from the spatial table screenshot.
XENIUM_RECORD = {
    "study_accession": "GSE289001",
    "title": "Spatial single cell transcriptomic analysis [Xenium]",
    "platforms": ["Xenium"],
    "resolution": "single-cell",
    "technology": "imaging",
    "readout_assays": ["Spatial Transcriptomics"],
    "organism": "Mus musculus",
    "organisms": None,
    "n_samples": 72,
    "data_availability": "matrix_only",
    "n_cells": 184900,
    "has_fastq": None,
    "n_fastq_runs": None,
    "is_long_read": False,
    "year": 2026,
}

GENERIC_SPATIAL_RECORD = {
    "study_accession": "GSE311717",
    "title": "Lipid-Associated Macrophage Polarization",
    "platforms": None,
    "resolution": None,
    "technology": None,
    "readout_assays": ["Single-cell Transcriptomics"],
    "organism": "Macaca fascicularis",
    "organisms": None,
    "n_samples": 44,
    "data_availability": "both",
    "n_cells": 175500,
    "has_fastq": True,
    "n_fastq_runs": 44,
    "is_long_read": False,
    "year": 2026,
}

VISIUM_RECORD = {
    "study_accession": "GSE307817",
    "title": "A MEF2C transcription factor network",
    "platforms": ["Visium"],
    "resolution": "spot",
    "technology": "sequencing",
    "readout_assays": ["Spatial Transcriptomics"],
    "organism": "Homo sapiens",
    "organisms": None,
    "n_samples": 12,
    "data_availability": "matrix_only",
    "n_cells": 20600,
    "has_fastq": None,
    "n_fastq_runs": None,
    "is_long_read": False,
    "year": 2026,
}


def test_spatial_row_matches_website() -> None:
    xenium = spatial_row(XENIUM_RECORD)
    assert xenium["Platform"] == "Xenium"
    assert xenium["Resolution"] == "single-cell"
    assert xenium["Technology"] == "imaging"
    assert xenium["Readout"] == "Spatial Transcriptomics"
    assert xenium["Samples"] == "72"
    assert xenium["Data"] == "matrix only"
    assert xenium["Cells"] == "184.9K"
    assert xenium["FASTQ"] == "—"

    generic = spatial_row(GENERIC_SPATIAL_RECORD)
    assert generic["Platform"] == "—"
    assert generic["Resolution"] == "—"
    assert generic["Technology"] == "—"
    assert generic["Data"] == "matrix + FASTQ"
    assert generic["Cells"] == "175.5K"
    assert generic["FASTQ"] == "yes (44)"

    visium = spatial_row(VISIUM_RECORD)
    assert visium["Platform"] == "Visium"
    assert visium["Resolution"] == "spot"
    assert visium["Technology"] == "sequencing"
    assert visium["Cells"] == "20.6K"


def test_empty_record_is_all_dashes() -> None:
    row = single_cell_row({})
    assert row["Study"] == "—"
    assert row["Samples"] == "—"
    assert row["Matrix"] == "no"
    assert row["Year"] == "—"
