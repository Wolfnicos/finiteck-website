#!/usr/bin/env python3
"""Regenerate the checked-in CSS bundle without installing build dependencies."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
source = (root / 'css/style.css').read_text()
# Keep whitespace in values and selectors: calc() and descendant combinators need it.
compact = re.sub(r'/\*.*?\*/', '', source, flags=re.S)
compact = re.sub(r'\s+', ' ', compact)
compact = re.sub(r'\s*([{};])\s*', r'\1', compact).strip()
(root / 'css/style.min.css').write_text(compact + '\n')
print(f'CSS: {len(source):,} → {len(compact):,} bytes')
