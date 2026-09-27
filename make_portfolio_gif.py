#!/usr/bin/env python3
"""
GIF + PNG de un solo archivo para eToro.

Simulación buy & hold desde 2022-01-03 con base USD 10,000.
No incluye aportes mensuales (eso es el DCA del proceso, no de esta curva).
Pesos iniciales: 32% SPYG, 21% SMH, 20% IEMG, 20% BRK.B, 8% VTI.
VOO se grafica solo como referencia y no entra al mix.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from PIL import Image

OUT_DIR = Path(__file__).resolve().parent
CACHE = OUT_DIR / "data" / "prices_clean.csv"

COLORS = {
    "VTI": "#E0898A",
    "VOO": "#C6B14A",
    "SPYG": "#5BAF8A",
    "SMH": "#4C9BD8",
    "BRK-B": "#C084D0",
    "IEMG": "#E07A3A",
    "Portafolio": "#1F2A37",
}
WEIGHTS = {"SPYG": 0.32, "SMH": 0.21, "IEMG": 0.20, "BRK-B": 0.20, "VTI": 0.08}
ORDER = ["VTI", "VOO", "SPYG", "SMH", "BRK-B", "IEMG", "Portafolio"]
PLOT_ORDER = ["VTI", "VOO", "SPYG", "SMH", "BRK-B", "IEMG"]
LABELS = {
    "VTI": "VTI",
    "VOO": "VOO",
    "SPYG": "SPYG",
    "SMH": "SMH",
    "BRK-B": "BRK.B",
    "IEMG": "IEMG",
    "Portafolio": "Portafolio",
}
BASE = 10_000.0
START = "2022-01-01"
END = "2026-09-27"


def money(x: float) -> str:
    return f"${x:,.0f}"


def download_prices() -> pd.DataFrame:
    import yfinance as yf

    tickers = ["VTI", "VOO", "SPYG", "SMH", "IEMG"]
    df = yf.download(tickers, start=START, end=END, auto_adjust=True, progress=False)["Close"]
    brk = yf.download("BRK-B", start=START, end=END, auto_adjust=True, progress=False)["Close"]
    if isinstance(brk, pd.DataFrame):
        brk = brk.iloc[:, 0]
    df["BRK-B"] = brk
    df = df[PLOT_ORDER].dropna(how="any")
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CACHE)
    return df


def load() -> tuple[pd.DataFrame, pd.DataFrame]:
    if CACHE.exists():
        df = pd.read_csv(CACHE, parse_dates=["Date"], index_col="Date")
        df = df[PLOT_ORDER].dropna()
    else:
        df = download_prices()
    norm = df / df.iloc[0] * BASE
    port = sum(norm[t] * w for t, w in WEIGHTS.items())
    norm["Portafolio"] = port
    rets = df.pct_change()
    rets["Portafolio"] = port.pct_change()
    return norm.dropna(), rets.dropna()


def style_ax(ax):
    ax.set_facecolor("#FFFFFF")
    ax.grid(True, color="#E6E8EB", linewidth=0.8, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#B8BFC6")
    ax.spines["bottom"].set_color("#B8BFC6")
    ax.tick_params(colors="#5C6670", labelsize=8.5)


def draw_frame(norm: pd.DataFrame, rets: pd.DataFrame, end_idx: int) -> Image.Image:
    slice_n = norm.iloc[: end_idx + 1]
    last = slice_n.iloc[-1]
    date = slice_n.index[-1]

    fig = plt.figure(figsize=(9.0, 11.2), dpi=120, facecolor="#FFFFFF")
    gs = fig.add_gridspec(2, 1, height_ratios=[1.28, 1.0])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    ax1.set_position([0.10, 0.50, 0.66, 0.355])
    ax2.set_position([0.10, 0.07, 0.86, 0.34])
    style_ax(ax1)
    style_ax(ax2)

    fig.text(0.10, 0.965, "DCA + diseño del portafolio", fontsize=16.5, fontweight="bold", color="#1F2A37", ha="left", va="top")
    fig.text(0.10, 0.928, "Cómo se suavizan los días malos… y también parte de los buenos", fontsize=10.2, color="#5C6670", ha="left", va="top")
    fig.text(0.97, 0.965, date.strftime("%d %b %Y"), fontsize=10.5, color="#1F2A37", ha="right", va="top")

    ax1.axhline(BASE, color="#C5CAD0", lw=1.0, ls="--", zorder=1)
    for t in PLOT_ORDER:
        ax1.plot(slice_n.index, slice_n[t], color=COLORS[t], lw=1.55, alpha=0.88, zorder=2, solid_capstyle="round")
    ax1.plot(slice_n.index, slice_n["Portafolio"], color=COLORS["Portafolio"], lw=2.65, zorder=3, solid_capstyle="round")
    for t in ORDER:
        ax1.scatter(date, last[t], s=26 if t == "Portafolio" else 18, color=COLORS[t], zorder=4, edgecolors="white", linewidths=0.5)

    ax1.set_xlim(norm.index[0], norm.index[-1] + pd.Timedelta(days=18))
    ax1.set_ylim(BASE * 0.42, max(BASE * 4.25, float(norm.max().max()) * 1.06))
    ax1.set_ylabel("Valor de $10,000 iniciales", fontsize=9.2, color="#3D4650")
    ax1.set_title("Evolución  ·  Base $10,000 desde 2022-01-03  ·  sin aportes extra", fontsize=10.2, color="#1F2A37", loc="left", pad=8)
    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _p: f"${x/1000:.0f}k"))

    fig.text(0.80, 0.835, "De $10,000 a…", fontsize=8.0, color="#8A9299", fontweight="bold")
    for i, t in enumerate(ORDER):
        y = 0.812 - i * 0.028
        fig.text(0.80, y, "●", fontsize=10, color=COLORS[t], ha="left", va="center")
        fig.text(0.825, y, f"{LABELS[t]}  {money(last[t])}", fontsize=8.1, color="#1F2A37", ha="left", va="center", fontweight="bold" if t == "Portafolio" else "regular")

    fig.text(0.10, 0.898, "Buy&hold  32% SPYG · 21% SMH · 20% IEMG · 20% BRK.B · 8% VTI   ·   VOO solo referencia", fontsize=7.2, color="#5C6670", ha="left", va="top")

    data = [rets[t].values * 100 for t in ORDER]
    bp = ax2.boxplot(
        data,
        tick_labels=[LABELS[t] for t in ORDER],
        patch_artist=True,
        widths=0.62,
        showfliers=True,
        flierprops=dict(marker="o", markersize=2.2, markerfacecolor="#2B2B2B", markeredgecolor="none", alpha=0.35),
        medianprops=dict(color="#1F2A37", linewidth=1.4),
        whiskerprops=dict(color="#4A5560", linewidth=1.0),
        capprops=dict(color="#4A5560", linewidth=1.0),
        boxprops=dict(linewidth=0.9, edgecolor="#4A5560"),
        zorder=3,
    )
    for patch, t in zip(bp["boxes"], ORDER):
        patch.set_facecolor(COLORS[t])
        patch.set_alpha(0.82 if t != "Portafolio" else 0.95)

    ax2.axhline(0.0, color="#D94848", lw=0.9, ls="--", alpha=0.75, zorder=1)
    ax2.set_ylim(-12.5, 18.5)
    ax2.set_ylabel("Retorno diario", fontsize=9.5, color="#3D4650")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _p: f"{x:.0f}%"))
    ax2.set_title("Boxplot de retornos diarios  ·  Mediana, dispersión y outliers", fontsize=10.6, color="#1F2A37", loc="left", pad=8)
    ax2.set_xlabel("")
    ax2.text(0.99, 0.96, "El mix recorta la cola de SMH\nen ambos sentidos", transform=ax2.transAxes, fontsize=7.4, color="#1F2A37", ha="right", va="top", linespacing=1.25)
    fig.text(0.10, 0.018, "Precios ajustados (Yahoo). Buy&hold con pesos iniciales, sin rebalanceo diario.  ·  Pasado ≠ futuro.  ·  Educativo, no recomendación.", fontsize=6.4, color="#8A9299", ha="left", va="bottom")

    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    buf = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8).reshape(h, w, 4)
    img = Image.fromarray(buf).convert("RGB")
    plt.close(fig)
    return img


def main():
    norm, rets = load()
    n = len(norm)
    step_idx = np.unique(np.linspace(40, n - 1, 46, dtype=int))
    print(f"rows={n}  frames={len(step_idx)}  last={norm.index[-1].date()}")
    print(norm.iloc[-1].round(0).to_string())

    frames = []
    for i, idx in enumerate(step_idx):
        frames.append(draw_frame(norm, rets, int(idx)))
        if i % 8 == 0:
            print(f"  frame {i+1}/{len(step_idx)}  {norm.index[idx].date()}")

    gif_path = OUT_DIR / "portafolio_dca_suaviza.gif"
    png_path = OUT_DIR / "portafolio_dca_suaviza.png"
    durations = [130] * (len(frames) - 1) + [2200]
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=False, disposal=2)
    frames[-1].save(png_path, optimize=True)
    print("GIF", gif_path, f"{gif_path.stat().st_size/1e6:.2f} MB")
    print("PNG", png_path, f"{png_path.stat().st_size/1e6:.2f} MB")


if __name__ == "__main__":
    main()
