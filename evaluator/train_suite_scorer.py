#!/usr/bin/env python3
"""Standalone post-hoc evaluator for the train-suite repo.

This file contains gold answers and was NOT present in the solver-visible
repository during the autoresearch run. During training, the agent only saw
score.py, which called an opaque local HTTP endpoint returning the aggregate
train_closeness metric.

Publish this evaluator only for reproducibility after the run. Do not place it
inside a live autoresearch workspace unless the goal is no longer black-box.
"""
from __future__ import annotations

import json
import math
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

GOLD: dict[str, Any] = {
    "records": {
        "flq-b1-nhqw-nonbloch": {
            "track": "B1",
            "track_dir": "B1-topo-invariants",
            "model_family": "quantum-walk",
            "answer": {"winding_number": 1},
            "verifier": {"type": "integer_exact"},
        },
        "flq-b1-bbh-n0-0-npi-4": {
            "track": "B1",
            "track_dir": "B1-topo-invariants",
            "model_family": "bbh-lattice",
            "answer": {"N_0": 0, "N_pi": 4, "corner_states_pi_gap": 16},
            "verifier": {"type": "integer_exact"},
        },
        "flq-b1-kicked-ssh-chern2": {
            "track": "B1",
            "track_dir": "B1-topo-invariants",
            "model_family": "kicked-ssh",
            "answer": {"max_chern_number_magnitude": 2},
            "verifier": {"type": "integer_exact"},
        },
        "flq-b1-kagome-magnon": {
            "track": "B1",
            "track_dir": "B1-topo-invariants",
            "model_family": "magnon-honeycomb",
            "answer": {"chern_lower": 1, "chern_middle": 0, "chern_upper": -1},
            "verifier": {"type": "integer_exact"},
        },
        "flq-b1-hofstadter-chern": {
            "track": "B1",
            "track_dir": "B1-topo-invariants",
            "model_family": "graphene-driven",
            "answer": {"chern_number_lowest_band": 1},
            "verifier": {"type": "integer_exact"},
        },
        "flq-b1-kicked-rotor-dirac": {
            "track": "B1",
            "track_dir": "B1-topo-invariants",
            "model_family": "kicked-rotor",
            "answer": {"edge_state_count": 2},
            "verifier": {"type": "integer_exact"},
        },
        "flq-b3-4d-qhe-floquet-muc-classA": {
            "track": "B3",
            "track_dir": "B3-critical-points",
            "model_family": "floquet-4d-dirac",
            "answer": {"mu_c_classA_C-1": 3.51},
            "verifier": {"type": "scalar_tolerance", "rel_tol": 0.003561},
        },
        "flq-b3-two-electron-doublon-localization": {
            "track": "B3",
            "track_dir": "B3-critical-points",
            "model_family": "hubbard-doublon",
            "answer": {"A_over_omega_DL": 1.2024},
            "verifier": {"type": "scalar_tolerance"},
        },
        "flq-b3-floquet-delta-ad-zero-threshold": {
            "track": "B3",
            "track_dir": "B3-critical-points",
            "model_family": "floquet-delta-scatterer",
            "answer": {"a_d_c1": 0.782},
            "verifier": {"type": "scalar_tolerance", "rel_tol": 0.001598},
        },
        "flq-b3-floquet-delta-ad-pole-domain-exit": {
            "track": "B3",
            "track_dir": "B3-critical-points",
            "model_family": "floquet-delta-scatterer",
            "answer": {"a_d_c2": 0.935},
            "verifier": {"type": "scalar_tolerance", "rel_tol": 0.001337},
        },
        "flq-b3-weyl-like-node-coalescence-A0c": {
            "track": "B3",
            "track_dir": "B3-critical-points",
            "model_family": "floquet-weyl-stacked-chern",
            "answer": {"A0c_inv_nm": 1.034},
            "verifier": {"type": "scalar_tolerance", "rel_tol": 0.001209},
        },
        "flq-b3-photonic-hubbard-cdt-amplitude": {
            "track": "B3",
            "track_dir": "B3-critical-points",
            "model_family": "hubbard-doublon",
            "answer": {"A_CDT_um": 11.0},
            "verifier": {"type": "scalar_tolerance", "rel_tol": 0.1},
        },
    }
}
TRACK_WEIGHTS = {"B1": 0.5, "B3": 0.5}


def as_float(value: Any) -> float:
    if isinstance(value, bool):
        raise ValueError("bool is not numeric")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("non-finite")
    return number


def field_score(got: Any, ref: Any, verifier_type: str | None) -> float:
    try:
        got_value = as_float(got)
        ref_value = as_float(ref)
    except Exception:
        return 0.0

    if verifier_type == "integer_exact":
        return 1.0 if int(round(got_value)) == int(ref_value) and abs(got_value - round(got_value)) < 1e-9 else 0.0

    scale = max(abs(ref_value), 1.0)
    error = abs(got_value - ref_value) / scale
    return max(0.0, 1.0 - min(error, 1.0))


def score_predictions(predictions: Any) -> float:
    if not isinstance(predictions, dict):
        return 0.0

    by_track: dict[str, list[float]] = {"B1": [], "B3": []}
    for record_id, record in GOLD["records"].items():
        expected = record["answer"] or {}
        verifier_type = (record.get("verifier") or {}).get("type")
        track = record.get("track")
        entry = predictions.get(record_id)

        if not isinstance(entry, dict):
            record_score = 0.0
        else:
            values = [field_score(entry.get(key), ref, verifier_type) for key, ref in expected.items()]
            record_score = sum(values) / len(values) if values else 0.0
            if set(entry) - set(expected):
                record_score *= 0.8

        by_track.setdefault(track, []).append(record_score)

    total = 0.0
    weight_sum = 0.0
    for track, values in by_track.items():
        if not values:
            continue
        weight = TRACK_WEIGHTS.get(track, 1.0)
        total += weight * (sum(values) / len(values))
        weight_sum += weight
    return total / weight_sum if weight_sum else 0.0


def score_file(path: str | Path = "predictions.json") -> float:
    return score_predictions(json.loads(Path(path).read_text()))


try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except Exception:
    FastAPI = None
    BaseModel = object

if FastAPI is not None:
    app = FastAPI(title="Floquet train-suite post-hoc evaluator")

    @app.post("/score")
    async def score_endpoint(payload: dict[str, Any]) -> dict[str, float]:
        return {"train_closeness": round(float(score_predictions(payload)), 6)}
else:
    app = None


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: Any) -> None:
        return

    def do_POST(self) -> None:
        if self.path != "/score":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("content-length", "0") or 0)
        try:
            predictions = json.loads(self.rfile.read(length).decode())
            metric = score_predictions(predictions)
            body = json.dumps({"train_closeness": round(float(metric), 6)}).encode()
        except Exception:
            body = json.dumps({"train_closeness": 0.0}).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Post-hoc evaluator for train-suite predictions")
    parser.add_argument("--file", default=None, help="Score a predictions JSON file and exit")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8769)
    args = parser.parse_args()

    if args.file:
        print(f"METRIC train_closeness={score_file(args.file):.6f}")
    else:
        print(f"Serving post-hoc evaluator on http://{args.host}:{args.port}/score")
        HTTPServer((args.host, args.port), Handler).serve_forever()
