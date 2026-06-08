"""
Pay Equity & Pay Transparency Analysis
--------------------------------------
A self-contained, reproducible pay-equity audit on SYNTHETIC compensation data.

The goal mirrors what a compensation team must do under Canada's 2026
pay-transparency laws (Ontario, BC): separate the *explained* portion of a
gender pay gap (driven by role, level, tenure) from the *unexplained* residual
that survives those controls -- the part that signals potential inequity --
and estimate the budget cost of remediation.

No real employee data is used. The dataset is generated with a fixed seed so
results are fully reproducible.

Run:  python3 analysis.py
Outputs: img/pay_gap_decomposition.png, img/residual_by_level.png, results.json
"""

import json
import os

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

SEED = 42
N = 1500
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(OUT_DIR, "img")
os.makedirs(IMG_DIR, exist_ok=True)


def generate_data(seed: int = SEED, n: int = N) -> pd.DataFrame:
    """Generate a synthetic but realistic compensation dataset.

    We deliberately bake in TWO things a real workforce shows:
      1. An *explained* gap: women are slightly over-represented in lower-paying
         job families and at lower levels (occupational segregation).
      2. An *unexplained* penalty: holding role, level, and tenure constant,
         women are paid a few percent less (the inequity we want to surface).
    """
    rng = np.random.default_rng(seed)

    job_families = {
        "Engineering": 135_000,
        "Data": 120_000,
        "Product": 125_000,
        "Operations": 85_000,
        "Support": 70_000,
    }

    female = rng.binomial(1, 0.45, n)

    # Occupational segregation: women slightly more likely in lower-paying families.
    fam_names = list(job_families.keys())
    base_probs = np.array([0.22, 0.18, 0.18, 0.22, 0.20])
    female_probs = np.array([0.14, 0.16, 0.16, 0.26, 0.28])
    roles = []
    for f in female:
        p = female_probs if f else base_probs
        roles.append(rng.choice(fam_names, p=p / p.sum()))
    roles = np.array(roles)

    # Level 1-5; women slightly under-represented at the top (glass ceiling).
    level = np.clip(rng.normal(2.8 - 0.25 * female, 1.0).round(), 1, 5).astype(int)
    tenure = np.clip(rng.gamma(2.0, 2.0, n), 0, 20)

    base = np.array([job_families[r] for r in roles], dtype=float)
    level_mult = 1 + 0.16 * (level - 1)        # ~16% per level
    tenure_effect = 1 + 0.012 * tenure          # ~1.2% per year
    noise = rng.normal(1.0, 0.06, n)

    # The unexplained penalty: ~5% lower pay for women, all else equal.
    unexplained_penalty = np.where(female == 1, 0.95, 1.0)

    salary = base * level_mult * tenure_effect * unexplained_penalty * noise

    return pd.DataFrame(
        {
            "salary": salary.round(0),
            "female": female,
            "role": roles,
            "level": level,
            "tenure": tenure.round(1),
        }
    )


def run_audit(df: pd.DataFrame) -> dict:
    """Raw gap vs. adjusted (unexplained) gap via OLS on log salary."""
    # Raw, unadjusted gap.
    mean_m = df.loc[df.female == 0, "salary"].mean()
    mean_f = df.loc[df.female == 1, "salary"].mean()
    raw_gap_pct = (mean_m - mean_f) / mean_m * 100

    # Adjusted model: control for role, level, tenure.
    model = smf.ols(
        "np.log(salary) ~ female + C(role) + level + tenure", data=df
    ).fit()
    female_coef = model.params["female"]
    female_p = model.pvalues["female"]
    # Convert log-point coefficient to an approximate percentage gap.
    adjusted_gap_pct = (1 - np.exp(female_coef)) * 100
    ci_low, ci_high = model.conf_int().loc["female"].tolist()
    adj_ci = [(1 - np.exp(ci_high)) * 100, (1 - np.exp(ci_low)) * 100]

    # Remediation: cost to lift each woman's pay by the unexplained percentage.
    women = df[df.female == 1]
    per_person_lift = women["salary"] * (np.exp(-female_coef) - 1)
    remediation_total = float(per_person_lift.sum())
    payroll = float(df["salary"].sum())

    return {
        "n": int(len(df)),
        "n_women": int(df.female.sum()),
        "mean_salary_men": round(mean_m),
        "mean_salary_women": round(mean_f),
        "raw_gap_pct": round(raw_gap_pct, 1),
        "adjusted_gap_pct": round(adjusted_gap_pct, 1),
        "adjusted_gap_ci": [round(adj_ci[0], 1), round(adj_ci[1], 1)],
        "female_pvalue": float(f"{female_p:.2e}"),
        "explained_gap_pct": round(raw_gap_pct - adjusted_gap_pct, 1),
        "remediation_total": round(remediation_total),
        "remediation_pct_of_payroll": round(remediation_total / payroll * 100, 2),
        "r_squared": round(model.rsquared, 3),
    }


def make_charts(df: pd.DataFrame, res: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.family": "serif", "axes.grid": False})

    # Chart 1: raw vs explained vs unexplained.
    fig, ax = plt.subplots(figsize=(7, 4.2))
    labels = ["Raw gap\n(unadjusted)", "Explained\n(role/level/tenure)", "Unexplained\n(adjusted residual)"]
    values = [res["raw_gap_pct"], res["explained_gap_pct"], res["adjusted_gap_pct"]]
    colors = ["#999999", "#34495e", "#cc0000"]
    bars = ax.bar(labels, values, color=colors, width=0.6)
    ax.set_ylabel("Gender pay gap (%)")
    ax.set_title("Decomposing the gender pay gap", fontstyle="italic")
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.1, f"{v:.1f}%", ha="center", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, "pay_gap_decomposition.png"), dpi=130, facecolor="#fffff8")
    plt.close(fig)

    # Chart 2: adjusted residual by level (where inequity concentrates).
    rows = []
    for lvl in sorted(df.level.unique()):
        sub = df[df.level == lvl]
        m = sub.loc[sub.female == 0, "salary"].mean()
        f = sub.loc[sub.female == 1, "salary"].mean()
        if m and not np.isnan(f):
            rows.append((lvl, (m - f) / m * 100))
    lvls, gaps = zip(*rows)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.bar([f"Level {l}" for l in lvls], gaps, color="#cc0000", width=0.6)
    ax.set_ylabel("Raw gap within level (%)")
    ax.set_title("Where the gap concentrates, by level", fontstyle="italic")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, "residual_by_level.png"), dpi=130, facecolor="#fffff8")
    plt.close(fig)


def main() -> None:
    df = generate_data()
    res = run_audit(df)
    make_charts(df, res)
    with open(os.path.join(OUT_DIR, "results.json"), "w") as fh:
        json.dump(res, fh, indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
