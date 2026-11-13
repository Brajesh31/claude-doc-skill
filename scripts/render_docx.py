#!/usr/bin/env python3
"""Render a DOCX to PDF and page images using LibreOffice and Poppler."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def require_command(*names: str) -> str:
    for name in names:
        path = shutil.which(name)
        if path:
            return path
    raise RuntimeError(f"Required command not found. Install one of: {', '.join(names)}")


def run(command: list[str]) -> None:
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        details = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{details}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path, help="Input .docx file")
    parser.add_argument("--output-dir", type=Path, default=Path("rendered"))
    parser.add_argument("--dpi", type=int, default=150)
    args = parser.parse_args()

    if not args.docx.is_file():
        parser.error(f"File not found: {args.docx}")
    if args.docx.suffix.lower() != ".docx":
        parser.error("Expected a .docx file")
    if not 50 <= args.dpi <= 600:
        parser.error("--dpi must be between 50 and 600")

    try:
        office = require_command("libreoffice", "soffice")
        pdftoppm = require_command("pdftoppm")
        args.output_dir.mkdir(parents=True, exist_ok=True)
        source = args.docx.resolve()
        output_dir = args.output_dir.resolve()

        run([office, "--headless", "--convert-to", "pdf", "--outdir", str(output_dir), str(source)])
        pdf_path = output_dir / f"{source.stem}.pdf"
        if not pdf_path.is_file():
            raise RuntimeError(f"PDF output was not created: {pdf_path}")

        prefix = output_dir / "page"
        run([pdftoppm, "-png", "-r", str(args.dpi), str(pdf_path), str(prefix)])
        images = sorted(output_dir.glob("page-*.png"))
        if not images:
            raise RuntimeError("No page images were generated")

        print(f"PDF: {pdf_path}")
        print(f"Rendered pages: {len(images)}")
        for image in images:
            print(image)
        return 0
    except Exception as exc:
        print(f"Rendering failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
