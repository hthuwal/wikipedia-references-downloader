import click
import os
import wikipedia

from download import get_data
from tqdm import tqdm
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

    for candidate in tqdm(reference_links, ascii=True):
        sub_dir = os.path.join(target_dir, candidate)
        log_file = os.path.join(sub_dir, "log.txt")
        links = reference_links[candidate]

        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)

        if threshold:
            links = links[:threshold]

        with open(log_file, "w") as log:
            for i, link in tqdm(enumerate(links), total=len(links), ascii=True):
                data, data_type = get_data(link)
                # print(link, data_type)
                if data_type is not None:
                    file_name = "%04d.%s" % (i, data_type)
                    file_path = os.path.join(sub_dir, file_name)
                    log.write("%s %s\n" % (file_name, link))
                    save_file(data, file_path, data_type)
                else:
                    log.write("Error:%s %s\n" % (data, link))


@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--threshold', '-t', default=None, type=int, help='Max Number of Referneces per page to be extracted.')
@click.option('--resume', help='Continue from last run...', is_flag=True)
def run(file, threshold, resume):
    """
    Download references from the wikipedia page of each keyword (one per line) in FILE.
    """
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            print("## %s ##" % line)
            save_reference_pages(line, threshold=threshold, resume=resume)
            print("")


if __name__ == '__main__':
    run()
