from bs4 import BeautifulSoup
from database.ai_content import aAdd, aGet
from nlp.openai import gpt3_davinci
from psycopg import AsyncConnection

from readuce.utils import removeUnderscores


async def addAISections(
    aconn: AsyncConnection,
    soup: BeautifulSoup,
    level: int,
    title: str,
):

    pretty_title = removeUnderscores(title)
    if soup.body is not None:

        section_tags = soup.body.find_all('h2')

        for s_tag in section_tags:

            print(s_tag)
            id = s_tag['id']

            if id not in ["External_links", "References", "See_also",
                          "Bibliography"]:
                row = await aGet(aconn, level, title, section=id)

                content: str = ''
                if row is None:
                    section: str = s_tag.string

                    prompt = sectionPromptDavinci(level, pretty_title, section)

                    if prompt is None:
                        return

                    content, model = await gpt3_davinci.aInfer(prompt)
                    await aAdd(
                        aconn,
                        level,
                        title,
                        section=id,
                        content=content,
                        model=model
                    )
                else:
                    content = row.content

                tag = BeautifulSoup(
                    f"{s_tag}<div class='ai_section'><p>{content}</p></div>",
                    'html.parser'
                )

                s_tag.replace_with(tag)

            else:
                print('Skipping section')


def sectionPromptDavinci(level: int, title: str, section: str):

    text = ''

    if level == 1:
        text = f'''\
        Tell me more about the {section} of "{title}" like I am 2 years old
        '''

    elif level == 2:
        text = f'''\
        Tell me more about the {section} of "{title}" like I am 5 years old
        '''

    elif level == 3:
        text = f'''\
        Tell me more about the {section} of "{title}" like I am a teenager
        '''

    elif level == 4:
        text = f'''
        Tell me more about the {section} of "{title}" like I am almost \
        knowledgeable in this field
        '''

    elif level == 5:
        text = f'''
        Tell me more about the {section} of "{title}" like I am knowledgeable \
        in this field
        '''

    elif level == 6:
        text = f'''
        Tell me more about the {section} of "{title}" like I am almost an \
        expert in this field
        '''

    elif level == 7:
        text = f'''
        Tell me more about the {section} of "{title}" like I am an expert in \
        this field
        '''

    return text
