import sys
from utils import client, logger, validate_symbol, validate_quantity

def place_market_order(symbol: str, side: str, quantity: float):
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        logger.error(f"Invalid side: {side}. Must be BUY or SELL.")
        return

    if not validate_symbol(symbol):
        logger.error(f"Invalid symbol: {symbol}")
        return

    if not validate_quantity(symbol, quantity):
        logger.error(f"Invalid quantity: {quantity}")
        return

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        logger.info(f"Market order placed: {order}")
        print(f"Market order placed successfully: {order['orderId']}")
    except Exception as e:
        logger.error(f"Failed to place market order: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python market_orders.py SYMBOL BUY/SELL QUANTITY")
        sys.exit(1)

    _, symbol, side, quantity_str = sys.argv
    try:
        quantity = float(quantity_str)
    except ValueError:
        print("Quantity must be a number.")
        sys.exit(1)

    place_market_order(symbol, side, quantity)