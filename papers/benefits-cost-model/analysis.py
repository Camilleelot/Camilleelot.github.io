"""
Gender-Affirming Benefits Cost Model
------------------------------------
Estimates the annual employer cost of adding comprehensive gender-affirming
health coverage, the way a total-rewards team would benchmark it before
recommending the benefit to leadership.

The headline metric is PEPY -- cost Per Employee Per Year -- because that is
what benefits teams and insurers actually negotiate on. A useful property falls
out of the math: PEPY does NOT depend on headcount, so a 500-person nonprofit
and a 20,000-person enterprise face the same *per-employee* cost; only the total
scales. This is why employers consistently report "insignificant or no premium
increase" after adding the benefit.

All inputs are transparent, adjustable assumptions -- not real claims data.

Run:  python3 analysis.py
Outputs: img/pepy_sensitivity.png, img/total_by_size.png, results.json
"""

import json
import os

import numpy as np

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(OUT_DIR, "img")
os.makedirs(IMG_DIR, exist_ok=True)

# ---- Baseline assumptions (all adjustable) -------------------------------
# Share of the workforce who are transgender / gender-diverse.
PREVALENCE = 0.006          # 0.6%
# Of those, the share actively claiming gender-affirming care in a given year.
ANNUAL_UTILIZATION = 0.30   # 30%
# Expected annual claim per *actively transitioning* member, blending:
#   mental health (~$1.5k/yr), hormone therapy (~$1.5k/yr), and the amortized
#   expected value of episodic surgical care (spread over years, not everyone).
AVG_ANNUAL_CLAIM = 12_000

WORKFORCE_SIZES = [500, 2_000, 10_000, 25_000]


def pepy(prevalence: float, utilization: float, avg_claim: float) -> float:
    """Cost per employee per year. Independent of headcount by construction."""
    return prevalence * utilization * avg_claim


def model() -> dict:
    base_pepy = pepy(PREVALENCE, ANNUAL_UTILIZATION, AVG_ANNUAL_CLAIM)

    by_size = []
    for n in WORKFORCE_SIZES:
        total = base_pepy * n
        expected_users = PREVALENCE * ANNUAL_UTILIZATION * n
        by_size.append(
            {
                "employees": n,
                "expected_annual_users": round(expected_users, 1),
                "total_annual_cost": round(total),
                "pepy": round(base_pepy, 2),
            }
        )

    # Compare PEPY against a typical total benefits spend (~$8,000 PEPY) to show
    # how small the marginal cost is.
    typical_benefits_pepy = 8_000
    share_of_benefits = base_pepy / typical_benefits_pepy * 100

    return {
        "assumptions": {
            "prevalence": PREVALENCE,
            "annual_utilization": ANNUAL_UTILIZATION,
            "avg_annual_claim": AVG_ANNUAL_CLAIM,
        },
        "baseline_pepy": round(base_pepy, 2),
        "share_of_typical_benefits_pepy_pct": round(share_of_benefits, 3),
        "by_workforce_size": by_size,
    }


def make_charts(res: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.family": "serif"})

    # Chart 1: PEPY sensitivity heatmap over prevalence x utilization.
    prevalences = np.array([0.003, 0.006, 0.009, 0.012, 0.015])
    utilizations = np.array([0.10, 0.20, 0.30, 0.40, 0.50, 0.60])
    grid = np.array(
        [[pepy(p, u, AVG_ANNUAL_CLAIM) for u in utilizations] for p in prevalences]
    )

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    im = ax.imshow(grid, cmap="Reds", aspect="auto", origin="lower")
    ax.set_xticks(range(len(utilizations)))
    ax.set_xticklabels([f"{int(u*100)}%" for u in utilizations])
    ax.set_yticks(range(len(prevalences)))
    ax.set_yticklabels([f"{p*100:.1f}%" for p in prevalences])
    ax.set_xlabel("Annual utilization (share of eligible members claiming)")
    ax.set_ylabel("Trans / gender-diverse prevalence")
    ax.set_title("Cost per employee per year ($)", fontstyle="italic")
    for i in range(len(prevalences)):
        for j in range(len(utilizations)):
            ax.text(j, i, f"${grid[i, j]:.0f}", ha="center", va="center",
                    fontsize=8, color="#111" if grid[i, j] < grid.max() * 0.6 else "#fff")
    fig.colorbar(im, ax=ax, label="PEPY ($)")
    fig.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, "pepy_sensitivity.png"), dpi=130, facecolor="#fffff8")
    plt.close(fig)

    # Chart 2: total annual cost by workforce size (baseline).
    sizes = [r["employees"] for r in res["by_workforce_size"]]
    totals = [r["total_annual_cost"] for r in res["by_workforce_size"]]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    bars = ax.bar([f"{s:,}" for s in sizes], totals, color="#34495e", width=0.6)
    ax.set_ylabel("Total annual cost ($)")
    ax.set_xlabel("Workforce size")
    ax.set_title(f"Total cost at baseline (${res['baseline_pepy']:.0f} PEPY)", fontstyle="italic")
    for b, v in zip(bars, totals):
        ax.text(b.get_x() + b.get_width() / 2, v, f"${v:,.0f}", ha="center",
                va="bottom", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, "total_by_size.png"), dpi=130, facecolor="#fffff8")
    plt.close(fig)


def main() -> None:
    res = model()
    make_charts(res)
    with open(os.path.join(OUT_DIR, "results.json"), "w") as fh:
        json.dump(res, fh, indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
