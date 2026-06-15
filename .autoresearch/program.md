# Autoresearch: train_closeness

- Optimize: maximize
- Budget: 12
- Eval: python3 score.py
- Guard: python3 -m json.tool predictions.json >/dev/null

## Taste / keep-discard rules

- Keep only when the metric improves and the guard passes.
- Prefer the smallest change that moves the metric.
