from database.content import aAddContent
from psycopg import AsyncConnection
from nlp.openai.gpt3_davinci import aInfer
from readuce.utils import removeItalics, removeUnderscores


async def aOverview(
    aconn: AsyncConnection,
    level: int,
    title: str,
):
    pretty_title = removeUnderscores(title)
    pretty_title = removeItalics(title)
    prompt = overviewPromptDavinci(level, pretty_title)

    if prompt is None:
        return

    content, model = await aInfer(prompt)

    row = await aAddContent(aconn, level, title, "readuce", content, model)

    return row


async def aSubSection(aconn: AsyncConnection, level: int, title: str, id: str):

    pretty_title = removeUnderscores(title)
    pretty_title = removeItalics(title)
    sub_section: str = removeUnderscores(id)
    prompt = sectionPromptDavinci(level, pretty_title, sub_section)

    if prompt is None:
        return

    content, model = await aInfer(prompt)

    row = await aAddContent(
        aconn,
        level,
        title,
        section=id,
        content=content,
        model=model,
    )

    return row


def overviewPromptDavinci(level: int, title: str | None):
    if title is None:
        return

    text = ''

    if level == 1:
        text = f'Summarize "{title}" like I am 2 years old'

    elif level == 2:
        text = f'Summarize "{title}" like I am 5 years old'

    elif level == 3:
        text = f'Summarize "{title}" like I am a teenager'

    elif level == 4:
        text = f'''
        Summarize "{title}" like I am almost knowledgeable in this field
        '''

    elif level == 5:
        text = f'''
        Summarize "{title}" like I am knowledgeable in this field
        '''

    elif level == 6:
        text = f'''
        Summarize "{title}" like I am almost an expert in this field
        '''

    elif level == 7:
        text = f'''
        Summarize "{title}" like I am an expert in this field
        '''

    return text


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
