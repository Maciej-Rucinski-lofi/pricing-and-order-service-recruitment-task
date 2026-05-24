class PricingError(Exception):
    """Base error for pricing domain failures."""


class UnknownProductError(PricingError):
    def __init__(self, product_id: str) -> None:
        super().__init__(f"Unknown product: {product_id}")
        self.product_id = product_id


class InvalidQuantityError(PricingError):
    def __init__(self, quantity: int) -> None:
        super().__init__(f"Invalid quantity: {quantity}")
        self.quantity = quantity


class UnsupportedCustomerTypeError(PricingError):
    def __init__(self, customer_type: str) -> None:
        super().__init__(f"Unsupported customer type: {customer_type}")
        self.customer_type = customer_type
