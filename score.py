#!/usr/bin/env python3
from __future__ import annotations
import json
import urllib.request
from pathlib import Path

pred_path = Path('predictions.json')
if not pred_path.exists():
    print('METRIC train_closeness=0.000000')
    raise SystemExit(0)
try:
    payload = pred_path.read_bytes()
    json.loads(payload)
except Exception:
    print('METRIC train_closeness=0.000000')
    raise SystemExit(0)
req = urllib.request.Request(
    'http://127.0.0.1:8769/score',
    data=payload,
    headers={'content-type': 'application/json'},
    method='POST',
)
try:
    result = json.loads(urllib.request.urlopen(req, timeout=10).read().decode())
    print(f"METRIC train_closeness={float(result['train_closeness']):.6f}")
except Exception:
    print('METRIC train_closeness=0.000000')
