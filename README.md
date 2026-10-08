# mergepdf

A small Python script that merges all PDF files in the current folder into a single PDF, saved in an `output/` subfolder.

## Features

- **Natural sort order**: `2.pdf` comes before `10.pdf` (not 1, 10, 2).
- **Order check**: prints the merge order and page count of each file before merging; use `--confirm` to approve it first.
- **Safe skipping**: corrupted or encrypted PDFs are reported and skipped instead of crashing the run.
- **Clean output**: the result is written to `output/merged.pdf`. Only the current folder is scanned, so previous outputs are never merged again.
- **Bookmarks**: each source file becomes a bookmark in the merged PDF.

## Requirements

- Python 3.8+
- [pypdf](https://pypi.org/project/pypdf/)

```bash
pip install pypdf
```

## Usage

1. Copy `mergepdf.py` into the folder that contains your PDFs.
2. Open a terminal in that folder and run:

```bash
python mergepdf.py
```

### Options

| Option | Description |
|--------|-------------|
| `--confirm` | Show the merge order and ask for confirmation before merging |
| `-o NAME.pdf`, `--output NAME.pdf` | Output file name (default: `merged.pdf`) |

### Examples

```bash
python mergepdf.py                    # merge everything into output/merged.pdf
python mergepdf.py --confirm          # review the order before merging
python mergepdf.py -o report.pdf      # custom output name
```

### Sample output

```
Merge order:
    1. chapter1.pdf  (12 pages)
    2. chapter2.pdf  (8 pages)
    3. chapter10.pdf  (20 pages)
3 files, 40 pages total

Done: /path/to/folder/output/merged.pdf
```

## Notes

- Files are sorted by name using natural ordering. To control the order exactly, prefix names with numbers (e.g. `01_intro.pdf`, `02_methods.pdf`).
- Password-protected PDFs are skipped. Remove the password first if you want them included.
- Subfolders are not scanned.

## License

Free to use and modify.
