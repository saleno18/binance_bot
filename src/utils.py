import os
from dotenv import load_dotenv
from binance.client import Client
from loguru import logger

# Load environment variables from .env file if present
load_dotenv()

# Fetch API keys from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

if not API_KEY or not API_SECRET:
    logger.error("API_KEY and API_SECRET must be set as environment variables or in a .env file.")
    raise Exception("Missing Binance API credentials.")

# Initialize Binance Futures client
client = Client(API_KEY, API_SECRET)

# Configure logger to write to bot.log with timestamps and error tracebacks
logger.add(
    "bot.log",
    rotation="10 MB",  # rotate after 10 MB
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
    enqueue=True  # thread-safe logging
)

def validate_symbol(symbol: str) -> bool:
    """
    Validate if the symbol exists in Binance Futures exchange info.
    """
    try:
        info = client.futures_exchange_info()
        symbols = [s['symbol'] for s in info['symbols']]
        if symbol in symbols:
            return True
        else:
            logger.error(f"Symbol '{symbol}' not found in Binance Futures symbols.")
            return False
    except Exception as e:
        logger.error(f"Error fetching exchange info: {e}")
        return False

def validate_quantity(symbol: str, quantity: float) -> bool:
    """
    Basic validation for quantity.
    You can extend this to check minQty, stepSize from exchange info.
    """
    if quantity <= 0:
        logger.error(f"Quantity must be positive. Got: {quantity}")
        return False
    # TODO: Add symbol-specific min/max quantity validation if needed
    return True