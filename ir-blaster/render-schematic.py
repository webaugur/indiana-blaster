#!/usr/bin/env python3
"""Render ir-blaster-schematic.png (Uno + transistor IR LED)."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D

OUT = Path(__file__).resolve().parent / "ir-blaster-schematic.png"


def wire(ax, pts, **kw):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color="#1a1a1a", lw=2.2, solid_capstyle="round", **kw)


def node(ax, x, y):
    ax.add_patch(Circle((x, y), 0.07, fc="#1a1a1a", zorder=5))


def label(ax, x, y, text, **kw):
    kw.setdefault("fontsize", 11)
    kw.setdefault("fontfamily", "DejaVu Sans")
    kw.setdefault("color", "#111")
    ax.text(x, y, text, **kw)


def main():
    fig, ax = plt.subplots(figsize=(16.5, 8.6), dpi=140)
    ax.set_xlim(0, 16.5)
    ax.set_ylim(0, 8.6)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("#f4f1ea")
    ax.set_facecolor("#f4f1ea")

    # Uno board
    uno = FancyBboxPatch(
        (0.4, 1.4),
        3.4,
        5.4,
        boxstyle="round,pad=0.04,rounding_size=0.12",
        facecolor="#1b6b4a",
        edgecolor="#0d3d2a",
        lw=2,
    )
    ax.add_patch(uno)
    label(ax, 2.1, 6.5, "Arduino Uno", ha="center", va="center", color="white", fontsize=14, fontweight="bold")
    label(ax, 2.1, 6.1, "5 V USB / barrel", ha="center", va="center", color="#d4f5e6", fontsize=9)

    # Pin blocks
    pins = [
        (1.1, 5.35, "5V", "#c0392b"),
        (1.1, 4.25, "D3", "#f39c12"),
        (1.1, 3.15, "GND", "#2c3e50"),
    ]
    for x, y, name, col in pins:
        ax.add_patch(FancyBboxPatch((x - 0.45, y - 0.32), 1.7, 0.64, boxstyle="round,pad=0.02", fc=col, ec="none"))
        label(ax, x + 0.4, y, name, ha="center", va="center", color="white", fontsize=13, fontweight="bold")

    label(ax, 2.1, 2.15, "D3 = 38 kHz carrier", ha="center", color="#eafaf1", fontsize=9)
    label(ax, 2.1, 1.8, "do not drive LED from D3 alone", ha="center", color="#ffd7a8", fontsize=8)

    # 1k base resistor (zigzag)
    rx, ry = 4.55, 4.25
    zig_x = [rx, rx + 0.18]
    zig_y = [ry, ry]
    for i in range(5):
        zig_x.append(rx + 0.28 + i * 0.18)
        zig_y.append(ry + (0.22 if i % 2 == 0 else -0.22))
    zig_x += [rx + 1.28, rx + 1.45]
    zig_y += [ry, ry]
    ax.plot(zig_x, zig_y, color="#1a1a1a", lw=2.2)
    label(ax, rx + 0.72, ry + 0.48, "1 kΩ", ha="center", fontsize=12, fontweight="bold")
    label(ax, rx + 0.72, ry - 0.48, "base", ha="center", fontsize=9, color="#444")

    # 100 ohm collector resistor
    rx2, ry2 = 5.35, 5.35
    zig_x = [rx2, rx2 + 0.18]
    zig_y = [ry2, ry2]
    for i in range(5):
        zig_x.append(rx2 + 0.28 + i * 0.18)
        zig_y.append(ry2 + (0.22 if i % 2 == 0 else -0.22))
    zig_x += [rx2 + 1.28, rx2 + 1.45]
    zig_y += [ry2, ry2]
    ax.plot(zig_x, zig_y, color="#1a1a1a", lw=2.2)
    label(ax, rx2 + 0.72, ry2 + 0.48, "100 Ω", ha="center", fontsize=12, fontweight="bold")

    # Transistor 2N2222
    tx, ty = 8.15, 4.25
    ax.add_patch(Circle((tx, ty), 0.72, fc="#ece6d8", ec="#1a1a1a", lw=2))
    # emitter / collector / base legs inside
    ax.plot([tx - 0.35, tx + 0.15], [ty, ty], color="#1a1a1a", lw=2)
    ax.plot([tx + 0.15, tx + 0.42], [ty, ty + 0.55], color="#1a1a1a", lw=2)
    ax.plot([tx + 0.15, tx + 0.42], [ty, ty - 0.55], color="#1a1a1a", lw=2)
    # emitter arrow
    ax.annotate(
        "",
        xy=(tx + 0.42, ty - 0.55),
        xytext=(tx + 0.22, ty - 0.22),
        arrowprops=dict(arrowstyle="->", color="#1a1a1a", lw=1.8),
    )
    label(ax, tx, ty - 1.05, "2N2222 / 2N3904", ha="center", fontsize=11, fontweight="bold")
    label(ax, tx, ty - 1.35, "NPN", ha="center", fontsize=9, color="#444")
    label(ax, tx - 0.95, ty + 0.05, "B", fontsize=10, color="#555")
    label(ax, tx + 0.55, ty + 0.72, "C", fontsize=10, color="#555")
    label(ax, tx + 0.55, ty - 0.78, "E", fontsize=10, color="#555")

    # IR LED
    lx, ly = 8.15, 5.35
    ax.add_patch(Circle((lx - 0.28, ly), 0.22, fc="#f7d6d6", ec="#1a1a1a", lw=1.6))
    ax.plot([lx - 0.08, lx + 0.28], [ly + 0.28, ly], color="#1a1a1a", lw=2)
    ax.plot([lx - 0.08, lx + 0.28], [ly - 0.28, ly], color="#1a1a1a", lw=2)
    ax.plot([lx + 0.28, lx + 0.28], [ly - 0.32, ly + 0.32], color="#1a1a1a", lw=2.2)
    # IR arrows
    ax.annotate("", xy=(lx + 1.15, ly + 0.55), xytext=(lx + 0.45, ly + 0.18),
                arrowprops=dict(arrowstyle="->", color="#8e1b1b", lw=1.6))
    ax.annotate("", xy=(lx + 1.15, ly + 0.22), xytext=(lx + 0.45, ly - 0.05),
                arrowprops=dict(arrowstyle="->", color="#8e1b1b", lw=1.6))
    label(ax, lx + 1.35, ly + 0.55, "IR 940 nm", fontsize=11, fontweight="bold", color="#8e1b1b")
    label(ax, lx - 0.55, ly + 0.42, "+", fontsize=12, fontweight="bold")
    label(ax, lx + 0.42, ly + 0.42, "−", fontsize=12, fontweight="bold")

    # Wires
    # 5V to 100R
    wire(ax, [(2.35, 5.35), (5.35, 5.35)])
    node(ax, 2.35, 5.35)
    # 100R to LED anode
    wire(ax, [(6.80, 5.35), (7.87, 5.35)])
    # LED cathode down to collector
    wire(ax, [(8.43, 5.35), (8.95, 5.35), (8.95, 4.80), (tx + 0.42, ty + 0.55)])
    # D3 to 1k
    wire(ax, [(2.35, 4.25), (4.55, 4.25)])
    node(ax, 2.35, 4.25)
    # 1k to base
    wire(ax, [(6.00, 4.25), (tx - 0.72, 4.25)])
    # emitter to GND rail
    wire(ax, [(tx + 0.42, ty - 0.55), (tx + 0.42, 3.15), (2.35, 3.15)])
    node(ax, 2.35, 3.15)

    # Title + notes
    label(ax, 8.2, 8.2, "IndianaDell IR blaster", ha="center", fontsize=18, fontweight="bold")
    label(ax, 8.2, 7.8, "Uno  ·  115200  ·  keypad + indiana-ir-send", ha="center", fontsize=11, color="#333")

    # Keypad
    ax.add_patch(FancyBboxPatch((11.2, 2.55), 4.9, 4.85, boxstyle="round,pad=0.05", fc="#fff", ec="#333", lw=1.4))
    label(ax, 13.65, 7.1, "4×4 keypad", ha="center", fontsize=12, fontweight="bold")
    label(ax, 13.65, 6.75, "rows D4–D7   cols D8–D11", ha="center", fontsize=8, color="#444")
    cells = [
        ("1", "2", "3", "A vol+/H1"),
        ("4", "5 OK", "6", "B mute/H2"),
        ("7", "8", "9", "C vol-/H3"),
        ("* DOT", "0", "# on/off", "D home/H4"),
    ]
    for r, row in enumerate(cells):
        for c, txt in enumerate(row):
            x = 11.45 + c * 1.15
            y = 5.85 - r * 0.75
            col = "#1b6b4a" if c == 3 or (r == 3 and c in (0, 2)) else "#2c3e50"
            ax.add_patch(FancyBboxPatch((x, y), 1.05, 0.62, boxstyle="round,pad=0.02", fc=col, ec="none"))
            label(ax, x + 0.52, y + 0.31, txt, ha="center", va="center", color="white", fontsize=7.5)

    notes = (
        "Aim the LED at the TV IR window. NPN: 2N2222 / 2N3904.\n"
        "# tap = power on   # hold = power off   A/C tap = vol   B tap = mute   hold A–D = HDMI\n"
        "Hold 2/8/4/6 = arrows   hold 5 = OK\n"
        "RGB: D12=R D13=G A0=B, one 220Ω on common (CC: common→R→GND; CA: 5V→R→common, set RGB_COMMON_ANODE 1).\n"
        "Flash: indiana-ir-flash     Send: indiana-ir-send poweron|hdmi2|5"
    )
    ax.add_patch(FancyBboxPatch((3.9, 0.2), 12.2, 1.25, boxstyle="round,pad=0.06", fc="#fff", ec="#bbb", lw=1))
    ax.text(4.1, 1.25, notes, va="top", fontsize=10, fontfamily="DejaVu Sans", color="#222", linespacing=1.4)

    fig.tight_layout(pad=0.3)
    fig.savefig(OUT, dpi=140, facecolor=fig.get_facecolor())
    plt.close()
    print(OUT)


if __name__ == "__main__":
    main()
