import logging


def configure_root_logger(log_level: int, log_file: str = None) -> None:
    """
    Configures the root logger, applying the configuration to all loggers.

    :param log_level: Logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
    :param log_file: Optional log file to write logs to.
    """
    # Create root logger
    logger = logging.getLogger()
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
