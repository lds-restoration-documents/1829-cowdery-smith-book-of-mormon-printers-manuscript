#!/usr/bin/env python3
"""Extract the text layer of the JSP transcript PDF to one text file (pages separated by =====PAGE=====).
Usage: python tools/extract_reference.py "JSP.pdf" work/jsp.txt
In the POC the JSP PDF ("Printer's Manuscript of the Book of Mormon, circa August 1829-circa January 1830, Page i.pdf",
380 pages) gave 1.5 MB of text with `[p. N]` page markers, `<x>` for insertions and `[x]` for editorial reconstruction."""
import sys, pypdfium2 as pdfium
d = pdfium.PdfDocument(sys.argv[1])
open(sys.argv[2], 'w').write(''.join(d[i].get_textpage().get_text_range() + '\n=====PAGE=====\n' for i in range(len(d))))
