from pathlib import Path
from zipfile import ZipFile
import re
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".txt", ".md", ".html", ".htm", ".pdf", ".odt"}


def clean_spaces(text: str) -> str:
    """Убирает лишние пробелы и переносы."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def read_pdf(path: Path) -> str:
    """Читает текст из PDF."""
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return clean_spaces(" ".join(pages))


def read_odt(path: Path) -> str:
    """Читает текст из ODT через content.xml."""
    with ZipFile(path) as archive:
        xml_content = archive.read("content.xml")

    root = ET.fromstring(xml_content)
    texts = []
    for elem in root.iter():
        if elem.text:
            texts.append(elem.text)
    return clean_spaces(" ".join(texts))


def read_html(path: Path) -> str:
    """Читает текст из HTML."""
    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    return clean_spaces(soup.get_text(" "))


def read_text_file(path: Path) -> str:
    """Читает обычный текст или Markdown."""
    return clean_spaces(path.read_text(encoding="utf-8", errors="ignore"))


def read_document(path: Path) -> str:
    """Выбирает способ чтения по расширению файла."""
    if path.suffix.lower() == ".pdf":
        return read_pdf(path)
    if path.suffix.lower() == ".odt":
        return read_odt(path)
    if path.suffix.lower() in {".html", ".htm"}:
        return read_html(path)
    return read_text_file(path)


def load_documents(docs_dir: str) -> list[dict]:
    """Загружает документы из папки."""
    docs = []
    for path in sorted(Path(docs_dir).rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            text = read_document(path)
            if text:
                docs.append(
                    {
                        "doc_id": path.stem,
                        "path": str(path),
                        "text": text,
                    }
                )
    return docs
