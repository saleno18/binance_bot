import sys
from utils import client, logger, validate_symbol, validate_quantity


def place_limit_order(symbol: str, side: str, quantity: float, price: float):
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

    if price <= 0:
        logger.error(f"Invalid price: {price}")
        return

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",  # Good-Til-Canceled
            quantity=quantity,
            price=str(price)
        )
        logger.info(f"Limit order placed: {order}")
        print(f"Limit order placed successfully: {order['orderId']}")
    except Exception as e:
        logger.error(f"Failed to place limit order: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python limit_orders.py SYMBOL BUY/SELL QUANTITY PRICE")
        sys.exit(1)

    _, symbol, side, quantity_str, price_str = sys.argv
    try:
        quantity = float(quantity_str)
        price = float(price_str)
    except ValueError:
        print("Quantity and price must be numbers.")
        sys.exit(1)

    place_limit_order(symbol, side, quantity, price)