from bs4 import BeautifulSoup


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


def fixMath(soup):
    """
    fixMath(soup)

    Fixes math equations in the inputted soup object.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        A BeautifulSoup object created using the bs4 module.

    Returns
    -------
    bs4.BeautifulSoup
        A modified version of the inputted soup object with math equations
        fixed.

    """

    spans = soup.body.find_all(attrs={'class': "mwe-math-mathml-inline"})

    for s in spans:
        s['style'] = ''

    scripts = BeautifulSoup(
        '''
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6">
    </script> <script id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>''', 'html.parser')

    soup.body.insert(0, scripts)

    return soup


def fixMathFallbackImage(soup):
    """
    fixMathFallbackImage(soup)

    Parameters
    ----------
    soup : bs4.BeautifulSoup object
        a BeautifulSoup object containing the HTML of the page

    Returns
    -------
    soup : bs4.BeautifulSoup object
        a BeautifulSoup object with all math fallback images having their
        style attribute removed
    """

    images = soup.body.find_all(
        attrs={'class': "mwe-math-fallback-image-inline"})

    for i in images:
        del i['style']

    return soup


def fixSideBarListTitle(soup):
    """
    fixSideBarListTitle(soup)

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        The soup object to parse

    Returns
    -------
    soup : bs4.BeautifulSoup
        The updated soup object

    fixSideBarListItems(soup)

    Parameters
    ----------
    ...
    -------
    soup : bs4.BeautifulSoup
        The updated soup object
    """

    spans = soup.body.find_all(attrs={'class': "sidebar-list-title"})

    for s in spans:
        del s['style']

    return soup


def includeTitle(soup):
    """
    Parameters
    ----------
    soup: BeautifulSoup object
        The parsed HTML page to include the title in.

    Returns
    -------
    soup: BeautifulSoup object
        The modified BeautifulSoup object with the title included.
    """

    title = soup.title.string
    title = removeItalics(title)
    title = removeQuotes(title)
    title = removeAsterisks(title)
    title = removeUnderscores(title)

    tag = BeautifulSoup(f"""<div class="title">{title}</div>""", 'html.parser')

    soup.body.insert(0, tag)
