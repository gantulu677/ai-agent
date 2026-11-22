"""Standard-library logging setup."""
import logging


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger("agent_runtime")
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        logger.addHandler(handler)
    return logger
