    "roti": [("Dry tawa, high heat", "45â€“60 s per side, then puff on flame", "Brown speckles, fully puffed")],
    "vegetables": [("Stir-fry, high heat", "4â€“6 min", "Bright colour, still snaps when bent")],
    "cauliflower": [("Roast at 220Â°C", "22â€“28 min", "Charred edges, tender stem")],
    "spinach": [("Wilt in a hot pan", "2â€“3 min", "Collapsed and dark, no raw squeak")],
    "onion": [("SautÃ© for a curry base", "8â€“10 min", "Deep golden â€” pale onion means a raw-tasting gravy")],
}


def _parse_qty(text: str) -> tuple[float, str]:
    """
    Pull a leading quantity off an ingredient line.

    Handles '2', '0.5', '1/2' and mixed numbers like '1 1/2', because recipes
    are written all three ways and a plain float() chokes on the last two.
    Returns (quantity, remainder). Quantity is 0.0 when the line has no
    number at all ('salt to taste'), which callers treat as unscalable.
    """
    s = text.strip()
    m = re.match(r"^(\d+)\s+(\d+)\s*/\s*(\d+)\s*(.*)$", s)
    if m:  # mixed number: 1 1/2
        whole, num, den, rest = m.groups()
        if int(den) != 0:
            return int(whole) + int(num) / int(den), rest.strip()
    m = re.match(r"^(\d+)\s*/\s*(\d+)\s*(.*)$", s)
    if m:  # bare fraction: 1/2
        num, den, rest = m.groups()
        if int(den) != 0:
            return int(num) / int(den), rest.strip()
    m = re.match(r"^(\d+(?:\.\d+)?)\s*(.*)$", s)
    if m:
        return float(m.group(1)), m.group(2).strip()
    return 0.0, s


def _fmt_qty(value: float) -> str:
    """
    Render a scaled quantity the way a recipe would write it.

    Below 10 it snaps to the nearest cook-friendly fraction (â…› through Â¾)
    because '0.583 cup' is not an instruction anyone can follow. Above 10 the
    fractions stop being useful, so it rounds to whole numbers.
    """
    if value <= 0:
        return ""
    if value >= 10:
        return f"{value:.0f}"

    whole = int(value)
    frac = value - whole
    if frac < 0.06:
        return f"{whole}" if whole else "0"

    best = min(NICE_FRACTIONS, key=lambda f: abs(float(f) - frac))
    if abs(float(best) - frac) > 0.07:
        # Not close to anything cooks measure â€” one decimal is more honest.
        return f"{value:.1f}"
    if float(best) == 1.0:
        return f"{whole + 1}"
    return f"{whole} {best.numerator}/{best.denominator}" if whole else f"{best.numerator}/{best.denominator}"

