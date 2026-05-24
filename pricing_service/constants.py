"""Domain constants — see README § Domain decisions."""

from decimal import ROUND_HALF_UP, Decimal

MONEY_QUANTIZE = Decimal("0.01")
ROUNDING = ROUND_HALF_UP
