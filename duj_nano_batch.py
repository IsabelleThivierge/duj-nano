#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


MODES = ["duj", "control", "no_orbit_band"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--proof-script", type=str, default="duj_nano_proof.py")
    p.add_argument("--repeats", type=int, default=3)
    p.add_argument("--steps", type=int, default=320)
    p.add_argument("--state-dim", type=int, default=8192)
    p.add_argument("--seed", type=int, default=11)
    p.add_argument("--same-seed", action="store_true",
                   help="Use identical seed for every repeat (strict replay test).")
    p.add_argument("--noise-scale", type=float, default=0.001)
    p.add_argument("--out-csv", type=str, default="duj_nano_batch_results.csv")
    return p.parse_args()


def run_one(
    proof_script: str,
    mode: str,
    steps: int,
    state_dim: int,
    seed: int,
    noise_scale: float,
) -> Dict[str, Any]:

    cmd = [
        sys.executable,
        proof_script,
        "--mode", mode,
        "--steps", str(steps),
        "--state-dim", str(state_dim),
        "--seed", str(seed),
        "--noise-scale", str(noise_scale),
        "--json",
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("ERROR running:", " ".join(cmd))
        print(result.stderr)
        raise RuntimeError("Subprocess failed")

    try:
        data = json.loads(result.stdout)
    except Exception:
        print("Failed to parse JSON output:")
        print(result.stdout)
        raise

    return data


def summarize(mode_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    inv_avg = [r["summary"]["inv_avg"] for r in mode_results]
    inv_max = [r["summary"]["inv_max"] for r in mode_results]
    viol = [r["summary"]["viol_total"] for r in mode_results]
    first_pass = [r["summary"].get("first_pass") for r in mode_results]
    lat = [r["summary"]["lat_avg"] for r in mode_results]
    actives = [r["summary"]["actives"] for r in mode_results]

    return {
        "inv_avg": statistics.mean(inv_avg),
        "inv_max": statistics.mean(inv_max),
        "viol_mean": statistics.mean(viol),
        "first_pass": next((x for x in first_pass if x is not None), None),
        "lat_avg": statistics.mean(lat),
        "actives": statistics.mean(actives),
        "digest_stable": len(set(r["summary"]["digest"] for r in mode_results)) == 1,
    }


def main():
    args = parse_args()

    print(f"Using proof script: {args.proof_script}")
    print(f"Repeats per mode: {args.repeats}")
    print(f"Steps: {args.steps}")
    print(f"State dim: {args.state_dim}")
    print(f"Seed base: {args.seed}")
    print(f"Same seed mode: {'yes' if args.same_seed else 'no'}")
    print(f"Noise scale: {args.noise_scale}")
    print()

    all_results: Dict[str, List[Dict[str, Any]]] = {}

    for mode in MODES:
        print(f"Running mode: {mode}")
        mode_results = []

        for i in range(args.repeats):
            seed = args.seed if args.same_seed else args.seed + i

            result = run_one(
                args.proof_script,
                mode,
                args.steps,
                args.state_dim,
                seed,
                args.noise_scale,
            )

            s = result["summary"]

            print(
                f"  run {i+1}/{args.repeats} | seed={seed} "
                f"| inv_avg={s['inv_avg']:.6f} "
                f"| viol={s['viol_total']} "
                f"| fp={s.get('first_pass')} "
                f"| digest={s['digest'][:10]}..."
            )

            mode_results.append(result)

        all_results[mode] = mode_results
        print()

    print("mode          inv_avg   inv_max   viol_mean   first_pass   lat_avg   actives   digest_stable")
    print("----------------------------------------------------------------------------------------------")

    summary_rows = []

    for mode in MODES:
        summary = summarize(all_results[mode])

        print(
            f"{mode:<13}"
            f"{summary['inv_avg']:<10.4f}"
            f"{summary['inv_max']:<10.4f}"
            f"{summary['viol_mean']:<12.1f}"
            f"{str(summary['first_pass']):<13}"
            f"{summary['lat_avg']:<10.4f}"
            f"{summary['actives']:<10.4f}"
            f"{'yes' if summary['digest_stable'] else 'no'}"
        )

        summary_rows.append({
            "mode": mode,
            **summary
        })

    with open(args.out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=summary_rows[0].keys())
        writer.writeheader()
        writer.writerows(summary_rows)

    print()
    print(f"Saved CSV summary to: {args.out_csv}")
    print()
    print("Interpretation:")
    print("- Lower inv_avg / inv_max is better.")
    print("- Lower total_violations is better.")
    print("- Later first_passage_step is better; '-' means no passage detected.")
    print("- digest_stable=yes means exact replay stability across repeats.")
    print("- Use --same-seed for strict replay testing.")
    print("- Omit --same-seed to test robustness across different seeds.")


if __name__ == "__main__":
    main()
