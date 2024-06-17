import logging
import os


def configure_logger(name: str, log_level: int, log_file: str = None) -> logging.Logger:
    """
    Configures and returns a logger.

    :param name: Name of the logger.
    :param log_level: Logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
    :param log_file: Optional log file to write logs to.
    :return: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    # Log format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler (if log_file is specified)
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
    logger = configure_logger(
        'transaction_extractor', log_level='DEBUG', log_file=os.getenv('LOG_FILE', 'app.log'))
