import logging
import uvicorn.logging

FORMAT = "%(levelprefix)s %(message)s"
_formatter = uvicorn.logging.DefaultFormatter(FORMAT)


def getMainLogger():
    logger = logging.getLogger("main_logger")
    ch = logging.StreamHandler()
    ch.setFormatter(_formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)

    return logger
