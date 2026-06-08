import os
from binance.client import Client
from dotenv import load_dotenv
from .logging_config import logger

class BinanceTestnetClient:
    def __init__(self):
        """Initialize the Binance Client using testnet."""
        load_dotenv()
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')

        if not self.api_key or not self.api_secret:
            logger.error("API credentials missing in environment variables.")
            raise ValueError("BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env file.")

        try:
            # Initialize client and explicitly set to testnet
            self.client = Client(self.api_key, self.api_secret, testnet=True)
            
            logger.info("Binance Testnet Client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Binance Client: {str(e)}")
            raise
    
    def get_client(self) -> Client:
        return self.client
