"""Command line interface for seqout-fetch."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Mapping, Optional

import typer

from . import __version__
from .client import SeqoutError, fetch_facets, fetch_projects
from .schema import DATASETS

FACET_PREVIEW = 40

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Filter the seqout.org single-cell and spatial study tables and export them as CSV.",
)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"seqout-fetch {__version__}")
        raise typer.Exit()


def _bool_value(option: str, value: Optional[str]) -> Optional[str]:
    """Validate a tri-state true/false filter."""
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized not in ("true", "false"):
        raise typer.BadParameter("must be 'true' or 'false'", param_hint=option)
    return normalized


def _validate(order: str, limit: int) -> None:
    if order not in ("asc", "desc"):
        raise typer.BadParameter("must be 'asc' or 'desc'", param_hint="--order")
    if limit <= 0:
        raise typer.BadParameter("must be greater than 0", param_hint="--limit")


def _progress(done: int, total: int) -> None:
    typer.echo(f"  fetched {done}/{total}", err=True)


def _flatten(value: Any) -> str:
    """Turn an API value into a single CSV cell."""
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    if value is None:
        return ""
    return str(value).replace("\n", " ")


def _write_csv(path: Path, columns: tuple[str, ...], records: list[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for record in records:
            writer.writerow({key: _flatten(record.get(key, "")) for key in columns})


def _print_facets(dataset: str, facet_keys: tuple[str, ...]) -> None:
    try:
        payload = fetch_facets(dataset)
    except SeqoutError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    for key in facet_keys:
        values = payload.get(key) or []
        if not values:
            continue
        typer.echo(f"\n== {key} ({len(values)}) ==")
        for item in values[:FACET_PREVIEW]:
            if isinstance(item, dict):
                typer.echo(f"  {str(item.get('value')):55s} {item.get('studies')}")
            else:
                typer.echo(f"  {item}")
        if len(values) > FACET_PREVIEW:
            typer.echo(f"  ... {len(values) - FACET_PREVIEW} more")


def _run(
    dataset: str,
    filters: Mapping[str, Any],
    *,
    raw: bool,
    out: Optional[Path],
    limit: int,
    max_records: int,
    sleep: float,
    sort: str,
    order: str,
    facets: bool,
) -> None:
    spec = DATASETS[dataset]

    if facets:
        _print_facets(dataset, spec.facet_keys)
        return

    active = {key: value for key, value in filters.items() if value not in (None, "")}
    described = ", ".join(f"{key}={value}" for key, value in active.items()) or "no filters"
    typer.echo(f"querying {dataset} ({described})", err=True)

    try:
        rows = fetch_projects(
            dataset,
            active,
            page_size=limit,
            max_records=max_records,
            sleep=sleep,
            sort=sort,
            order=order,
            progress=_progress,
        )
    except SeqoutError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    typer.echo(f"  matched {len(rows)} studies", err=True)

    if raw:
        columns = spec.raw_columns
        records = rows
    else:
        columns = spec.columns
        records = [spec.row(record) for record in rows]

    target = Path(out) if out else Path(spec.default_out)
    _write_csv(target, columns, records)
    typer.echo(f"wrote {target} ({len(records)} rows, {len(columns)} columns)")


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
@app.callback()
def _root(
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
) -> None:
    """seqout-fetch: filter seqout.org study tables and export CSV."""


@app.command("single-cell")
def single_cell(
    modality: Optional[str] = typer.Option(None, "--modality", help="Declared assay type, e.g. scRNA-seq."),
    cell_or_nucleus: Optional[str] = typer.Option(None, "--cell-or-nucleus", help="single-cell or single-nucleus."),
    perturbation_method: Optional[str] = typer.Option(None, "--perturbation-method", help="Perturb-seq, CROP-seq, ..."),
    intervention_kind: Optional[str] = typer.Option(None, "--intervention-kind", help="genetic or chemical."),
    chemistry: Optional[str] = typer.Option(None, "--chemistry", help="e.g. \"10x Chromium 3' v3\"."),
    organism: Optional[str] = typer.Option(None, "--organism", help="Organism name, e.g. \"Homo sapiens\"."),
    tissue: Optional[str] = typer.Option(None, "--tissue", help="Tissue term, e.g. kidney."),
    assay_l1: Optional[str] = typer.Option(None, "--assay-l1", help="Assay level-1 category."),
    year: Optional[str] = typer.Option(None, "--year", help="Publication year."),
    has_matrix: Optional[str] = typer.Option(None, "--has-matrix", help="true or false."),
    has_fastq: Optional[str] = typer.Option(None, "--has-fastq", help="true or false."),
    has_sra: Optional[str] = typer.Option(None, "--has-sra", help="true or false."),
    is_long_read: Optional[str] = typer.Option(None, "--is-long-read", help="true or false."),
    query: Optional[str] = typer.Option(None, "-q", "--query", help="Free-text keyword search."),
    sort: str = typer.Option("year", "--sort", help="Sort field."),
    order: str = typer.Option("desc", "--order", help="asc or desc."),
    limit: int = typer.Option(100, "--limit", help="Records per page."),
    max_records: int = typer.Option(0, "--max-records", help="Stop after N records (0 = all)."),
    sleep: float = typer.Option(0.5, "--sleep", help="Seconds between pages."),
    raw: bool = typer.Option(False, "--raw", help="Export every API field instead of the website columns."),
    out: Optional[Path] = typer.Option(None, "-o", "--out", help="Output CSV path (default: seqout_single_cell.csv)."),
    facets: bool = typer.Option(False, "--facets", help="Print valid filter values and exit."),
) -> None:
    """Studies from https://seqout.org/technology/single-cell."""
    _validate(order, limit)
    _run(
        "single-cell",
        {
            "modality": modality,
            "cell_or_nucleus": cell_or_nucleus,
            "perturbation_method": perturbation_method,
            "intervention_kind": intervention_kind,
            "chemistry": chemistry,
            "organism": organism,
            "tissue": tissue,
            "assay_l1": assay_l1,
            "year": year,
            "has_matrix": _bool_value("--has-matrix", has_matrix),
            "has_fastq": _bool_value("--has-fastq", has_fastq),
            "has_sra": _bool_value("--has-sra", has_sra),
            "is_long_read": _bool_value("--is-long-read", is_long_read),
            "q": query,
        },
        raw=raw,
        out=out,
        limit=limit,
        max_records=max_records,
        sleep=sleep,
        sort=sort,
        order=order,
        facets=facets,
    )


