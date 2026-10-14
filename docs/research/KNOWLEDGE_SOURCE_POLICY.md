# Knowledge Source Policy

Last reviewed: 2026-10-14 (Asia/Karachi).

## Admission requirements

A source must have a stable publisher and canonical URL, an explicit version or update date, a recorded retrieval date, a documented reuse basis, mandatory attribution, a non-endorsement statement where applicable, a local checksum, and an approval state. Content without a clear reuse basis remains disabled.

Only approved files inside `data/source_registry` may enter the current pipeline. Registry paths are resolved and checked against that directory; path escapes, unknown types, empty files, oversized files, invalid UTF-8, NUL-containing text, encrypted PDFs, excessive PDF pages, excessive page streams, and excessive extracted text are rejected.

## Current evaluation sources

Two short, project-authored evaluation summaries are derived from CDC pages:

1. CDC Hand Hygiene Frequently Asked Questions, updated 2024-03-14.
2. CDC Clinical Signs and Symptoms of Influenza, updated 2026-02-04.

CDC states that most CDC/ATSDR website information is public domain, while warning that contractor, grantee, third-party, image, logo, and international-rights exceptions can apply. The registry therefore records the source, attribution, reuse-policy URL, non-endorsement language, exact evaluation summary, and checksum. These summaries are approved only for engineering evaluation and are not a clinical corpus.

## Data rules

- No patient records, personal health information, user uploads, or private documents.
- No network fetching during startup or tests; fixtures are reviewed and versioned in Git.
- No source is silently updated. Changed content requires a new checksum and source version.
- Extracted text remains untrusted data. It cannot select tools, modify policy, or become system instructions.
- Deletion must eventually tombstone the source version and remove its chunks and derived vectors.

## PDF limitation

`pypdf` extraction is enabled for approved, small, digitally created PDFs. OCR is not enabled. The parser runs in the API process in this milestone, so arbitrary user-uploaded PDFs remain prohibited. A later upload feature must add stronger file isolation, malware scanning, resource limits, and asynchronous processing before accepting untrusted documents.
