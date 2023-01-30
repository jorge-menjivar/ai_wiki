import logging
import uvicorn.logging

FORMAT = "%(levelprefix)s %(message)s"
_formatter = uvicorn.logging.DefaultFormatter(FORMAT)
_logger = None


def getMainLogger():
    """
    Summary
    -------
    Retrieves the main logger for logging messages.

    Parameters
    ----------
    None

    Returns
    -------
    logger : logger
        The main logger used for logging messages.

    Raises
    ------
    None

    Example
    -------
    logger = getMainLogger()
    logger.info("A message to be logged")

    """

    global _logger
    if _logger is None:
        _logger = logging.getLogger("main_logger")
        ch = logging.StreamHandler()
        ch.setFormatter(_formatter)
        _logger.addHandler(ch)
        _logger.setLevel(logging.DEBUG)

    return _logger
