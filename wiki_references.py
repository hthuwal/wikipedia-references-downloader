import os
import wikipedia

from download import get_data
from wikipedia import DisambiguationError


def get_references(keyword, recurse=True):
    try:
        page = wikipedia.page(keyword)
        return {keyword: page.references}

    except DisambiguationError as e:
        if recurse:
            options = wikipedia.search(keyword, results=5)  # Get Top 5 candidates
            references = {}
            for each in options:
                references.update(get_references(each, recurse=False))
            return references
        else:
            return {}


def save_file(data, file_name, data_type):
    if data_type == "pdf":
        f = open(file_name, "wb")
    else:
        f = open(file_name, "w")
    f.write(data)
    f.close()


def save_reference_pages(keyword, target_dir="wikipedia"):
    reference_links = get_references(keyword)
    target_dir = os.path.join(target_dir, keyword)

    for candidate in reference_links:
        sub_dir = os.path.join(target_dir, candidate)
        log_file = os.path.join(sub_dir, "log.txt")
        links = reference_links[candidate]

        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)

        with open(log_file, "w") as log:
            for i, link in enumerate(links):
                data, data_type = get_data(link)
                print(link, data_type)
                if data_type is not None:
                    file_name = "%04d.%s" % (i, data_type)
                    file_path = os.path.join(sub_dir, file_name)
                    log.write("%s %s\n" % (file_name, link))
                    save_file(data, file_path, data_type)
                else:
                    log.write("Error:%s %s" % (data, link))


save_reference_pages("Earth")
