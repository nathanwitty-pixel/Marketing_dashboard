"""
theme.py
─────────────────────────────────────────────────────────────────
Denri Africa · Marketing Dashboard — colour scheme, extracted from the
dashboard pages so charts, cards and generated HTML can share one source
of truth instead of hard-coding hex strings everywhere.

Usage:
    from theme import SURFACE, TEXT, ACCENT, CHART_SERIES, STATUS, GRADIENTS
    from theme import hex_to_rgba, gradient_css, css_variables

    bg       = SURFACE["card"]                 # "#1e2130"
    ink      = TEXT["muted"]                    # "#94a3b8"
    green    = ACCENT["emerald"]["base"]        # "#34d399"
    grid     = hex_to_rgba(BORDER["default"], 0.55)
    topbar   = gradient_css("green")            # linear-gradient(...)

Dark theme throughout (bg #0f1117). All values are the ones actually in use
on the pages; the ordering of CHART_SERIES matches how the charts assign hues.
"""

# ── Surfaces / backgrounds ────────────────────────────────────
SURFACE = {
    "page":       "#0f1117",   # app background
    "card":       "#1e2130",   # standard card / panel
    "card_alt":   "#171a27",   # darker gradient card
    "raised":     "#252840",   # hovered / raised table row
    "table_head": "#161824",   # table header strip
    "inset":      "#0b0d16",   # deep inset, chart point borders
    "tint_green": "#0d2a1f",   # success callout background tint
    "tint_deep":  "#022c22",   # deepest green tint
}

# ── Borders ───────────────────────────────────────────────────
BORDER = {
    "default": "#2d3148",   # every card / divider
    "hover":   "#3d4a5c",   # border on hover
    "subtle":  "#374151",   # faint separators
}

# ── Text / ink ────────────────────────────────────────────────
TEXT = {
    "heading": "#f8fafc",   # headings, big numbers
    "white":   "#ffffff",
    "body":    "#e2e8f0",   # default body text
    "light":   "#cbd5e1",   # secondary body
    "muted":   "#94a3b8",   # labels, axis ticks
    "dim":     "#64748b",   # captions, hints
    "faint":   "#475569",   # placeholders, empty states
}

# ── Accent hues (named shades used on cards, charts, badges) ───
ACCENT = {
    "emerald": {"base": "#34d399", "deep": "#10b981", "soft": "#6ee7b7", "bright": "#4ade80", "tint": "#d1fae5"},
    "cyan":    {"base": "#22d3ee", "deep": "#06b6d4", "soft": "#67e8f9", "pale": "#a5f3fc", "ice": "#e2f9ff"},
    "amber":   {"base": "#f59e0b", "gold": "#facc15", "warm": "#fbbf24", "deep": "#eab308", "soft": "#fcd34d", "pale": "#fde68a"},
    "red":     {"base": "#f87171", "deep": "#ef4444", "soft": "#fca5a5"},
    "rose":    {"base": "#fb7185", "deep": "#f43f5e", "pink": "#f472b6", "magenta": "#ec4899"},
    "violet":  {"base": "#a78bfa", "deep": "#8b5cf6", "soft": "#c4b5fd", "vivid": "#a855f7", "dark": "#7c3aed", "night": "#2e1065"},
    "indigo":  {"base": "#818cf8", "deep": "#6366f1", "darker": "#4f46e5"},
    "blue":    {"base": "#3b82f6", "sky": "#38bdf8", "soft": "#60a5fa", "pale": "#93c5fd", "ocean": "#0ea5e9"},
    "orange":  {"base": "#fb923c", "deep": "#f97316", "burnt": "#ea580c"},
}

# ── Status / semantic colours ─────────────────────────────────
STATUS = {
    "good":     "#34d399",   # on-track, growth, sold
    "warning":  "#fbbf24",   # attention / below-target
    "bad":      "#f87171",   # miss, dead stock, decline
    "critical": "#ef4444",
    "neutral":  "#94a3b8",   # n/a, flat
}

# ── Chart categorical palette ─────────────────────────────────
# Assign series colours in THIS fixed order (matches the dashboard charts).
CHART_SERIES = [
    "#34d399",  # 1 emerald
    "#22d3ee",  # 2 cyan
    "#a78bfa",  # 3 violet
    "#f59e0b",  # 4 amber
    "#fb923c",  # 5 orange
    "#818cf8",  # 6 indigo
    "#f472b6",  # 7 pink
    "#f87171",  # 8 red
]
CHART_GRID  = "rgba(45,49,72,0.55)"     # gridlines  = BORDER["default"] @ 0.55
CHART_TRACK = "rgba(148,163,184,0.35)"  # 'remaining'/track bars = TEXT["muted"] @ 0.35

