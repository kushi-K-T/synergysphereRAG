import os
import csv
from typing import List, Dict, Any
from pypdf import PdfReader
from docx import Document as DocxDocument

class DocumentLoader:
    @staticmethod
    def load_file(file_path: str) -> List[Dict[str, Any]]:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == ".pdf":
            return DocumentLoader._load_pdf(file_path)
        elif ext == ".docx":
            return DocumentLoader._load_docx(file_path)
        elif ext in [".txt", ".md"]:
            return DocumentLoader._load_text(file_path)
        elif ext == ".csv":
            return DocumentLoader._load_csv(file_path)
        else:
            raise ValueError(f"Unsupported loader extension: {ext}")

    @staticmethod
    def _load_pdf(path: str) -> List[Dict[str, Any]]:
        pages_content = []
        reader = PdfReader(path)
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            pages_content.append({
                "text": text,
                "page": idx + 1,
                "source": os.path.basename(path)
            })
        return pages_content

    @staticmethod
    def _load_docx(path: str) -> List[Dict[str, Any]]:
        doc = DocxDocument(path)
        full_text = "\n".join([p.text for p in doc.paragraphs if p.text])
        return [{"text": full_text, "page": 1, "source": os.path.basename(path)}]

    @staticmethod
    def _load_text(path: str) -> List[Dict[str, Any]]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return [{"text": content, "page": 1, "source": os.path.basename(path)}]

    @staticmethod
    def _load_csv(path: str) -> List[Dict[str, Any]]:
        rows = []
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(", ".join(row))
        return [{"text": "\n".join(rows), "page": 1, "source": os.path.basename(path)}]