#!/usr/bin/env python3
"""
Convert a Markdown file to a formatted Word (.docx) document using pandoc.
Usage: python md_to_docx.py <input.md> <output.docx>
"""

import subprocess
import sys
import os


def convert_md_to_docx(input_md: str, output_docx: str) -> None:
    """Convert Markdown to Word using pandoc with professional formatting."""
    if not os.path.exists(input_md):
        print(f"[ERROR] Input file not found: {input_md}")
        sys.exit(1)

    cmd = [
        "pandoc",
        input_md,
        "-o", output_docx,
        "--from", "markdown",
        "--to", "docx",
        "-V", "lang=zh-CN",
        "--toc",
        "--toc-depth=2",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[OK] Word document generated: {output_docx}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] pandoc conversion failed:\n{e.stderr}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python md_to_docx.py <input.md> <output.docx>")
        sys.exit(1)
    convert_md_to_docx(sys.argv[1], sys.argv[2])
