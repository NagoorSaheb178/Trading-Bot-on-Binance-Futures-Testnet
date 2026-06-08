import logging
import os

def setup_logging():
    """Configure logging for the application."""
    log_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger('trading_bot')
    logger.setLevel(logging.DEBUG) # Catch everything

    # Ensure no duplicate handlers if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # File Handler
    file_handler = logging.FileHandler('trading_bot.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_formatter)

    # Add handlers
    logger.addHandler(file_handler)

    # Disable spammy library logs
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('binance.client').setLevel(logging.INFO)

    return logger

logger = setup_logging()
