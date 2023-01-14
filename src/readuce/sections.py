from bs4 import BeautifulSoup
from src.data import db
from src.openai.nlp import gpt3_davinci


def addAISections(
    conn,
    soup: BeautifulSoup,
    level: int,
    title: str,
):
    if soup.body is not None:

        section_tags = soup.body.find_all('h2')

        for s_tag in section_tags:

            print(s_tag)
            id = s_tag['id']

            if id not in ["External_links", "References", "See_also",
                          "Bibliography"]:
                row = db.getContentRow(conn, level, title, section=id)

                content: str = ''
                if row is None:
                    pretty_title = ""
                    if soup.title is None or soup.title.string is None:
                        return soup

                    pretty_title = soup.title.string
                    section: str = s_tag.string

                    prompt = sectionPromptDavinci(level, pretty_title, section)

                    if prompt is None:
                        return

                    content, model = gpt3_davinci.infer(prompt)
                    db.addContent(
                        conn,
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
