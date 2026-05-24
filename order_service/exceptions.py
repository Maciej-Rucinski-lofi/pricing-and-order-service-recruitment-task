class OrderError(Exception):
    """Base error for order domain failures."""


class PricingUnavailableError(OrderError):
    """Pricing backend failed or is unreachable (infrastructure)."""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause
