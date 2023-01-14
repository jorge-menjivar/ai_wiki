from bs4 import BeautifulSoup


def removeItalics(title: str | None):
    if title is not None:
        title = title.replace("&lt;i&gt;", "")
        title = title.replace("&lt;/i&gt;", "")
        title = title.replace("<i>", "")
        title = title.replace("</i>", "")
        return title


def removeQuotes(title: str | None):
    if title is not None:
        title = title.replace("\"", "")
        return title


def removeAsterisks(title: str | None):
    if title is not None:
        title = title.replace("*", "")
        return title


def removeUnderscores(text: str):
    return text.replace('_', ' ')


def fixMath(soup):
    spans = soup.body.find_all(attrs={
        'class': "mwe-math-mathml-inline"}
    )

    for s in spans:
        s['style'] = ''

    scripts = BeautifulSoup('''
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6">
    </script> <script id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>''', 'html.parser')

    soup.body.insert(0, scripts)

    return soup


def fixSideBarListTitle(soup):
    spans = soup.body.find_all(attrs={
        'class': "sidebar-list-title"}
    )

    for s in spans:
        del s['style']

    return soup
