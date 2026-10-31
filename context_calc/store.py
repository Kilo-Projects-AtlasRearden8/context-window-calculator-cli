import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from .config import store_path


def _now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_estimates():
    path = store_path()
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    return data


def save_estimate(record):
    path = store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    estimates = load_estimates()
    entry = dict(record)
    entry.setdefault("saved_at", _now_iso())
    estimates.append(entry)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(estimates, handle, indent=2)
        handle.write("\n")
    return entry


def clear_estimates():
    path = store_path()
    if path.exists():
        path.unlink()
    return []


FIELDNAMES = [
    "saved_at",
    "model",
    "model_name",
    "context_window",
    "chars_per_token",
    "method",
    "reserve_completion",
    "source",
    "source_excerpt",
    "estimated_tokens",
    "available_for_prompt",
    "remaining_tokens",
    "fits_within_context",
    "percent_of_context",
]


def export_csv(path):
    estimates = load_estimates()
    out = Path(path)
    if out.parent and not out.parent.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        for estimate in estimates:
            writer.writerow(estimate)
    return len(estimates)
