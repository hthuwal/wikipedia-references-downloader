## Wikipedia References Extractor

- Download references from the wikipedia page of each keyword (one per line) in FILE.
- Incase no single page exists for the corresponding keyword.
    + keyword is searched on wikipedia.
    + references from the wikipedia pages of top 5 results are used.

### Dependencies

```
pip install -r requirements.txt
```

### Usage

```
python wiki_references.py [OPTIONS] FILE
```

### Page Handling

- References which point to a html page are downloaded and cleaned.
    + Since the references point to different kinds of websites. Its impossible to completely clean the data.
        * Each site requires its own cleaner.
    + However, basic cleaning is performed and only the raw textual data is kept.
        * All HTML, CSS and JS is removed.

- References which point to a pdf are downloaded as binary pdf files.
    + No Need to do HTML, CSS cleaning here.

- References pointing to arxiv website are converted to direct pdf links and are then downloaded as pdfs.
