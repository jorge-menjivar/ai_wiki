def getLevelString(level: int):
    """
    getLevelString(level: int)

    Description:
        This function takes in a level (int) and returns a string formatted as
        "l[level]"

    Parameters:
        level (int): The level to be converted to a string

    Returns:
        level_string (str): A string formatted as "l[level]"

    Example:
        >>> getLevelString(2)
        'l2'
    """

    level_string: str = f"l{level}"
    return level_string


def removeItalics(text: str | None):
    """
    removeItalics(text)

    Remove all italicized text from a string.

    Parameters
    ----------
    text : str
        The string to remove italicized text from.

    Returns
    -------
    str
        The string without italicized text.
    """

    if text is not None:
        text = text.replace("&lt;i&gt;", "")
        text = text.replace("&lt;/i&gt;", "")
        text = text.replace("<i>", "")
        text = text.replace("</i>", "")
        return text
    return ""


def removeQuotes(text: str | None):
    """
    removeQuotes(text: str | None)

    Parameters
    ----------
    text : str | None
        The string that is to be processed.

    Returns
    -------
    str
        The string with any quotes removed. If no text is provided, an empty
        string will be returned.

    Description
    -----------
    Removes all quotes from a given string. If no string is provided, an empty
    string will be returned.
    """

    if text is not None:
        text = text.replace("\"", "")
        return text
    return ""


def removeAsterisks(text: str | None):
    """
    removeAsterisks(text: str | None)

    Remove asterisks from a given string.

    Parameters
    ----------
    text : str | None
        The string to remove asterisks from.

    Returns
    -------
    str
        The string without asterisks. If the input is None, an empty string is
        returned.

    """

    if text is not None:
        text = text.replace("*", "")
        return text
    return ""


def removeUnderscores(text: str | None):
    """
    Removes underscores from a string.

    Parameters
    ----------
    text : str | None
        The string to process.

    Returns
    -------
    str
        The processed string with underscores removed.
    """

    if text is not None:
        text = text.replace('_', ' ')
        return text
    return ""
