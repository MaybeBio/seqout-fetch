"""Formatting helpers that mirror the seqout.org table renderers.

The reference implementations live in the seqout-web frontend repository:

- ``components/single-cell-collection-card.tsx``
- ``components/spatial-collection-card.tsx``
- ``components/collection-card/shared.tsx`` (``TagList``, ``Availability``)
- ``utils/format.ts`` (``humanize``)

Keeping the same rules here means the CSV matches what the website shows.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

DASH = "—"
TAG_PREVIEW = 2


def humanize(value: Any) -> str:
    """Format a count like the website: 725, 3.2K, 1.2M, 1.5B."""
    if value is None:
        return DASH
    try:
        number = int(value)
    except (TypeError, ValueError):
        return str(value)

    for unit, divisor in (("B", 1_000_000_000), ("M", 1_000_000), ("K", 1_000)):
        if number >= divisor:
            text = f"{number / divisor:.1f}"
            return text[:-2] + unit if text.endswith(".0") else text + unit
    return str(number)


def as_list(value: Any) -> list[str]:
    """Normalize an API value that may be None, a string, or a list."""
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value]
    return [str(value)]


def tag_list(
    value: Any,
    labels: Mapping[str, str] | None = None,
    preview: int = TAG_PREVIEW,
    separator: str = "; ",
) -> str:
    """Render the website's TagList: first N values, then ``+rest``."""
    values = as_list(value)
    if labels:
        values = [labels.get(item, item) for item in values]
    if not values:
        return DASH

    shown = separator.join(values[:preview])
    remaining = len(values) - preview
    return f"{shown} +{remaining}" if remaining > 0 else shown


def availability(have: Any, runs: Any) -> str:
    """Render the website's Availability cell."""
    if have is None:
        return DASH
    if have:
        return f"yes ({humanize(runs)})" if runs else "yes"
    return "no"


def badge_or_dash(value: Any) -> str:
    """Render a single-value badge, or a dash when the value is missing."""
    return DASH if value in (None, "") else str(value)


def matrix_cell(record: Mapping[str, Any]) -> str:
    """Render the single-cell ``Matrix`` column."""
    if record.get("n_cells_source") == "reads" and record.get("n_cells"):
        return f"no (≈{humanize(record['n_cells'])} cells from reads)"
    if record.get("has_matrix"):
        cells = record.get("n_cells")
        return f"yes ({humanize(cells)} cells)" if cells else "yes"
    return "no"


def organism_cell(record: Mapping[str, Any]) -> str:
    """Render the dominant organism, with ``+N`` for additional organisms."""
    base = record.get("organism") or DASH
    organisms = as_list(record.get("organisms"))
    return f"{base} +{len(organisms) - 1}" if len(organisms) > 1 else base


def year_cell(record: Mapping[str, Any]) -> str:
    """Render the publication year, or a dash."""
    year = record.get("year")
    return str(year) if year is not None else DASH


def join_columns(values: Sequence[str], separator: str = ", ") -> str:
    """Join a sequence for compact display inside a CSV cell."""
    return separator.join(str(item) for item in values if item not in (None, ""))
