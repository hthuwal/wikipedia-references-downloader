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


def get_data(url):
    try:
        web_page = requests.get(url, timeout=(5, None))
        content_type = web_page.headers.get('content-type')
    except Exception:
        return None, None

    if content_type is None:
        content_type = ""

    if web_page.status_code == 200:
        if 'application/pdf' in content_type:
            return web_page.content, "pdf"
        else:
            soup = BeautifulSoup(web_page.content, 'html.parser')
            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts)
            data = u"\n".join(t.strip() for t in visible_texts if t.strip())
            return data, "txt"

    return None, None


if __name__ == "__main__":
    print(get_data("https://www.lipsum.com/"))
