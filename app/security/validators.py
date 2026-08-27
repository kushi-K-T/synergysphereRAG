import os
import re
from fastapi import HTTPException

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md", ".csv"}

def validate_file_extension(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    ext_lower = ext.lower()
    if ext_lower not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )
    return ext_lower

def validate_file_size(size_in_bytes: int, max_size_mb: int) -> None:
    max_bytes = max_size_mb * 1024 * 1024
    if size_in_bytes > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum threshold of {max_size_mb}MB."
        )

def sanitize_path(filename: str) -> str:
    cleaned = os.path.basename(filename)
    cleaned = re.sub(r'[^a-zA-Z0-9_.-]', '_', cleaned)
    return cleaned