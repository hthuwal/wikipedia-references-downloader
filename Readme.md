## Wikipedia References Extractor

- Download references from the wikipedia page of each keyword (one per line) in FILE.
- Incase no single page exists for the corresponding keyword.
    + keyword is searched on wikipedia.
    + references from the wikipedia pages of top 5 results are used.

### Dependencies

```
pip install -r requirements.txt
```

## Extracting Links 

```
python wiki_references.py [OPTIONS] FILE

  Extract links to references from the wikipedia page of each keyword (one
  per line) in FILE.

Options:
  -t, --threshold INTEGER  Max Number of Referneces per page to be extracted.
  --resume                 Continue from last run...
  --help                   Show this message and exit.

```

- References pointing to arxiv website are converted to direct pdf links.

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
  │       └── references.txt
  └── Velocity
      └── Velocity
          └── references.txt
  ```

- `references.txt` will contain link to the references mentioned in the wikipedia pages of parent folders wikipedia page.

## Downloading the reference pages

