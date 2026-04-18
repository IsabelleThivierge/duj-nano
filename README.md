# DUJ Nano — Minimal Stability Test

Nano-scale test harness demonstrating bounded vs divergent dynamics under noise in a constraint-enforced update rule.

## What this is

This repository contains a minimal, reproducible experiment comparing:

- `control` (unconstrained update)
- `duj` (constraint-enforced update)
- `no_orbit_band` (ablation)

## Key observation

Under identical stochastic forcing:

- **control** exhibits explosive divergence
- **duj** remains bounded through low and moderate noise
- **no_orbit_band** tracks `duj` closely in the current regime

This repository does **not** claim to be the full DUJ system. It isolates a minimal stabilizing slice that already shows a clear regime difference.

## Example runs

```bash
python3 duj_nano_batch.py --noise-scale 0.01
python3 duj_nano_batch.py --noise-scale 0.05
python3 duj_nano_batch.py --noise-scale 0.075
python3 duj_nano_batch.py --noise-scale 0.1
Yes. Do it in this order.

Step 1 — Edit the README first

On the repo page, tap the pencil icon in the README box.

Replace the current README with this:

# DUJ Nano — Minimal Stability Test
Nano-scale test harness demonstrating bounded vs divergent dynamics under noise in a constraint-enforced update rule.
## What this is
This repository contains a minimal, reproducible experiment comparing:
- `control` (unconstrained update)
- `duj` (constraint-enforced update)
- `no_orbit_band` (ablation)
## Key observation
Under identical stochastic forcing:
- **control** exhibits explosive divergence
- **duj** remains bounded through low and moderate noise
- **no_orbit_band** tracks `duj` closely in the current regime
This repository does **not** claim to be the full DUJ system. It isolates a minimal stabilizing slice that already shows a clear regime difference.
## Example runs
```bash
python3 duj_nano_batch.py --noise-scale 0.01
python3 duj_nano_batch.py --noise-scale 0.05
python3 duj_nano_batch.py --noise-scale 0.075
python3 duj_nano_batch.py --noise-scale 0.1

Metrics

* inv_avg, inv_max: invariant drift
* viol_mean: total violations
* first_pass: first detected collapse / passage
* lat_avg: latency proxy

Empirical summary

Observed behavior across current runs:

Noise	DUJ	Control
0.01	bounded, 0 violations	unstable
0.05	bounded, 0 violations	strong divergence
0.075	near-zero violations	catastrophic divergence
0.1	bounded degradation	explosive divergence

Interpretation

A constrained update rule produces a qualitative shift in system behavior:

* unconstrained → runaway divergence
* constrained → bounded dynamics with graceful degradation

Current limitations

* nano-scale only
* short horizon
* synthetic stress test
* current harness does not expose all DUJ components
* no_orbit_band ≈ duj in this regime, suggesting the dominant stabilizer is elsewhere in the stack

Purpose

To provide a minimal, reproducible experiment showing a structural stability difference under noise on edge hardware.

⸻
