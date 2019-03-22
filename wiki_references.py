import wikipedia
from wikipedia import DisambiguationError

def get_references(keyword):
    try:
        page = wikipedia.page(keyword)
        return page.references
    except DisambiguationError:
        pass

print(get_references("Harish"))