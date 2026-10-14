"""Deterministic normalization and paragraph-aware chunking."""

import hashlib
import re
import unicodedata
from collections.abc import Iterable

from sehat_api.knowledge.models import ExtractedSection

_CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_HORIZONTAL_SPACE = re.compile(r"[^\S\n]+")
_EXCESS_NEWLINES = re.compile(r"\n{3,}")


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).replace("\r\n", "\n").replace("\r", "\n")
    normalized = _CONTROL_CHARACTERS.sub("", normalized)
    lines = [_HORIZONTAL_SPACE.sub(" ", line).strip() for line in normalized.split("\n")]
    return _EXCESS_NEWLINES.sub("\n\n", "\n".join(lines)).strip()


def content_digest(sections: Iterable[ExtractedSection]) -> str:
    canonical = "\n\n".join(normalize_text(section.text) for section in sections)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def split_section(
    section: ExtractedSection,
    *,
    max_chars: int = 700,
) -> list[tuple[str, int, int]]:
    """Return content plus one-based paragraph range without crossing pages."""

    if max_chars < 100:
        raise ValueError("max_chars must be at least 100")
    paragraphs = [
        part.strip()
        for part in normalize_text(section.text).split("\n\n")
        if part.strip()
    ]
    chunks: list[tuple[str, int, int]] = []
    pending: list[str] = []
    start = 1

    def flush(end: int) -> None:
        nonlocal pending, start
        if pending:
            chunks.append(("\n\n".join(pending), start, end))
            pending = []

    for index, paragraph in enumerate(paragraphs, start=1):
        if len(paragraph) > max_chars:
            flush(index - 1)
            words = paragraph.split()
            segment: list[str] = []
            for word in words:
                candidate = " ".join([*segment, word])
                if segment and len(candidate) > max_chars:
                    chunks.append((" ".join(segment), index, index))
                    segment = [word]
                else:
                    segment.append(word)
            if segment:
                chunks.append((" ".join(segment), index, index))
            start = index + 1
            continue

        candidate = "\n\n".join([*pending, paragraph])
        if pending and len(candidate) > max_chars:
            flush(index - 1)
            start = index
        pending.append(paragraph)

    flush(len(paragraphs))
    return chunks
