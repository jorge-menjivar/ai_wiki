from bs4 import BeautifulSoup
from utils import parsing


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
    title = parsing.removeItalics(title)
    title = parsing.removeQuotes(title)
    title = parsing.removeAsterisks(title)
    title = parsing.removeUnderscores(title)

    tag = BeautifulSoup(f"""<div class="title">{title}</div>""", 'html.parser')

    soup.body.insert(0, tag)
