from bs4 import BeautifulSoup


async def aAddAIOverview(soup: BeautifulSoup):
    """Adds an AI Overview to the HTML text.

    Parameters
    ----------
    soup : BeautifulSoup
        BeautifulSoup object representing the HTML page to add the AIOverview
        to.

    Returns
    -------
    None
        This function does not return anything.

    Raises
    ------
    TypeError
        If the parameter `soup` is not of type `BeautifulSoup`.

    Examples
    --------
    >>> import requests
    >>> from bs4 import BeautifulSoup
    >>>
    >>> url = "http://example.com"
    >>> response = requests.get(url)
    >>>
    >>> soup = BeautifulSoup(response.text, 'html.parser')
    >>> aAddAIOverview(soup)
    """

    if soup.body is not None:

        first_p = soup.body.find('p')

        tag = BeautifulSoup(
            f'''<h2>Overview</h2>
                        <div class="ai_overview"></div>
                    <h2>Article</h2> {first_p}''', 'html.parser')

        if first_p is not None:
            first_p.replace_with(tag)
