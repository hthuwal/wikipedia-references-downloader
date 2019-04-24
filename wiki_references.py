import click
import os
import string
import unicodedata
import wikipedia

from download import preprocess_url
from tqdm import tqdm
from wikipedia import DisambiguationError

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255


def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)

    # Truncate file names for windows
    if len(cleaned_filename) > char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]


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
    except Exception as e:
        return {}


def save_file(data, file_name, data_type):
    if data_type == "pdf":
        f = open(file_name, "wb")
    else:
        f = open(file_name, "w")
    f.write(data)
    f.close()


def save_reference_pages(keyword, threshold=None, target_dir="wikipedia", resume=False):
    target_dir = os.path.join(target_dir, keyword)
    if resume and os.path.exists(target_dir):
        return

    reference_links = get_references(keyword)
    for candidate in reference_links:
        if(candidate == keyword):
            sub_dir = target_dir
        else:
            sub_dir = os.path.join(target_dir, clean_filename(candidate))
        links_file = os.path.join(sub_dir, "references.txt")
        links = reference_links[candidate]

        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)

        with open(links_file, "w") as file:
            for link in links:
                link = preprocess_url(link)
                file.write(f"{link}\n")


@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--threshold', '-t', default=None, type=int, help='Max Number of Referneces per page to be extracted.')
@click.option('--resume', help='Continue from last run...', is_flag=True)
def run(file, threshold, resume):
    """
    Extract links to references from the wikipedia page of each keyword (one per line) in FILE.
    """
    with open(file, "r") as f:
        keywords = [line.strip() for line in f.readlines()]
        for line in tqdm(keywords, ascii=True):
            line = line.strip()
            save_reference_pages(line, threshold=threshold, resume=resume)


if __name__ == '__main__':
    run()
