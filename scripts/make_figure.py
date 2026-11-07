"""Rebuild the country DPT table and figure from 480 aggregate rows.

Run from any directory: python path/to/repo/scripts/make_figure.py
No microdata or internal audit files required. No fitting or imputation.
"""
from pathlib import Path
import csv
import math
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

def calculate():
    with (ROOT / "data/derived/dpt_country_by_imputation.csv").open(
        encoding="utf-8", newline=""
    ) as f:
        inputs = list(csv.DictReader(f))
    assert len(inputs) == 480
    groups = defaultdict(list)
    for row in inputs:
        groups[int(row["cid"])].append(row)
    assert len(groups) == 48
    output = []
    for cid, rows in groups.items():
        assert sorted(int(r["imp"]) for r in rows) == list(range(1, 11))
        assert len({r["country"] for r in rows}) == 1
        assert len({int(r["n"]) for r in rows}) == 1
        values = [float(r["mean_dpt"]) for r in rows]
        assert all(math.isfinite(v) for v in values)
        output.append(dict(cid=cid, country=rows[0]["country"],
                           mean_dpt=math.fsum(values) / 10))
    output.sort(key=lambda r: (-r["mean_dpt"], r["country"]))
    for rank, row in enumerate(output, 1):
        row["rank"] = rank
    return output

def render(rows):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "svg.fonttype": "none"})
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 10.5))
    fig.patch.set_facecolor("#fcfcfa")
    reference = math.fsum(r["mean_dpt"] for r in rows) / len(rows)
    for ax, subset in zip(axes, [rows[:24], rows[24:]]):
        ax.set_facecolor("#fcfcfa")
        y = list(range(len(subset)))
        values = [r["mean_dpt"] for r in subset]
        ax.hlines(y, 0, values, colors="#d8e5e5", linewidth=2)
        ax.scatter(values, y, c="#176b70", s=30, zorder=3)
        ax.axvline(reference, color="#818789", linestyle=(0, (3, 3)), linewidth=1)
        ax.set_yticks(y, [r["country"] for r in subset], fontsize=9)
        ax.invert_yaxis()
        ax.set_xlim(0, 3.55)
        ax.set_xticks([0, 1, 2, 3])
        ax.set_xlabel("Mean daily playtime (hours)", labelpad=11)
        ax.tick_params(axis="both", length=0, pad=7)
        ax.grid(axis="x", color="#e8e8e4", linewidth=0.6)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_visible(False)
        for i, v in enumerate(values):
            ax.text(v + 0.10, i, f"{v:.2f}", va="center", fontsize=9, color="#314449",
                    bbox=dict(facecolor="#fcfcfa", edgecolor="none", pad=0.4))
    fig.suptitle("Daily gaming across 48 country and region samples", x=0.035,
                 y=0.97, ha="left", fontsize=20, fontweight="bold", color="#183e44")
    fig.text(0.035, 0.925,
             "Equal-weight average of ten imputation-specific means | PISA 2022 thesis data",
             fontsize=11, color="#526469")
    fig.text(0.035, 0.058,
             f"Dashed line: equal-country average ({reference:.2f} h). Points show unweighted sample means; no confidence intervals.",
             fontsize=10, color="#526469")
    fig.text(0.035, 0.030,
             "Portfolio recalculation: aggregation corrected; original imputations retained, including out-of-range values (2.69% of entries).",
             fontsize=9, color="#526469")
    fig.subplots_adjust(left=0.18, right=0.965, top=0.88, bottom=0.13, wspace=1.07)
    # Catch clipped figure/axis text before writing the review artifacts.
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bounds = fig.bbox
    for text in fig.findobj(matplotlib.text.Text):
        if not text.get_visible() or not text.get_text():
            continue
        box = text.get_window_extent(renderer)
        assert box.x0 >= bounds.x0 - 1 and box.x1 <= bounds.x1 + 1, text.get_text()
        assert box.y0 >= bounds.y0 - 1 and box.y1 <= bounds.y1 + 1, text.get_text()
    target = ROOT / "results/figures"
    target.mkdir(parents=True, exist_ok=True)
    fig.savefig(target / "daily_playtime.png", dpi=160, facecolor=fig.get_facecolor())
    fig.savefig(target / "daily_playtime.svg", facecolor=fig.get_facecolor())
    plt.close(fig)

if __name__ == "__main__":
    rows = calculate()
    target = ROOT / "results/tables"
    target.mkdir(parents=True, exist_ok=True)
    with (target / "daily_playtime.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["cid", "country", "mean_dpt", "rank"])
        writer.writeheader()
        writer.writerows(rows)
    render(rows)
    print("Verified 48 country summaries from 480 aggregate inputs; table and figures written.")
