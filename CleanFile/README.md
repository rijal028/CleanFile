# CleanFile

CleanFile is a beginner-friendly web tool that rebuilds PDF documents into a clean, script-free version.

## Problem

Many people receive PDF files for school, work, or official purposes but cannot verify if they contain hidden scripts or unsafe elements.

Interactive features such as JavaScript or embedded objects are unnecessary for most everyday documents.

## Solution

CleanFile extracts only readable text from a PDF and reconstructs a brand-new document.

The rebuilt file:
- Contains no scripts
- Contains no embedded actions
- Contains no hidden objects
- Uses safe default fonts
- Is lightweight and readable

It prioritizes safety and clarity over exact visual replication.

## How It Works

1. Upload a PDF
2. Extract readable text
3. Rebuild a new clean PDF from scratch
4. Download the safe version

The original document structure is not reused.

## Tech Stack

- Python
- Streamlit
- PyPDF
- ReportLab

## How to Run Locally

Install dependencies:

pip install -r requirements.txt

Run the app:

python -m streamlit run app.py

## Target Use Cases

- School assignments
- Reports
- Administrative documents
- Government forms (text-based)
- Everyday document sharing

## Limitations

- Complex layouts may not be perfectly preserved
- Images and interactive elements are not retained
- Scientific symbols may be simplified

This is intentional to ensure safety and simplicity.
