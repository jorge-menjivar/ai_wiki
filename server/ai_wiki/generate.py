from database.content import aAddContent
from psycopg import AsyncConnection
from nlp.openai.gpt3_davinci import aInfer
from utils.parsing import removeItalics, removeUnderscores


async def aOverview(
    aconn: AsyncConnection,
    level: int,
    title: str,
):
    """
    Asynchronously generate a summary of an article given its title.

    Parameters
    ----------
    aconn : AsyncConnection
        The async connection to the database.
    level : int
        The article level.
    title : str
        The article title.

    Returns
    -------
    row : dict
        The row of the generated content saved in the database, or None.
    """

    pretty_title = removeUnderscores(title)
    pretty_title = removeItalics(title)
    prompt = overviewPromptDavinci(level, pretty_title)

    if prompt is None:
        return

    content, model = await aInfer(prompt)

    row = await aAddContent(aconn, level, title, "readuce", content, model)

    return row


async def aSubSection(aconn: AsyncConnection, level: int, title: str, id: str):
    """
    Parameters:
        aconn (AsyncConnection): Connection object for asynchronous database
        connection
        level (int): Level of the subsection
        title (str): Title of the subsection
        id (str): Unique identifier of the subsection

    Returns:
        row (dict): Dictionary of content row data

    Description:
        This function takes a connection object, level, title, and subsection
        id and returns the row data of the content. It uses the
        removeUnderscores and removeItalics functions to remove underscores
        and italics from the subsection title. It then uses the
        sectionPromptDavinci function to generate a prompt which is used in
        the aInfer function to generate content and model. The generated
        content and model are used in the aAddContent function to add a
        content row to the database.
    """

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
        text = f'Summarize "{title}" like I am 5 years old'

    elif level == 2:
        text = f'Summarize "{title}" like I am a teenager'

    elif level == 3:
        text = f'''
        Summarize "{title}" like I am almost knowledgeable in this field
        '''

    elif level == 4:
        text = f'''
        Summarize "{title}" like I am knowledgeable in this field
        '''

    elif level == 5:
        text = f'''
        Summarize "{title}" like I am an expert in this field
        '''

    return text


def sectionPromptDavinci(level: int, title: str, section: str):

    text = ''

    if level == 1:
        text = f'''
        I know "{title}". \
        Tell me specifically its {section} like I am 5 years old
        '''

    elif level == 2:
        text = f'''
        I know "{title}". \
        Tell me specifically its {section} like I am a teenager
        '''

    elif level == 3:
        text = f'''
        I know "{title}". \
        Tell me specifically its {section} like I am almost \
        knowledgeable in this field
        '''

    elif level == 4:
        text = f'''
        I know "{title}". \
        Tell me specifically its {section} like I am knowledgeable \
        in this field
        '''

    elif level == 5:
        text = f'''
        I know "{title}". \
        Tell me specifically its {section} like I am an expert in \
        this field
        '''

    return text
