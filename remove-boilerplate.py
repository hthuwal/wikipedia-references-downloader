import justext
import os
import click
import shutil
from tqdm import tqdm


def clean(content):
    paragraphs = justext.justext(content, justext.get_stoplist("English"))
    content = ""
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            content += f"{paragraph.text}\n\n"
    return content


def write_to_file(file, content):
    with open(file, "w") as f:
        f.write(content)


@click.command()
@click.argument('sdir', type=click.Path(exists=True))
def run(sdir):
    """
    Remove Boilerplate from raw html pages in the directory "SDIR"
    """
    for rdir, folders, files in os.walk(sdir):
        if files and os.path.basename(rdir) != 'cleaned':
            print(rdir)
            target_dir = os.path.join(rdir, "cleaned")

            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            os.makedirs(target_dir)

            for file in tqdm(files, ascii=True):
                name, ext = os.path.splitext(file)

                if ext in ['.html', '.xml', '.xhtml', '.php']:
                    source_file = os.path.join(rdir, file)
                    target_file = os.path.join(target_dir, name + ".txt")

                    content = open(source_file, "rb").read()
                    content = content.decode(errors='ignore')
                    cleaned_content = clean(content)
                    write_to_file(target_file, cleaned_content)


if __name__ == "__main__":
    run()
