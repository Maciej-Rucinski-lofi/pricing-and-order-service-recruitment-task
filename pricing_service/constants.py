"""Domain constants — see README § Domain decisions."""

from decimal import ROUND_HALF_UP, Decimal

MONEY_QUANTIZE = Decimal("0.01")
ROUNDING = ROUND_HALF_UP


def round_money(amount: Decimal) -> Decimal:
    return amount.quantize(MONEY_QUANTIZE, rounding=ROUNDING)
