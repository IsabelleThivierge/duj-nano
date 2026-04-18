#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import numpy as np


# ----------------------------
# Utilities
# ----------------------------

def stable_digest(x: np.ndarray) -> str:
    """Small, stable fingerprint of the state."""
    import hashlib
    h = hashlib.sha256(x.tobytes()).hexdigest()
    return h[:16]


def now():
    return time.perf_counter()


# ----------------------------
# Core dynamics
# ----------------------------

@dataclass
class State:
    x: np.ndarray
    target: np.ndarray


def make_initial_states(seed: int, state_dim: int) -> State:
    rng = np.random.default_rng(seed)
    # Start near target (origin) but with small offset
    x0 = rng.normal(0.0, 0.05, size=(state_dim,))
    target = np.zeros_like(x0)
    return State(x=x0, target=target)


def control_step(x: np.ndarray, target: np.ndarray, noise: np.ndarray) -> np.ndarray:
    """
    Unconstrained (baseline) update:
    simple attraction + noise, which becomes unstable under larger noise.
    """
    # small attraction toward target
    drift = -0.02 * (x - target)
    # additive noise
    x_next = x + drift + noise
    return x_next


def duj_step(
    x: np.ndarray,
    target: np.ndarray,
    noise: np.ndarray,
    radius: float = 2.5,
    lr: float = 0.05,
) -> np.ndarray:
    """
    Minimal DUJ-like constrained update:
    gradient-like attraction + projection into a bounded manifold (radius ball).
    """
    # gradient step toward target
    grad = (target - x)
    x_next = x + lr * grad + noise

    # invariant projection (bounded radius)
    norm = np.linalg.norm(x_next)
    if norm > radius:
        x_next = (x_next / (norm + 1e-12)) * radius

    return x_next


# ----------------------------
# Simulation
# ----------------------------

def run_sim(
    mode: str,
    steps: int,
    state_dim: int,
    seed: int,
    noise_scale: float,
) -> Dict[str, Any]:

    rng = np.random.default_rng(seed)
    st = make_initial_states(seed, state_dim)

    x = st.x
    target = st.target

    inv_vals = []
    viol_total = 0
    first_pass: Optional[int] = None

    t0 = now()

    for t in range(steps):
        noise = rng.normal(0.0, noise_scale, size=x.shape)

        if mode == "control":
            x = control_step(x, target, noise)

        elif mode == "duj":
            x = duj_step(x, target, noise)

        elif mode == "no_orbit_band":
            # In this nano harness, this matches DUJ behavior (ablation)
            x = duj_step(x, target, noise)

        else:
            raise ValueError(f"Unknown mode: {mode}")

        # Invariant proxy: distance from target (L2)
        inv = float(np.linalg.norm(x - target))
        inv_vals.append(inv)

        # Violation: exceeding a soft threshold
        if inv > 3.0:
            viol_total += 1
            if first_pass is None:
                first_pass = t

    t1 = now()

    inv_avg = float(np.mean(inv_vals))
    inv_max = float(np.max(inv_vals))
    lat_avg = (t1 - t0) / max(1, steps)

    summary = {
        "inv_avg": inv_avg,
        "inv_max": inv_max,
        "viol_total": int(viol_total),
        "first_pass": first_pass,
        "lat_avg": float(lat_avg),
        "actives": float(state_dim),
        "digest": stable_digest(x),
    }

    return {
        "config": {
            "mode": mode,
            "steps": steps,
            "state_dim": state_dim,
            "seed": seed,
            "noise_scale": noise_scale,
        },
        "summary": summary,
    }


# ----------------------------
# CLI
# ----------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", type=str, choices=["duj", "control", "no_orbit_band"], default="duj")
    p.add_argument("--steps", type=int, default=320)
    p.add_argument("--state-dim", type=int, default=8192)
    p.add_argument("--seed", type=int, default=11)
    p.add_argument("--noise-scale", type=float, default=0.001)
    p.add_argument("--json", action="store_true", help="Output JSON only")
    return p.parse_args()


def main():
    args = parse_args()

    result = run_sim(
        mode=args.mode,
        steps=args.steps,
        state_dim=args.state_dim,
        seed=args.seed,
        noise_scale=args.noise_scale,
    )

    if args.json:
        print(json.dumps(result))
    else:
        s = result["summary"]
        print("mode:", args.mode)
        print(f"inv_avg={s['inv_avg']:.6f}")
        print(f"inv_max={s['inv_max']:.6f}")
        print(f"viol_total={s['viol_total']}")
        print(f"first_pass={s['first_pass']}")
        print(f"lat_avg={s['lat_avg']:.6f}")
        print(f"digest={s['digest']}")


if __name__ == "__main__":
    main()
