"""HTTP access to the public seqout.org JSON API.

Endpoints used:

- ``GET /api/single-cell/projects``
- ``GET /api/spatial/projects``
- ``GET /api/single-cell/facets``
- ``GET /api/spatial/facets``
"""

from __future__ import annotations

import time
from typing import Any, Callable, Mapping

import requests

from . import __version__

API_BASE = "https://seqout.org/api"
USER_AGENT = f"seqout-fetch/{__version__}"

PROJECT_ENDPOINTS = {
    "single-cell": "single-cell/projects",
    "spatial": "spatial/projects",
}
FACET_ENDPOINTS = {
    "single-cell": "single-cell/facets",
    "spatial": "spatial/facets",
}


class SeqoutError(RuntimeError):
    """Raised when the API cannot be reached or returns an error."""


def _get_json(
    session: requests.Session,
    url: str,
    params: Mapping[str, Any] | None = None,
    retries: int = 3,
    timeout: int = 60,
    backoff: float = 3.0,
) -> Any:
    """GET JSON with exponential backoff.

    seqout.org drops TLS connections occasionally, so a couple of retries
    turn a transient failure into a successful run.
    """
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            response = session.get(
                url,
                params=dict(params or {}),
                timeout=timeout,
                headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            )
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(backoff * attempt)

    raise SeqoutError(f"GET {url} failed after {retries} attempts: {last_error}")


def fetch_projects(
    dataset: str,
    filters: Mapping[str, Any],
    page_size: int = 100,
    max_records: int = 0,
    sleep: float = 0.5,
    sort: str = "year",
    order: str = "desc",
    session: requests.Session | None = None,
    retries: int = 3,
    timeout: int = 60,
    progress: Callable[[int, int], None] | None = None,
) -> list[dict[str, Any]]:
    """Page through one project endpoint and return every matching record."""
    if dataset not in PROJECT_ENDPOINTS:
        raise ValueError(f"unknown dataset: {dataset}")

    session = session or requests.Session()
    url = f"{API_BASE}/{PROJECT_ENDPOINTS[dataset]}"
    rows: list[dict[str, Any]] = []
    offset = 0

    while True:
        params = {key: value for key, value in filters.items() if value not in (None, "")}
        params.update(
            {"limit": page_size, "offset": offset, "sort": sort, "order": order}
        )

        payload = _get_json(session, url, params=params, retries=retries, timeout=timeout)
        total = payload.get("total", 0)
        batch = payload.get("results", [])

        rows.extend(batch)
        if progress:
            progress(len(rows), total)

        offset += payload.get("count", len(batch))
        if not batch or offset >= total:
            break
        if max_records and len(rows) >= max_records:
            break

        time.sleep(sleep)

    return rows[:max_records] if max_records else rows


def fetch_facets(
    dataset: str,
    session: requests.Session | None = None,
    retries: int = 3,
    timeout: int = 60,
) -> dict[str, Any]:
    """Return the facet counts (valid filter values) for one dataset."""
    if dataset not in FACET_ENDPOINTS:
        raise ValueError(f"unknown dataset: {dataset}")

    session = session or requests.Session()
    url = f"{API_BASE}/{FACET_ENDPOINTS[dataset]}"
    return _get_json(session, url, retries=retries, timeout=timeout)
