# src/pizza.py
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from decimal import Decimal, ROUND_HALF_UP, getcontext
import yaml

# High precision for intermediate steps
getcontext().prec = 28
TWO = Decimal("0.01")

def money(x) -> Decimal:
    """Round HALF_UP to 2 decimals for currency."""
    return (Decimal(str(x))).quantize(TWO, rounding=ROUND_HALF_UP)

@dataclass
class Pizza:
    size: str
    toppings: List[str]

class Menu:
    def __init__(self, data: Dict[str, Any]):
        self.shop = data.get("shop", {})
        self.sizes = data.get("sizes", {})
        self.toppings = data.get("toppings", {})
        self.promos = data.get("promos", {})

    @classmethod
    def from_yaml(cls, path: str) -> "Menu":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return cls(data)

    # Internal: Decimal pricing for correctness
    def _price_pizza_dec(self, p: Pizza) -> Decimal:
        if p.size not in self.sizes:
            raise ValueError("Unknown size")
        base = Decimal(str(self.sizes[p.size]))
        tops = sum(Decimal(str(self.toppings[t])) for t in p.toppings if t in self.toppings)
        return money(base + tops)

    # Public: float for tests
    def price_pizza(self, p: Pizza) -> float:
        return float(self._price_pizza_dec(p))

# Public API: return **float** for tests
def apply_promos(menu: Menu, pizzas: List[Pizza], promo_code: Optional[str]) -> float:
    if not promo_code:
        return 0.0
    promo = menu.promos.get(promo_code)
    if not promo:
        return 0.0

    ptype = promo.get("type")
    percent = Decimal(str(promo.get("percent", 0))) / Decimal("100")

    if ptype == "two_large_pct_off":
        large_prices = [menu._price_pizza_dec(p) for p in pizzas if p.size == "large"]
        if len(large_prices) >= 2:
            raw = sum(large_prices, Decimal("0.00")) * percent
            return float(money(raw))  # float for the test
        return 0.0

    if ptype == "percent_off_order":
        raw = sum((menu._price_pizza_dec(p) for p in pizzas), Decimal("0.00")) * percent
        return float(money(raw))      # float for the test

    return 0.0

def total_with_tax(menu: Menu, pizzas: List[Pizza], promo_code: Optional[str] = None) -> Dict[str, float]:
    subtotal_dec = sum((menu._price_pizza_dec(p) for p in pizzas), Decimal("0.00"))

    # Rounded discount for display (float from apply_promos)
    rounded_discount_float = apply_promos(menu, pizzas, promo_code)
    rounded_discount_dec = money(rounded_discount_float)

    # Recompute raw discount (unrounded) for correct tax math
    raw_discount = Decimal("0.00")
    if promo_code:
        promo = menu.promos.get(promo_code)
        if promo:
            ptype = promo.get("type")
            percent = Decimal(str(promo.get("percent", 0))) / Decimal("100")
            if ptype == "two_large_pct_off":
                large_prices = [menu._price_pizza_dec(p) for p in pizzas if p.size == "large"]
                if len(large_prices) >= 2:
                    raw_discount = sum(large_prices, Decimal("0.00")) * percent
            elif ptype == "percent_off_order":
                raw_discount = subtotal_dec * percent

    tax_rate = Decimal(str(menu.shop.get("tax_rate", 0.0)))
    total_dec = money((subtotal_dec - raw_discount) * (Decimal("1.0") + tax_rate))

    return {
        "subtotal": float(money(subtotal_dec)),
        "discount": float(rounded_discount_dec),  # e.g., 3.13 / 2.03
        "tax_rate": float(tax_rate),
        "total": float(total_dec),                # e.g., 19.23
    }
