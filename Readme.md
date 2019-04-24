# Wikipedia References Extractor

- Download references from the wikipedia page of each keyword (one per line) in FILE.
- Incase no single page exists for the corresponding keyword.
    + keyword is searched on wikipedia.
    + references from the wikipedia pages of top 5 results are used.

## Installing Dependencies

- aria2c
- Installing python dependencies
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
  │   └── references.txt
  └── Velocity
      └── references.txt
  ```

- `references.txt` will contain link to the references mentioned in the wikipedia pages of parent folders wikipedia page.

## Downloading the reference pages

```
bash download.sh wikipedia
```

- This will parallely download the links (at max 16 at a time) in all the `references.txt` files.
  + Uses `aria2c`
- For e.g. if a `reference.txt` file contains 5 links. These will be first downloaded as files with names 1, 2, 3, 4, 5.
- The script will then attempt to find appropriate extension for these files and rename them accordingly.
```
wikipedia
├── electron
│   ├── 10.html
│   ├── 1.html
│   ├── 2.html
│   ├── 3.html
│   ├── 4.html
│   ├── 5.html
│   ├── 6.html
│   ├── 7.html
│   ├── 8.html
│   ├── 9.html
│   ├── log.txt
│   └── references.txt
└── photon
    ├── 10.html
    ├── 1.pdf
    ├── 2.html
    ├── 3.html
    ├── 4.html
    ├── 5.pdf
    ├── 6.html
    ├── 7.pdf
    ├── 8.html
    ├── 9.html
    ├── log.txt
    └── references.txt
```
- `log.txt` file is also generated which keeps a record of which file number contains which links content.

## Cleaning the downloaded webpages

- Remove Boiler Plate from downloaded webpages using [justText](https://pypi.org/project/jusText/)
- Convert pdf files to txt using [pdftotext](https://pypi.org/project/pdftotext/)

```
python remove-boilerplate.py [OPTIONS] SDIR

  Remove Boilerplate from raw html pages in the directory "SDIR"

Options:
  --help  Show this message and exit.

```

- The script will create a folder called `cleaned` with the same directory structures as the SDIR but the raw files replaced with cleaned files.
- No file is created if after cleaning the content is empty.
```
cleaned
└── wikipedia
    ├── electron
    │   ├── 1.txt
    │   ├── 2.txt
    │   ├── 3.txt
    │   ├── 4.txt
    │   ├── 5.txt
    │   ├── 6.txt
    │   ├── 8.txt
    │   ├── 9.txt
    │   └── log.txt
    └── photon
        ├── 2.txt
        ├── 3.txt
        ├── 4.txt
        ├── 5.txt
        └── log.txt
```
