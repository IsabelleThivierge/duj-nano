# DUJ Nano — Minimal Stability Test

Nano-scale test harness demonstrating bounded vs divergent dynamics under noise in a constraint-enforced update rule.

## Results summary

Observed behavior across runs (noise_scale=0.05, steps=320, state_dim=8192):
All runs use identical initialization seeds across modes to ensure direct comparability, unless otherwise specified.

- **Control**: rapid divergence — violation count grows exponentially, indicating an unstable regime under stochastic forcing.

- **DUJ (constraint-enforced)**: bounded behavior — violation count remains at zero across all tested steps, indicating preservation of a viable state region.

- **No_orbit_band (ablation)**: remains bounded in the current regime, suggesting that the primary stabilizing effect is not solely dependent on orbit-band structure.

**Key observation:**
Under identical noise and initialization, the system exhibits a clear regime shift:
- unconstrained → divergent
- constrained → bounded

This indicates that the update rule enforces a structural constraint that prevents trajectory escape under stochastic perturbation.
 
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
