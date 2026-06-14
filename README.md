# Floquet train-suite autoresearch lab

This is a black-box multi-problem autoresearch lab for the Floquet train split.

Visible files:

- `problems/*.json`: solver-visible problem statements for 12 train records.
- `problems/manifest.json`: record ids, tracks, model families, verifier type, and output keys only.
- `predictions.json`: create this file yourself. It is intentionally absent at startup.
- `score.py`: calls an opaque local scorer and prints only the aggregate metric.
- `solvers/`, `docs/`: build reusable code and notes here.

Metric contract:

- Metric name: `train_closeness`
- Range: `0.0` worst to `1.0` best
- Direction: higher is better
- Scorer output exposes only the aggregate metric, not per-record or per-field errors.

Goal:

Build a reusable Floquet problem-solving monorepo, not a one-off numeric guess file.
Kept experiments should add or improve reusable methods, modules, README/docs, or shared workflows.
