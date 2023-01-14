def removeItalics(title: str | None):
    if title is not None:
        title = title.replace("&lt;i&gt;", "")
        title = title.replace("&lt;/i&gt;", "")
        title = title.replace("<i>", "")
        title = title.replace("</i>", "")
        print(f'new title: {title}')
        return title


def removeQuotes(title: str | None):
    if title is not None:
        title = title.replace("\"", "")
        print(f'new title: {title}')
        return title


def removeAsterisks(title: str | None):
    if title is not None:
        title = title.replace("*", "")
        print(f'new title: {title}')
        return title


def removeUnderscores(text: str):
    return text.replace('_', ' ')
