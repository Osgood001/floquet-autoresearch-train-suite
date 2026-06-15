# Post-hoc evaluator

This directory contains the standalone train-suite evaluator used to reproduce the reported `train_closeness` metric.

Important: `train_suite_scorer.py` contains gold answers. It was **not** present in the solver-visible repository during the autoresearch run. During autoresearch, the workspace only contained `score.py`, which posted `predictions.json` to an opaque local HTTP endpoint and received the aggregate metric.

Use this evaluator after the fact for reproducibility, not as part of a black-box solving workspace.

Run as the same HTTP scorer shape used during autoresearch:

```bash
python3 evaluator/train_suite_scorer.py --port 8769
python3 score.py
```

Score a file directly:

```bash
python3 evaluator/train_suite_scorer.py --file predictions.json
```

Optional FastAPI mode, if `fastapi` and `uvicorn` are installed:

```bash
uvicorn evaluator.train_suite_scorer:app --host 127.0.0.1 --port 8769
```
