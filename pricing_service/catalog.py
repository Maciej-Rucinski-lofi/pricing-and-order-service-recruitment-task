import json
from pathlib import Path

from pricing_service.models import Product

DEFAULT_PRODUCTS_PATH = Path(__file__).resolve().parent.parent / "config" / "products.json"


def load_products(path: Path | None = None) -> dict[str, Product]:
    """Load product catalog from JSON config."""
    config_path = path or DEFAULT_PRODUCTS_PATH
    with config_path.open(encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, list):
        raise ValueError(f"Expected a JSON array in {config_path}")
    products = _parse_products(raw)
    if not products:
        raise ValueError(f"Product catalog is empty: {config_path}")
    return products


def get_product(products: dict[str, Product], product_id: str) -> Product | None:
    return products.get(product_id)


def _parse_products(raw: list[dict]) -> dict[str, Product]:
    from decimal import Decimal

    products: dict[str, Product] = {}
    for item in raw:
        product_id = item["id"]
        products[product_id] = Product(
            id=product_id,
            name=item["name"],
            unit_price=Decimal(str(item["price"])),
        )
    return products
