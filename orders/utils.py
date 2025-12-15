from decimal import Decimal

def calculate_quote(base_price_eur, design_type: str, size: str, brief: str) -> Decimal:
    """
    Server-side quote calculation (cannot be manipulated by user).
    Demonstrates compound logic (ifs, loops) for LO1.9/1.10.
    """
    price = Decimal(base_price_eur)

    design_type = (design_type or "").lower()
    size = (size or "").lower()
    brief = (brief or "").lower()

    # Type multipliers
    type_multipliers = {
        "logo": Decimal("1.20"),
        "poster": Decimal("1.10"),
        "icon": Decimal("1.00"),
        "branding": Decimal("1.35"),
    }
    for key, mult in type_multipliers.items():
        if key in design_type:
            price *= mult
            break

    # Size add-on
    if "a0" in size or "a1" in size or "large" in size:
        price += Decimal("30.00")
    elif "a3" in size or "medium" in size:
        price += Decimal("15.00")

    # Complexity keywords
    complexity_keywords = ["illustration", "detailed", "hand-drawn", "complex", "many elements"]
    complexity_hits = sum(1 for kw in complexity_keywords if kw in brief)

    if complexity_hits >= 2:
        price += Decimal("40.00")
    elif complexity_hits == 1:
        price += Decimal("20.00")

    # Round to 2dp
    return price.quantize(Decimal("0.01"))
