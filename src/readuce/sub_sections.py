from bs4 import BeautifulSoup
from src.readuce.utils import removeUnderscores
from src.data import db
from src.openai.nlp import gpt3_davinci


def addAISubSections(
    conn,
    soup: BeautifulSoup,
    level: int,
    title: str,
):
    if soup.body is not None:

        ss_tags = soup.body.find_all('h3')

        for ss_tag in ss_tags:

            print(ss_tag)
            id = ss_tag['id']

            row = db.getContentRow(conn, level, title, section=id)

            content: str = ""
            if row is None:
                pretty_title = ""
                if soup.title is None or soup.title.string is None:
                    return soup

                pretty_title = soup.title.string
                sub_section: str = removeUnderscores(id)

                prompt = sectionPromptDavinci(level, pretty_title, sub_section)

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
                f"{ss_tag}<div class='ai_sub_section'><p>{content}</p></div>",
                'html.parser'
            )

            ss_tag.replace_with(tag)


def sectionPromptDavinci(level: int, title: str, section: str):

    text = ''

    if level == 1:
        text = f'''
        I know "{title}". \
        Tell me specifically its {section} like I am 2 years old
        '''

    elif level == 2:
        text = f'''
        I know "{title}". \
        Tell me specifically its {section} like I am 5 years old
        '''

    elif level == 3:
        text = f'''
        I know "{title}". \
        Tell me specifically its {section} like I am a teenager
        '''

    elif level == 4:
        text = f'''
        I know "{title}". \
        Tell me specifically its {section} like I am almost \
        knowledgeable in this field
        '''

    elif level == 5:
        text = f'''
        I know "{title}". \
        Tell me specifically its {section} like I am knowledgeable \
        in this field
        '''

    elif level == 6:
        text = f'''
        I know "{title}". \
        Tell me specifically its {section} like I am almost an \
        expert in this field
        '''

    elif level == 7:
        text = f'''
        I know "{title}". \
        Tell me specifically its {section} like I am an expert in \
        this field
        '''

    return text
