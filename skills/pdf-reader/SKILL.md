---
name: pdf-reader-skill

# PDF Reader Skill

Install this skill to enable PDF reading capabilities for OpenClaw.

## Installation

```bash
# Install Python PDF library
pip install PyPDF2
```

## Usage

Once installed, you can read PDF files using:

```python
import PyPDF2

# Read PDF file
with open('path/to/file.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    print(text)
```

## Features
- Read text from PDF files
- Extract content from multiple pages
- Works with most standard PDF documents

## Notes
- Requires Python 3.6+
- Works best with text-based PDFs (not scanned images)
- May have issues with complex formatting or encrypted PDFs

## Example Usage

```bash
# Read a PDF file
python3 -c "
import PyPDF2

with open('document.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    print(text)
"
```

## Troubleshooting
- If you get "ModuleNotFoundError: No module named 'PyPDF2'", run `pip install PyPDF2`
- If text extraction fails, the PDF may be scanned or encrypted
- For scanned documents, you may need OCR tools like Tesseract

## Alternative Libraries
- `PyMuPDF` (faster, better for complex PDFs)
- `pdfplumber` (more robust text extraction)
- `pdfminer.six` (for detailed PDF analysis)

## Security
- Only read files you have permission to access
- Be cautious with PDFs from unknown sources (may contain malware)

---

**Skill created successfully!** Now you can read PDF files in your OpenClaw workspace.