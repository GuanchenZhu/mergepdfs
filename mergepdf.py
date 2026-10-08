#!/usr/bin/env python3
"""Merge all PDFs in the current folder into output/merged.pdf.

- Natural sort order (1.pdf, 2.pdf, 10.pdf instead of 1, 10, 2)
- Skips the output folder, corrupted files, and encrypted files
- Prints the merge order and page counts before merging
- Optional --confirm flag to approve the order before merging
- Adds one bookmark per source file

Requires: pip install pypdf
Usage:    python mergepdf.py [--confirm] [-o NAME.pdf]
"""
import argparse
import re
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def natural_key(path: Path):
    """Sort key so that 'file2.pdf' comes before 'file10.pdf'."""
    parts = re.split(r"(\d+)", path.name.lower())
    return [int(p) if p.isdigit() else p for p in parts]


def main():
    ap = argparse.ArgumentParser(description="Merge all PDFs in the current folder.")
    ap.add_argument("-o", "--output", default="merged.pdf", help="output file name")
    ap.add_argument("--confirm", action="store_true", help="confirm order before merging")
    args = ap.parse_args()

    folder = Path.cwd()
    out_dir = folder / "output"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / args.output

    # Only scan the current folder (non-recursive), so files in output/
    # are never merged back into the result.
    pdfs = sorted(
        (p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"),
        key=natural_key,
    )
    if not pdfs:
        sys.exit("No PDF files found in the current folder.")

    # Validate each file: readable, not encrypted, count pages.
    valid = []
    for p in pdfs:
        try:
            reader = PdfReader(p)
            if reader.is_encrypted:
                print(f"[SKIP] Encrypted: {p.name}")
                continue
            valid.append((p, reader, len(reader.pages)))
        except Exception as e:
            print(f"[SKIP] Cannot read {p.name}: {e}")

    if not valid:
        sys.exit("No valid PDFs to merge.")

    print("\nMerge order:")
    total = 0
    for i, (p, _, n) in enumerate(valid, 1):
        print(f"  {i:>3}. {p.name}  ({n} pages)")
        total += n
    print(f"{len(valid)} files, {total} pages total\n")

    if args.confirm:
        answer = input("Is the order correct? Press Enter to continue, or type n to cancel: ")
        if answer.strip().lower() == "n":
            sys.exit("Cancelled.")

    writer = PdfWriter()
    for p, reader, _ in valid:
        start = len(writer.pages)
        for page in reader.pages:
            writer.add_page(page)
        writer.add_outline_item(p.stem, start)  # bookmark for this source file

    with open(out_path, "wb") as f:
        writer.write(f)

    print(f"Done: {out_path}")


if __name__ == "__main__":
    main()
