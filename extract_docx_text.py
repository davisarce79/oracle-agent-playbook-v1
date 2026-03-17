#!/usr/bin/env python3
import zipfile
import xml.etree.ElementTree as ET
import sys
import re

def extract_docx_text(path):
    with zipfile.ZipFile(path) as z:
        # Find the main document XML
        doc_xml = z.read('word/document.xml')
    # Parse XML
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    root = ET.fromstring(doc_xml)
    # Gather all text elements
    texts = []
    for paragraph in root.findall('.//w:p', ns):
        runs = paragraph.findall('.//w:r', ns)
        para_text = ''.join(r.findtext('.//w:t', '', ns) for r in runs)
        if para_text.strip():
            texts.append(para_text.strip())
    return '\n\n'.join(texts)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: extract_docx_text.py <file.docx>")
        sys.exit(1)
    text = extract_docx_text(sys.argv[1])
    print(text)
