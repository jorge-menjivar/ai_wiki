from bs4 import BeautifulSoup


async def aAddAISubSections(soup: BeautifulSoup):
    if soup.body is not None:

        ss_tags = soup.body.find_all('h3')

        for ss_tag in ss_tags:

            id = ss_tag['id']
            print(id)

            tag = BeautifulSoup(
                f"""{ss_tag}\
                <div class='ai_sub_section' id='ai_{id}'>
                </div>""", 'html.parser')

            ss_tag.replace_with(tag)


def addAISubSections(soup: BeautifulSoup):

    if soup.body is not None:

        ss_tags = soup.body.find_all('h3')

        for ss_tag in ss_tags:

            id = ss_tag['id']
            print(id)

            tag = BeautifulSoup(
                f"""{ss_tag}\
                <div class='ai_sub_section'>
                </div>""", 'html.parser')

            ss_tag.replace_with(tag)
