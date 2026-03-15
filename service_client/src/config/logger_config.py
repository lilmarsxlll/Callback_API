import logging


def setup_logging():
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
