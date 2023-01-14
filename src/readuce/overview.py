from bs4 import BeautifulSoup
from src.data import db
from src.openai.nlp import gpt3_davinci


def addAIOverview(
    conn,
    soup: BeautifulSoup,
    level: int,
    title: str
):
    if soup.body is not None:

        row = db.getContentRow(conn, level, title, "readuce")

        content: str = ""
        model: str = ""
        timestamp: str = ""
        if row is None:
            pretty_title = ""
            if soup.title is not None:
                pretty_title = soup.title.string

            prompt = overviewPromptDavinci(level, pretty_title)

            if prompt is None:
                return

            content, model = gpt3_davinci.infer(prompt)

            row = db.addContent(conn, level, title, "readuce", content, model)

            if row is not None:
                timestamp = row.timestamp

        else:
            content = row.content
            model = row.model
            timestamp = row.timestamp

        first_p = soup.body.find('p')

        disclaimer = f'''This content was generated using {model} on \
            {timestamp}'''

        tag = BeautifulSoup(
            f'''<h2>Overview</h2>
                    <div class="ai_overview">
                        <p class="overview_disclaimer">{disclaimer}</p>
                        <p class="overview_content">{content}</p>
                    </div>
                <h2>Article</h2> {first_p}''',
            'html.parser'
        )

        if first_p is not None:
            first_p.replace_with(tag)

    return soup


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
