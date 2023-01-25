from bs4 import BeautifulSoup


def removeItalics(text: str | None):
    if text is not None:
        text = text.replace("&lt;i&gt;", "")
        text = text.replace("&lt;/i&gt;", "")
        text = text.replace("<i>", "")
        text = text.replace("</i>", "")
        return text
    return ""


def removeQuotes(text: str | None):
    if text is not None:
        text = text.replace("\"", "")
        return text
    return ""


def removeAsterisks(text: str | None):
    if text is not None:
        text = text.replace("*", "")
        return text
    return ""


def removeUnderscores(text: str | None):
    if text is not None:
        text = text.replace('_', ' ')
        return text
    return ""


def fixMath(soup):
    spans = soup.body.find_all(attrs={'class': "mwe-math-mathml-inline"})

    for s in spans:
        s['style'] = ''

    scripts = BeautifulSoup(
        '''
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6">
    </script> <script id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>''', 'html.parser')

    soup.body.insert(0, scripts)

    return soup


def fixMathFallbackImage(soup):
    images = soup.body.find_all(
        attrs={'class': "mwe-math-fallback-image-inline"})

    for i in images:
        del i['style']

    return soup


def fixSideBarListTitle(soup):
    spans = soup.body.find_all(attrs={'class': "sidebar-list-title"})

    for s in spans:
        del s['style']

    return soup


def includeTitle(soup):
    title = soup.title.string
    title = removeItalics(title)
    title = removeQuotes(title)
    title = removeAsterisks(title)
    title = removeUnderscores(title)

    tag = BeautifulSoup(f"""<div class="title">{title}</div>""", 'html.parser')

    soup.body.insert(0, tag)
