import wikipedia
from wikipedia import DisambiguationError

def get_references(keyword, recurse=True):
    try:
        page = wikipedia.page(keyword)
        return {keyword: page.references}
  
    except DisambiguationError as e:
        if recurse:
            options = wikipedia.search(keyword, results=5)  ## Get Top 5 candidates 
            references = {}
            for each in options:
                references.update(get_references(each, recurse=False))
            return references
        else:
            return {}

print(get_references("Harish"))