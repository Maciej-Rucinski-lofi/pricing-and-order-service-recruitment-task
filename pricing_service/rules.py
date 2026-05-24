import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from pricing_service.exceptions import UnsupportedCustomerTypeError

DEFAULT_RULES_PATH = Path(__file__).resolve().parent.parent / "config" / "pricing_rules.json"


@dataclass(frozen=True)
class PricingRules:
    customer_discounts: dict[str, Decimal]
    quantity_discounts: list[tuple[int, Decimal]]
    max_total_discount_percent: Decimal


def load_rules(path: Path | None = None) -> PricingRules:
    """Load discount rules from JSON config."""
    config_path = path or DEFAULT_RULES_PATH
    with config_path.open(encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, dict):
        raise ValueError(f"Expected a JSON object in {config_path}")

    customer_discounts = {
        name: Decimal(str(percent))
        for name, percent in raw["customer_discounts"].items()
    }
    quantity_discounts = [
        (entry["min_quantity"], Decimal(str(entry["percent"])))
        for entry in raw["quantity_discounts"]
    ]
    return PricingRules(
        customer_discounts=customer_discounts,
        quantity_discounts=quantity_discounts,
        max_total_discount_percent=Decimal(str(raw["max_total_discount_percent"])),
    )


def calculate_discount_percent(
    rules: PricingRules,
    quantity: int,
    customer_type: str,
) -> Decimal:
    """Compute effective discount % (additive, capped)."""
    if customer_type not in rules.customer_discounts:
        raise UnsupportedCustomerTypeError(customer_type)

    customer_discount = rules.customer_discounts[customer_type]
    quantity_discount = _quantity_discount_percent(rules, quantity)
    combined = customer_discount + quantity_discount
    return min(combined, rules.max_total_discount_percent)


def _quantity_discount_percent(rules: PricingRules, quantity: int) -> Decimal:
    applicable = Decimal("0")
    for min_quantity, percent in rules.quantity_discounts:
        if quantity >= min_quantity and percent > applicable:
            applicable = percent
    return applicable
