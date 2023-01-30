from bs4 import BeautifulSoup


async def aAddAISubSections(soup: BeautifulSoup):
    """
    Parameters
    ----------
    soup : BeautifulSoup
        An object containing a parsed document tree.

    Returns
    -------
    None

    Raises
    ------
    None

    See Also
    --------
    BeautifulSoup

    Notes
    -----
    This function adds a <div> tag with the class ai_sub_section and the id
    ai_[id] to each <h3> tag in the document tree.
    """

    if soup.body is not None:

        ss_tags = soup.body.find_all('h3')

        for ss_tag in ss_tags:

            id = ss_tag['id']

            tag = BeautifulSoup(
                f"""{ss_tag}\
                <div class='ai_sub_section' id='ai_{id}'>
                </div>""", 'html.parser')

            ss_tag.replace_with(tag)
