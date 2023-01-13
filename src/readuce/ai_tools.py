from bs4 import BeautifulSoup
from src.data import db
# from src.mystic.nlp import gpt3_neo_2_7b
from src.openai.nlp import gpt3_davinci
# from src.octopus.utils import removeQuotes


def addAiSummary(
    conn,
    soup: BeautifulSoup,
    level: int,
    title: str
):
    if soup.body is not None:

        content = db.getContent(conn, level, title, "summary")

        if content is None:
            pretty_title = ""
            if soup.title is not None:
                pretty_title = soup.title.string

            prompt = summaryPromptDavinci(level, pretty_title)

            print(f"The final prompt is:\n\n {prompt}")

            if prompt is None:
                return

            content = gpt3_davinci.infer(prompt)
            db.addContent(conn, level, title, "summary", content)

        # text = """Ansible is an open source automation tool for Linux \\
        #     systems. It can be used as part of your infrastructure \\
        #     or application management workflow by automating repetitive \\
        #     tasks such as provisioning servers, deploying applications, \\
        #     configuring services, managing users, groups, hosts, networks, \\
        #     etc."""

        first_p = soup.body.find('p')

        tag = BeautifulSoup(
            f"<div class='ai_summary'><p>{content}</p></div> {first_p}",
            'html.parser'
        )

        tag = BeautifulSoup(
            f"<h2>Summary</h2><p>{content}</p> <h2>Article</h2> {first_p}",
            'html.parser'
        )

        if first_p is not None:
            first_p.replace_with(tag)

    return soup


def summaryPrompt(level: int, title: str | None):
    if title is None:
        return

    text = """
    The following is a conversation with all-knowing super-intelligent\\
    assistant.
    The assistant receives is helpful, creative, clever, and offers to\\
    expand the user's knowledge.
    The assistant explains the concept received in the prompt in different\\
    levels of difficulty.


    """

    if level == 1:
        text = text + f"""
        Human: 'Summarize {title} like I am 5 years old":

        Assistant:
        """

    elif level == 2:
        text = text + f"""
        Human: 'Summarize {title} like I am a teenager":

        Assistant:
        """

    elif level == 3:
        text = text + f"""
        Human: 'Summarize {title} like I am an adult":

        Assistant:
        """

    elif level == 4:
        text = text + f"""
        Human: 'Summarize {title} like I am a smart person":

        Assistant:
        """

    elif level == 5:
        text = text + f"""
        Human: 'Summarize {title} like I am an expert in\\
        the field surround this topic":

        Assistant:
        """

    return text


def summaryPromptDavinci(level: int, title: str | None):
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