# ── Gradients (start → end) for card top-bars & pills ─────────
# Cards use 90deg; the LIVE/FORECAST pills use 135deg.
GRADIENTS = {
    "red":      ("#ef4444", "#f97316"),
    "amber":    ("#f59e0b", "#eab308"),
    "blue":     ("#3b82f6", "#6366f1"),
    "purple":   ("#8b5cf6", "#6366f1"),
    "green":    ("#10b981", "#06b6d4"),
    "rose":     ("#f43f5e", "#ef4444"),
    "cyan":     ("#06b6d4", "#3b82f6"),
    "indigo":   ("#6366f1", "#8b5cf6"),
    "orange":   ("#f97316", "#eab308"),
    "live":     ("#6366f1", "#8b5cf6"),   # "LIVE" pill
    "forecast": ("#0ea5e9", "#6366f1"),   # "FORECAST" pill
}


# ── Product (bag) colours ─────────────────────────────────────
# The 11 colours your bags actually come in (from STOCK_LEVELS / sales data),
# ordered by how much stock & sales they represent (Brown highest → Yellow
# lowest). The sheet stores the NAME only; these hex values are display swatches
# chosen to be recognisable and to read on the dark theme.
PRODUCT_COLOURS = {
    "Brown":  "#8b5e3c",
    "Black":  "#111827",
    "Red":    "#ef4444",
    "Grey":   "#9ca3af",
    "Beige":  "#e7d8bf",
    "Green":  "#22c55e",
    "Blue":   "#3b82f6",
    "Pink":   "#f472b6",
    "Purple": "#a855f7",
    "Orange": "#f97316",
    "Yellow": "#facc15",
}

# Dark swatches need a light hairline border to be visible on the #0f1117 bg.
PRODUCT_COLOURS_NEED_BORDER = {"Black", "Brown"}


def product_swatch(name, default="#64748b"):
    """Return the display hex for a product colour NAME (case-insensitive)."""
    if not name:
        return default
    key = str(name).strip().lower()
    for cname, hexv in PRODUCT_COLOURS.items():
        if cname.lower() == key:
            return hexv
    return default


# ── Helpers ───────────────────────────────────────────────────
def hex_to_rgba(hex_color, alpha=1.0):
    """'#1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def gradient_css(name, angle="90deg"):
    """gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'."""
    start, end = GRADIENTS[name]
    return f"linear-gradient({angle}, {start}, {end})"


def css_variables():
    """Emit the whole palette as CSS custom properties for a :root {} block."""
    lines = []
    for k, v in SURFACE.items():  lines.append(f"  --surface-{k.replace('_', '-')}: {v};")
    for k, v in BORDER.items():   lines.append(f"  --border-{k}: {v};")
    for k, v in TEXT.items():     lines.append(f"  --text-{k}: {v};")
    for hue, shades in ACCENT.items():
        for shade, v in shades.items():
            suffix = "" if shade == "base" else f"-{shade}"
            lines.append(f"  --{hue}{suffix}: {v};")
    for k, v in STATUS.items():   lines.append(f"  --status-{k}: {v};")
    return ":root {\n" + "\n".join(lines) + "\n}"


# Flat name→hex map of every colour, for quick lookups / validation.
ALL = {}
ALL.update({f"surface.{k}": v for k, v in SURFACE.items()})
ALL.update({f"border.{k}": v for k, v in BORDER.items()})
ALL.update({f"text.{k}": v for k, v in TEXT.items()})
ALL.update({f"{hue}.{sh}": v for hue, shades in ACCENT.items() for sh, v in shades.items()})
ALL.update({f"status.{k}": v for k, v in STATUS.items()})
ALL.update({f"product.{k}": v for k, v in PRODUCT_COLOURS.items()})

__all__ = ["SURFACE", "BORDER", "TEXT", "ACCENT", "STATUS",
           "CHART_SERIES", "CHART_GRID", "CHART_TRACK", "GRADIENTS", "ALL",
           "PRODUCT_COLOURS", "PRODUCT_COLOURS_NEED_BORDER", "product_swatch",
           "hex_to_rgba", "gradient_css", "css_variables"]


if __name__ == "__main__":
    print(f"Denri dashboard theme — {len(ALL)} named colours\n")
    print("Chart series order:", " ".join(CHART_SERIES))
    print("\nProduct (bag) colours:")
    for name, hexv in PRODUCT_COLOURS.items():
        print(f"  {name:<7} {hexv}" + ("  (dark — add border)" if name in PRODUCT_COLOURS_NEED_BORDER else ""))
    print("\nExample gradient (green):", gradient_css("green"))
    print("Example rgba (card @ 0.5):", hex_to_rgba(SURFACE["card"], 0.5))
    print("\n:root CSS variables:\n")
    print(css_variables())
