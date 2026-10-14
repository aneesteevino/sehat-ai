from sehat_api.knowledge.models import ExtractedSection
from sehat_api.knowledge.text import normalize_text, split_section


def test_normalization_is_deterministic_and_preserves_paragraphs() -> None:
    source = "  Wash\t hands.\r\n\r\n\r\nUse soap.\x00  "

    assert normalize_text(source) == "Wash hands.\n\nUse soap."


def test_chunking_preserves_paragraph_locator_ranges() -> None:
    section = ExtractedSection(
        text="First short paragraph.\n\nSecond short paragraph.\n\nThird short paragraph.",
        page_number=2,
    )

    chunks = split_section(section, max_chars=100)

    assert chunks == [
        ("First short paragraph.\n\nSecond short paragraph.\n\nThird short paragraph.", 1, 3)
    ]


def test_oversized_paragraph_is_split_without_losing_words() -> None:
    paragraph = " ".join(f"word{index}" for index in range(60))

    chunks = split_section(ExtractedSection(paragraph, None), max_chars=100)

    assert len(chunks) > 1
    assert " ".join(chunk[0] for chunk in chunks) == paragraph
    assert all((start, end) == (1, 1) for _, start, end in chunks)
