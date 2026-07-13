from pypdf import PdfReader
from docx import Document
import pandas as pd


def read_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def read_docx(file):
    doc = Document(file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def read_excel(file):
    excel = pd.ExcelFile(file)

    text = ""

    for sheet in excel.sheet_names:
        df = pd.read_excel(excel, sheet_name=sheet)

        text += f"\nSheet : {sheet}\n"
        text += df.to_string(index=False)
        text += "\n"

    return text


def read_txt(file):
    return file.read().decode("utf-8")


def extract_text(uploaded_file):
    extension = uploaded_file.name.split(".")[-1].lower()

    if extension == "pdf":
        return read_pdf(uploaded_file)

    elif extension == "docx":
        return read_docx(uploaded_file)

    elif extension == "xlsx":
        return read_excel(uploaded_file)

    elif extension == "txt":
        return read_txt(uploaded_file)

    else:
        return ""