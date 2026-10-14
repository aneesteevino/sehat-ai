"""Bounded extraction for approved local text and PDF fixtures."""

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from sehat_api.knowledge.models import ExtractedSection


class DocumentRejectedError(ValueError):
    """The document failed a type, path, size, encryption, or extraction boundary."""


@dataclass(frozen=True, slots=True)
class ExtractionLimits:
    max_file_bytes: int = 2 * 1024 * 1024
    max_pages: int = 50
    max_page_stream_bytes: int = 2 * 1024 * 1024
    max_extracted_characters: int = 250_000


def _read_approved_path(path: Path, approved_root: Path, limits: ExtractionLimits) -> bytes:
    resolved_root = approved_root.resolve()
    resolved_path = path.resolve()
    if not resolved_path.is_relative_to(resolved_root):
        raise DocumentRejectedError("Document path escapes the approved source directory.")
    if not resolved_path.is_file():
        raise DocumentRejectedError("Approved document is missing.")
    size = resolved_path.stat().st_size
    if size == 0 or size > limits.max_file_bytes:
        raise DocumentRejectedError("Document size is outside the allowed range.")
    return resolved_path.read_bytes()


def extract_document(
    path: Path,
    approved_root: Path,
    content_type: str,
    *,
    limits: ExtractionLimits | None = None,
) -> list[ExtractedSection]:
    active_limits = limits or ExtractionLimits()
    data = _read_approved_path(path, approved_root, active_limits)

    if content_type == "text/plain":
        if path.suffix.casefold() != ".txt" or b"\x00" in data:
            raise DocumentRejectedError("Text fixture has an invalid type or contains NUL bytes.")
        try:
            text = data.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise DocumentRejectedError("Text fixtures must be valid UTF-8.") from exc
        if len(text) > active_limits.max_extracted_characters:
            raise DocumentRejectedError("Extracted text exceeds the character limit.")
        return [ExtractedSection(text=text, page_number=None)]

    if content_type != "application/pdf" or path.suffix.casefold() != ".pdf":
        raise DocumentRejectedError("Only approved text and PDF content types are supported.")
    if not data.startswith(b"%PDF-"):
        raise DocumentRejectedError("PDF signature is invalid.")

    try:
        reader = PdfReader(BytesIO(data), strict=True)
        if reader.is_encrypted:
            raise DocumentRejectedError("Encrypted PDFs are not accepted.")
        if not 1 <= len(reader.pages) <= active_limits.max_pages:
            raise DocumentRejectedError("PDF page count is outside the allowed range.")

        sections: list[ExtractedSection] = []
        total_characters = 0
        for page_number, page in enumerate(reader.pages, start=1):
            contents = page.get_contents()
            if (
                contents is not None
                and len(contents.get_data()) > active_limits.max_page_stream_bytes
            ):
                raise DocumentRejectedError("A PDF page content stream exceeds the limit.")
            text = page.extract_text() or ""
            total_characters += len(text)
            if total_characters > active_limits.max_extracted_characters:
                raise DocumentRejectedError("Extracted PDF text exceeds the character limit.")
            if text.strip():
                sections.append(ExtractedSection(text=text, page_number=page_number))
    except DocumentRejectedError:
        raise
    except (PdfReadError, ValueError, TypeError, KeyError) as exc:
        raise DocumentRejectedError("PDF parsing failed.") from exc

    if not sections:
        raise DocumentRejectedError("PDF contains no extractable text; OCR is not enabled.")
    return sections
