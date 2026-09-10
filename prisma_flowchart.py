#!/usr/bin/env python3
"""Publication-style literature screening flowchart (PRISMA-adapted)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

FONT = "Liberation Sans"
INK = "#1B1B1B"
SLATE = "#2F3E4E"
BOX_FILL = "#FFFFFF"
EXCL_FILL = "#F3F3F3"
FINAL_FILL = "#EEF1F0"
NOTE_FILL = "#F7F7F7"

OUT_DIR = Path(__file__).resolve().parent / "img"


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": FONT,
            "font.size": 9,
            "text.color": INK,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def rbox(ax, x, y, w, h, *, fc, ec=INK, lw=0.9, radius=0.05, z=2):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        clip_on=False,
        zorder=z,
        joinstyle="miter",
    )
    ax.add_patch(patch)
    return patch


def arrow(ax, p1, p2, *, ls="solid", scale=9):
    ax.add_patch(
        FancyArrowPatch(
            p1,
            p2,
            arrowstyle="-|>",
            mutation_scale=scale,
            linewidth=0.9,
            linestyle=ls,
            color=INK,
            shrinkA=0.5,
            shrinkB=0.5,
            clip_on=False,
            zorder=5,
        )
    )


def text_stack(ax, cx, cy, lines, *, ha="center"):
    """Vertically centre a list of (text, size, weight, style)."""
    gaps = [max(0.145, size * 0.0158) for _, size, _, _ in lines]
    y = cy + sum(gaps) / 2.0
    for (text, size, weight, style), gap in zip(lines, gaps):
        ax.text(
            cx,
            y - gap / 2.0,
            text,
            fontsize=size,
            fontweight=weight,
            fontstyle=style,
            ha=ha,
            va="center",
            color=INK,
            family=FONT,
            zorder=4,
        )
        y -= gap


def draw_flowchart(stem: Path) -> None:
    configure_style()
    fig_w, fig_h = 13.85, 10.55
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    x_s, w_s = 0.24, 1.80
    x_m, w_m = 2.24, 6.10
    x_r, w_r = 8.60, 4.98
    xm = x_m + w_m / 2.0
    xr = x_r + w_r / 2.0

    # Row heights (inches), stacked from the bottom.
    h = {
        "id": 1.72,
        "dup": 0.68,
        "scr": 1.10,
        "full": 1.24,
        "cmp": 1.54,
        "inc": 0.68,
        "con": 1.14,
    }
    g, g_note = 0.28, 0.50
    y = {}
    y["con"] = 0.20
    y["inc"] = y["con"] + h["con"] + g_note
    y["cmp"] = y["inc"] + h["inc"] + g
    y["full"] = y["cmp"] + h["cmp"] + g
    y["scr"] = y["full"] + h["full"] + g
    y["dup"] = y["scr"] + h["scr"] + g
    y["id"] = y["dup"] + h["dup"] + g

    # Stage rail.
    stages = [
        (y["id"], h["id"], "IDENTIFICATION"),
        (y["scr"], (y["dup"] + h["dup"]) - y["scr"], "SCREENING"),
        (y["full"], h["full"], "ELIGIBILITY"),
        (y["cmp"], h["cmp"], "COMPARABILITY &\nDATA-USABILITY\nASSESSMENT"),
        (y["con"], (y["inc"] + h["inc"]) - y["con"], "INCLUDED"),
    ]
    for ys, hs, label in stages:
        rbox(ax, x_s, ys, w_s, hs, fc=SLATE, ec=SLATE, radius=0.03, lw=0.4)
        ax.text(
            x_s + w_s / 2.0,
            ys + hs / 2.0,
            label,
            ha="center",
            va="center",
            color="white",
            fontsize=8.0,
            fontweight="bold",
            family=FONT,
            linespacing=1.28,
            zorder=4,
        )

    # Identification (header + hairline + body).
    rbox(ax, x_m, y["id"], w_m, h["id"], fc=BOX_FILL)
    ax.text(
        xm,
        y["id"] + h["id"] - 0.22,
        "Identification of studies via databases and complementary searches",
        ha="center",
        va="center",
        fontsize=8.15,
        fontweight="bold",
        family=FONT,
        color=INK,
        zorder=4,
    )
    y_rule = y["id"] + h["id"] - 0.42
    ax.plot(
        [x_m + 0.45, x_m + w_m - 0.45],
        [y_rule, y_rule],
        color="#8A8A8A",
        lw=0.5,
        solid_capstyle="butt",
        zorder=4,
        clip_on=False,
    )
    text_stack(
        ax,
        xm,
        y["id"] + (y_rule - 0.08 - y["id"]) / 2.0,
        [
            ("Records identified through database searching", 9.05, "normal", "normal"),
            ("and complementary sources", 9.05, "normal", "normal"),
            ("", 3.4, "normal", "normal"),
            ("Databases: CNKI, Wanfang Data, Web of Science, Scopus", 8.05, "normal", "normal"),
            ("Additional sources: reference lists, institutional websites,", 8.05, "normal", "normal"),
            ("and general-purpose web searches", 8.05, "normal", "normal"),
            ("", 4.0, "normal", "normal"),
            ("n = 379", 10.0, "bold", "normal"),
        ],
    )

    main_h = {
        "id": h["id"],
        "dup": 0.68,
        "scr": 0.68,
        "full": 0.68,
        "cmp": 0.82,
        "inc": 0.68,
        "con": h["con"],
    }
    main_y = {k: y[k] + (h[k] - main_h[k]) / 2.0 for k in h}

    def main_box(key, lines, fill=BOX_FILL, lw=0.9):
        rbox(ax, x_m, main_y[key], w_m, main_h[key], fc=fill, lw=lw)
        text_stack(ax, xm, main_y[key] + main_h[key] / 2.0, lines)

    def excl_box(key, lines, *, ha="left"):
        rbox(ax, x_r, y[key], w_r, h[key], fc=EXCL_FILL)
        cx = xr if ha == "center" else x_r + 0.22
        text_stack(ax, cx, y[key] + h[key] / 2.0, lines, ha=ha)

    main_box(
        "dup",
        [
            ("Records after duplicates removed", 9.15, "normal", "normal"),
            ("n = 329", 10.0, "bold", "normal"),
        ],
    )
    main_box(
        "scr",
        [
            ("Records screened (title and abstract)", 9.15, "normal", "normal"),
            ("n = 329", 10.0, "bold", "normal"),
        ],
    )
    main_box(
        "full",
        [
            ("Full-text documents assessed for eligibility", 9.15, "normal", "normal"),
            ("n = 159", 10.0, "bold", "normal"),
        ],
    )
    main_box(
        "cmp",
        [
            ("Documents entering comparability and", 9.05, "normal", "normal"),
            ("data-usability assessment", 9.05, "normal", "normal"),
            ("n = 120", 10.0, "bold", "normal"),
        ],
    )
    main_box(
        "inc",
        [
            ("Documents included in the final review", 9.15, "normal", "normal"),
            ("n = 102", 10.0, "bold", "normal"),
        ],
    )
    main_box(
        "con",
        [
            ("Consolidated source-study / modeling-exercise records", 9.05, "normal", "normal"),
            ("n = 80", 10.2, "bold", "normal"),
            ("", 4.2, "normal", "normal"),
            ("275 coded scenario cases;  240 with principal", 8.1, "normal", "normal"),
            ("milestone-year quantitative outcomes", 8.1, "normal", "normal"),
        ],
        fill=FINAL_FILL,
        lw=1.1,
    )

    excl_box(
        "dup",
        [
            ("Duplicate records removed", 9.05, "normal", "normal"),
            ("n = 50", 10.0, "bold", "normal"),
        ],
        ha="center",
    )
    excl_box(
        "scr",
        [
            ("Records excluded after title and abstract screening", 8.2, "bold", "normal"),
            ("n = 170", 9.35, "bold", "normal"),
            ("–  Not related to China or coal power", 7.95, "normal", "normal"),
            ("–  Lacked a forward-looking scenario or projection", 7.95, "normal", "normal"),
            ("–  Focused only on specific technical issues", 7.95, "normal", "normal"),
        ],
    )
    excl_box(
        "full",
        [
            ("Full-text documents excluded", 8.2, "bold", "normal"),
            ("n = 39", 9.35, "bold", "normal"),
            ("–  Lacked China-specific coal-power outcomes", 7.95, "normal", "normal"),
            ("–  Not related to China or coal power", 7.95, "normal", "normal"),
            ("–  Lacked sufficiently defined scenario assumptions", 7.95, "normal", "normal"),
            ("–  Lacked extractable indicators", 7.95, "normal", "normal"),
        ],
    )
    excl_box(
        "cmp",
        [
            ("Documents excluded during comparability and", 8.15, "bold", "normal"),
            ("data-usability assessment", 8.15, "bold", "normal"),
            ("n = 18", 9.35, "bold", "normal"),
            ("–  Insufficiently defined scenario or pathway", 7.9, "normal", "normal"),
            ("–  Unclear or incompatible system / technology", 7.9, "normal", "normal"),
            ("    boundaries", 7.9, "normal", "normal"),
            ("–  Insufficiently transparent key assumptions", 7.9, "normal", "normal"),
            ("–  Quantitative outcomes insufficiently extractable", 7.9, "normal", "normal"),
            ("    or comparable", 7.9, "normal", "normal"),
        ],
    )

    # Consolidation note, vertically centred on the included → consolidated gap.
    y_gap = (main_y["inc"] + main_y["con"] + main_h["con"]) / 2.0
    h_note = 0.78
    y_note = y_gap - h_note / 2.0
    rbox(ax, x_r, y_note, w_r, h_note, fc=NOTE_FILL, lw=0.8)
    text_stack(
        ax,
        xr,
        y_note + h_note / 2.0,
        [
            ("Scenario consolidation to avoid double counting", 8.15, "normal", "italic"),
            ("and to handle multi-scenario publications", 8.15, "normal", "italic"),
        ],
    )

    # Main-flow arrows.
    order = ["id", "dup", "scr", "full", "cmp", "inc", "con"]
    for a, b in zip(order, order[1:]):
        arrow(ax, (xm, main_y[a]), (xm, main_y[b] + main_h[b]))

    dashed = (0, (2.4, 1.5))
    for key in ("dup", "scr", "full", "cmp"):
        yc = main_y[key] + main_h[key] / 2.0
        arrow(ax, (x_m + w_m, yc), (x_r, yc), ls=dashed)

    arrow(ax, (x_m + w_m, y_gap), (x_r, y_gap), ls=dashed)

    stem.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "svg", "png"):
        fig.savefig(
            stem.with_suffix(f".{ext}"),
            dpi=600 if ext == "png" else 300,
            facecolor="white",
            edgecolor="none",
            bbox_inches="tight",
            pad_inches=0.10,
        )
    plt.close(fig)


if __name__ == "__main__":
    draw_flowchart(OUT_DIR / "prisma_flowchart")
    print(f"Wrote {OUT_DIR / 'prisma_flowchart'}.{{pdf,svg,png}}")
