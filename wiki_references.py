import download
import os
import wikipedia

from tqdm import tqdm
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

def save_file(text, file):
    with open(file, "w") as f:
        f.write(text)


def save_reference_pages(keyword, target_dir="wikipedia"):
    reference_links = get_references(keyword)
    target_dir = os.path.join(target_dir, keyword)

    for candidate in reference_links:
        sub_dir = os.path.join(target_dir, candidate)
        links = reference_links[candidate]
        
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)
        
        for i, link in enumerate(links):
            file = os.path.join(sub_dir, "%04d.txt" % i)
            text = download.text_from_html(link)
            save_file(text, file)
            
