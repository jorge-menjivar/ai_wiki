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
