"""
https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text/1983219#1983219
"""

from bs4 import BeautifulSoup
from bs4.element import Comment
import requests


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def preprocess_url(url: str):
    if "//arxiv.org/" in url:
        url = url.replace("abs", "pdf")
        url += ".pdf"
    return url


def get_data(url):
    url = preprocess_url(url)

    try:
        web_page = requests.get(url, timeout=(10, None))
        content_type = web_page.headers.get('content-type')
    except Exception:
        return "Timeout", None

    if content_type is None:
        content_type = ""

    if web_page.status_code == 200:
        if 'application/pdf' in content_type:
            return web_page.content, "pdf"
        else:
            soup = BeautifulSoup(web_page.content, 'html.parser')
            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts)
            data = u" ".join(t.strip(" ").strip("\t") for t in visible_texts if t.strip())
            return data, "txt"

    return str(web_page.status_code), None


if __name__ == "__main__":
    print(get_data("https://www.lipsum.com/"))
