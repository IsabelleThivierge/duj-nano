# DUJ Nano — Minimal Stability Test

Nano-scale test harness demonstrating bounded vs divergent dynamics under noise in a constraint-enforced update rule.

## Results summary

Observed behavior across runs:

- Control: divergence (violations explode)
- DUJ: bounded invariant, stable
- No_orbit_band: matches DUJ in current regime

Nano-scale test harness demonstrating bounded vs divergent dynamics under noise in a constraint-enforced update rule.

## Quick Start

```bash
pip install numpy
python3 duj_nano_batch.py --noise-scale 0.05
```

## What this is

This repository contains a minimal, reproducible experiment comparing:

- `control` (unconstrained update)
- `duj` (constraint-enforced update)
- `no_orbit_band` (ablation)

## Key observation

Under identical stochastic forcing:

- `control` exhibits explosive divergence  
- `duj` remains bounded through low and moderate noise  
- `no_orbit_band` tracks `duj` closely in the current regime  

This repository does not claim to be the full DUJ system. It isolates a minimal stabilizing slice that already shows a clear regime difference.

## Expected behavior

Typical outcome:

- `control` → rapidly increasing violations, often explosive  
- `duj` → bounded invariant, zero or near-zero violations  
- `no_orbit_band` → similar to `duj` in this regime  

This difference should be observable across multiple seeds.

## Example runs

```bash
python3 duj_nano_batch.py --noise-scale 0.01
python3 duj_nano_batch.py --noise-scale 0.05
python3 duj_nano_batch.py --noise-scale 0.075
python3 duj_nano_batch.py --noise-scale 0.1
```
