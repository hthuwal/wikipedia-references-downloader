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


def text_from_html(url):
    web_page = requests.get(url)
    if web_page.status_code:
        soup = BeautifulSoup(web_page.content, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)
    
    return ""



if __name__ == "__main__":
    print(text_from_html("https://www.lipsum.com/"))