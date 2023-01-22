from database import ai_content
from psycopg import AsyncConnection, Connection
from nlp.openai import gpt3_davinci
from readuce.utils import removeUnderscores


def overview(
    conn: Connection,
    level: int,
    title: str,
):
    pretty_title = removeUnderscores(title)
    prompt = overviewPromptDavinci(level, pretty_title)

    if prompt is None:
        return

    content, model = gpt3_davinci.infer(prompt)

    ai_content.add(
        conn,
        level,
        title,
        "readuce",
        content,
        model
    )


async def aOverview(
    aconn: AsyncConnection,
    level: int,
    title: str,
):
    pretty_title = removeUnderscores(title)
    prompt = overviewPromptDavinci(level, pretty_title)

    if prompt is None:
        return

    content, model = await gpt3_davinci.aInfer(prompt)

    await ai_content.aAdd(
        aconn,
        level,
        title,
        "readuce",
        content,
        model
    )


def subSection(
    conn: Connection,
    level: int,
    title: str,
    sub_section: str,
    id: str
):

    pretty_title = removeUnderscores(title)
    prompt = sectionPromptDavinci(level, pretty_title, sub_section)

    if prompt is None:
        return

    content, model = gpt3_davinci.infer(prompt)

    ai_content.add(
        conn,
        level,
        title,
        section=id,
        content=content,
        model=model
    )


async def aSubSection(
    aconn: AsyncConnection,
    level: int,
    title: str,
    sub_section: str,
    id: str
):

    pretty_title = removeUnderscores(title)
    prompt = sectionPromptDavinci(level, pretty_title, sub_section)

    if prompt is None:
        return

    content, model = await gpt3_davinci.aInfer(prompt)

    await ai_content.aAdd(
        aconn,
        level,
        title,
        section=id,
        content=content,
        model=model
    )


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
