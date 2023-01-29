import logging
import uvicorn.logging

FORMAT = "%(levelprefix)s %(message)s"
_formatter = uvicorn.logging.DefaultFormatter(FORMAT)
_logger = None


def getMainLogger():
    global _logger
    if _logger is None:
        _logger = logging.getLogger("main_logger")
        ch = logging.StreamHandler()
        ch.setFormatter(_formatter)
        _logger.addHandler(ch)
        _logger.setLevel(logging.DEBUG)

    return _logger
