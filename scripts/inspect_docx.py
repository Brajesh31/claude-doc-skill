#!/usr/bin/env python3
"""Print a structural inventory of a DOCX file."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.oxml.ns import qn
    from docx.text.paragraph import Paragraph
    from docx.table import Table
except ImportError:
    print("Missing dependency. Install with: python -m pip install python-docx", file=sys.stderr)
    raise SystemExit(2)


def iter_blocks(document):
    """Yield top-level paragraphs and tables in their original order."""
    for child in document.element.body.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, document)
        elif child.tag == qn("w:tbl"):
            yield Table(child, document)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path, help="Path to a .docx file")
    args = parser.parse_args()

    if not args.docx.is_file():
        parser.error(f"File not found: {args.docx}")
    if args.docx.suffix.lower() != ".docx":
        parser.error("Expected a .docx file")

    try:
        document = Document(str(args.docx))
    except Exception as exc:
        print(f"Could not open DOCX: {exc}", file=sys.stderr)
        return 1

    paragraphs = tables = 0
    print(f"File: {args.docx}")
    print(f"Sections: {len(document.sections)}")
    print(f"Inline images: {len(document.inline_shapes)}")
    print("Content in document order:")

    for index, block in enumerate(iter_blocks(document), start=1):
        if isinstance(block, Paragraph):
            paragraphs += 1
            value = " ".join(block.text.split())
            if value:
                style = block.style.name if block.style else "Unknown"
                print(f"{index:04d} PARAGRAPH [{style}]: {value}")
        else:
            tables += 1
            print(f"{index:04d} TABLE: {len(block.rows)} rows x {len(block.columns)} columns")
            for row in block.rows:
                cells = [" ".join(cell.text.split()) for cell in row.cells]
                print("      | " + " | ".join(cells))

    print("\nSummary:")
    print(f"Paragraph blocks: {paragraphs}")
    print(f"Tables: {tables}")
    print(f"Inline images: {len(document.inline_shapes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
