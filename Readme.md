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

### Output

- Suppose the input file (words.txt) contains the following lines.
  ```  
  Velocity
  Speed
  ```
- Running the command `python wiki_references.py words.txt` will create a folder `wikipedia` in the root directory. Its directory structure is as follows:
  ```
  wikipedia/
  ├── Speed
  │   └── Speed
  │       ├── 0001.txt
  │       ├── 0002.txt
  │       ├── 0003.txt
  │       ├── 0004.txt
  │       ├── 0005.txt
  │       ├── 0006.txt
  │       ├── 0008.txt
  │       ├── 0009.txt
  │       ├── 0010.txt
  │       ├── 0012.txt
  │       ├── 0013.txt
  │       ├── 0014.txt
  │       └── log.txt
  └── Velocity
      └── Velocity
          ├── 0000.txt
          ├── 0001.txt
          ├── 0002.txt
          ├── 0003.txt
          ├── 0004.txt
          ├── 0005.txt
          ├── 0006.txt
          ├── 0007.txt
          ├── 0008.txt
          ├── 0009.txt
          └── log.txt

  ```
- `log.txt` contains the information about which file corresponds to which link.
