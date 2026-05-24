from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

import yaml

DEFAULT_RULES_PATH = Path(__file__).resolve().parent.parent / "config" / "pricing_rules.yaml"


@dataclass(frozen=True)
class PricingRules:
    customer_discounts: dict[str, Decimal]
    quantity_discounts: list[tuple[int, Decimal]]
    max_total_discount_percent: Decimal


def load_rules(path: Path | None = None) -> PricingRules:
    """Load discount rules from YAML config."""
    config_path = path or DEFAULT_RULES_PATH
    with config_path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f)

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
    """Compute effective discount %. Full logic completed in Phase 3."""
    raise NotImplementedError("Discount calculation is implemented in Phase 3.")
