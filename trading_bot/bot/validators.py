import re
from typing import Optional

def validate_symbol(symbol: str) -> str:
    """Validate symbol format (e.g., BTCUSDT)."""
    symbol = symbol.upper()
    if not re.match(r"^[A-Z0-9]{2,15}$", symbol):
        raise ValueError(f"Invalid symbol format: {symbol}. Must be alphanumeric.")
    return symbol

def validate_quantity(quantity: float) -> float:
    """Validate that quantity is a positive number."""
    if quantity <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got: {quantity}")
    return quantity

def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    """Validate price depending on the order type."""
    if order_type.upper() in ["LIMIT", "STOP_LIMIT"] and price is None:
        raise ValueError(f"Price is required for {order_type} orders.")
    if price is not None and price <= 0:
        raise ValueError(f"Price must be greater than 0. Got: {price}")
    return price

def validate_stop_price(stop_price: Optional[float], order_type: str) -> Optional[float]:
    """Validate stop price for STOP orders."""
    if order_type.upper() in ["STOP_LIMIT"] and stop_price is None:
        raise ValueError(f"Stop Price is required for {order_type} orders.")
    if stop_price is not None and stop_price <= 0:
        raise ValueError(f"Stop Price must be greater than 0. Got: {stop_price}")
    return stop_price
