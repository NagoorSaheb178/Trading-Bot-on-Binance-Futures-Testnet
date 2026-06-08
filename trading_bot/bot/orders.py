from binance.exceptions import BinanceAPIException, BinanceRequestException
from .client import BinanceTestnetClient
from .logging_config import logger

class OrderManager:
    def __init__(self):
        self.bot_client = BinanceTestnetClient()
        self.client = self.bot_client.get_client()

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
        """
        Place an order on the Binance Futures Testnet (USDT-M).
        """
        params = {
            'symbol': symbol.upper(),
            'side': side.upper(),
            'type': order_type.upper(),
            'quantity': quantity,
        }

        if price is not None:
            params['price'] = price
            params['timeInForce'] = 'GTC' # Good Till Cancelled is generally required for limit orders

        if stop_price is not None:
            params['stopPrice'] = stop_price

        # Binance expects STOP as order type instead of STOP_LIMIT for futures sometimes,
        # but let's stick to standard parameter mapping.
        if order_type.upper() == 'STOP_LIMIT':
            params['type'] = 'STOP'

        try:
            logger.info(f"Sending order request: {params}")
            
            # Use futures_create_order for USDT-M futures
            response = self.client.futures_create_order(**params)
            
            logger.info(f"Order successful! Response: {response}")
            return {
                "success": True,
                "data": response
            }

        except BinanceAPIException as e:
            error_msg = f"Binance API Exception (Code {e.status_code}): {e.message}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
        except BinanceRequestException as e:
            error_msg = f"Binance Request Exception: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error occurred: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
