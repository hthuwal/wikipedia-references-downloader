import click
import justext
import os
import pdftotext
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
    if not content:
        return
    with open(file, "w") as f:
        f.write(content)


def extract_text_from_pdf(source_file):
    with open(source_file, "rb") as f:
        pdf = pdftotext.PDF(f)
        return "\n\n".join(pdf)


@click.command()
@click.argument('sdir', type=click.Path(exists=True))
def run(sdir):
    """
    Remove Boilerplate from raw html pages in the directory "SDIR"
    """
    for rdir, folders, files in os.walk(sdir):
        if files:
            print(rdir)
            target_dir = os.path.join("cleaned", rdir)

            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            os.makedirs(target_dir)

            for file in tqdm(files, ascii=True):
                name, ext = os.path.splitext(file)
                source_file = os.path.join(rdir, file)
                target_file = os.path.join(target_dir, name + ".txt")

                if ext in ['.html', '.xml', '.xhtml', '.php']:
                    content = open(source_file, "rb").read()
                    content = content.decode(errors='ignore')
                    cleaned_content = clean(content).strip()
                    write_to_file(target_file, cleaned_content)

                elif ext == ".pdf":
                    content = extract_text_from_pdf(source_file).strip()
                    write_to_file(target_file, content)

                elif file == "log.txt":
                    shutil.copy(source_file, target_file)


if __name__ == "__main__":
    run()