@app.command("spatial")
def spatial(
    platform: Optional[str] = typer.Option(None, "--platform", help="Visium, Xenium, MERFISH, CosMx, ..."),
    resolution: Optional[str] = typer.Option(None, "--resolution", help="single-cell, spot or roi."),
    technology: Optional[str] = typer.Option(None, "--technology", help="imaging, sequencing or hybrid."),
    data_availability: Optional[str] = typer.Option(None, "--data-availability", help="both, matrix_only, fastq_only or neither."),
    organism: Optional[str] = typer.Option(None, "--organism", help="Organism name, e.g. \"Homo sapiens\"."),
    tissue: Optional[str] = typer.Option(None, "--tissue", help="Tissue term, e.g. kidney."),
    readout_assay: Optional[str] = typer.Option(None, "--readout-assay", help="e.g. Spatial Transcriptomics."),
    cell_line: Optional[str] = typer.Option(None, "--cell-line", help="Cell line name."),
    sample_type: Optional[str] = typer.Option(None, "--sample-type", help="e.g. primary tissue, organoid."),
    year: Optional[str] = typer.Option(None, "--year", help="Publication year."),
    has_matrix: Optional[str] = typer.Option(None, "--has-matrix", help="true or false."),
    has_fastq: Optional[str] = typer.Option(None, "--has-fastq", help="true or false."),
    is_long_read: Optional[str] = typer.Option(None, "--is-long-read", help="true or false."),
    query: Optional[str] = typer.Option(None, "-q", "--query", help="Free-text keyword search."),
    sort: str = typer.Option("year", "--sort", help="Sort field."),
    order: str = typer.Option("desc", "--order", help="asc or desc."),
    limit: int = typer.Option(100, "--limit", help="Records per page."),
    max_records: int = typer.Option(0, "--max-records", help="Stop after N records (0 = all)."),
    sleep: float = typer.Option(0.5, "--sleep", help="Seconds between pages."),
    raw: bool = typer.Option(False, "--raw", help="Export every API field instead of the website columns."),
    out: Optional[Path] = typer.Option(None, "-o", "--out", help="Output CSV path (default: seqout_spatial.csv)."),
    facets: bool = typer.Option(False, "--facets", help="Print valid filter values and exit."),
) -> None:
    """Studies from https://seqout.org/technology/spatial."""
    _validate(order, limit)
    _run(
        "spatial",
        {
            "platform": platform,
            "resolution": resolution,
            "technology": technology,
            "data_availability": data_availability,
            "organism": organism,
            "tissue": tissue,
            "readout_assay": readout_assay,
            "cell_line": cell_line,
            "sample_type": sample_type,
            "year": year,
            "has_matrix": _bool_value("--has-matrix", has_matrix),
            "has_fastq": _bool_value("--has-fastq", has_fastq),
            "is_long_read": _bool_value("--is-long-read", is_long_read),
            "q": query,
        },
        raw=raw,
        out=out,
        limit=limit,
        max_records=max_records,
        sleep=sleep,
        sort=sort,
        order=order,
        facets=facets,
    )


def main() -> None:
    """Console script entry point."""
    app()


if __name__ == "__main__":
    main()
