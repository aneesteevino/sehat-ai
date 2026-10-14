from pathlib import Path

import pytest
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject
from sehat_api.knowledge.extraction import DocumentRejectedError, extract_document


def write_text_pdf(path: Path, text: str, *, password: str | None = None) -> None:
    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)
    font = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
        }
    )
    page[NameObject("/Resources")] = DictionaryObject(
        {
            NameObject("/Font"): DictionaryObject(
                {NameObject("/F1"): writer._add_object(font)}
            )
        }
    )
    stream = DecodedStreamObject()
    safe_text = text.replace("(", "\\(").replace(")", "\\)")
    stream.set_data(f"BT /F1 12 Tf 72 720 Td ({safe_text}) Tj ET".encode())
    page[NameObject("/Contents")] = writer._add_object(stream)
    if password:
        writer.encrypt(password)
    with path.open("wb") as handle:
        writer.write(handle)


def test_extracts_utf8_text_inside_approved_root(tmp_path: Path) -> None:
    fixture = tmp_path / "fixture.txt"
    fixture.write_text("Approved text.", encoding="utf-8")

    sections = extract_document(fixture, tmp_path, "text/plain")

    assert sections[0].text == "Approved text."
    assert sections[0].page_number is None


def test_rejects_path_escape_and_nul_bytes(tmp_path: Path) -> None:
    approved = tmp_path / "approved"
    approved.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("outside", encoding="utf-8")
    with pytest.raises(DocumentRejectedError, match="escapes"):
        extract_document(outside, approved, "text/plain")

    unsafe = approved / "unsafe.txt"
    unsafe.write_bytes(b"unsafe\x00text")
    with pytest.raises(DocumentRejectedError, match="NUL"):
        extract_document(unsafe, approved, "text/plain")


def test_extracts_text_pdf_and_rejects_encrypted_pdf(tmp_path: Path) -> None:
    plain = tmp_path / "plain.pdf"
    encrypted = tmp_path / "encrypted.pdf"
    write_text_pdf(plain, "Traceable PDF evidence")
    write_text_pdf(encrypted, "Private evidence", password="test-password")

    sections = extract_document(plain, tmp_path, "application/pdf")

    assert sections[0].page_number == 1
    assert "Traceable PDF evidence" in sections[0].text
    with pytest.raises(DocumentRejectedError, match="Encrypted"):
        extract_document(encrypted, tmp_path, "application/pdf")
