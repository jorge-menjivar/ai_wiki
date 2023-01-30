from bs4 import BeautifulSoup


async def aAddAIOverview(soup: BeautifulSoup):

    if soup.body is not None:

        first_p = soup.body.find('p')

        tag = BeautifulSoup(
            f'''<h2>Overview</h2>
                        <div class="ai_overview"></div>
                    <h2>Article</h2> {first_p}''', 'html.parser')

        if first_p is not None:
            first_p.replace_with(tag)
