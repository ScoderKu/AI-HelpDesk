"""Lightweight bilingual Markdown/TXT keyword retrieval for the US-15 RAG MVP."""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import TypedDict


KNOWLEDGE_ROOT = Path(
    os.getenv("KNOWLEDGE_BASE_DIR", str(Path(__file__).resolve().parents[2] / "knowledge"))
).resolve()
TOKEN_RE = re.compile(r"[\w+#.-]{2,}", re.UNICODE)
MAX_DOCUMENT_BYTES = 512_000
MAX_CHUNK_CHARS = 8_000
DEFAULT_LIMIT = 3
MAX_LIMIT = 5

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "can", "do",
    "for", "from", "how", "i", "in", "is", "it", "of", "on", "or", "the",
    "to", "was", "what", "when", "where", "which", "with", "you", "your",
    "ja", "että", "ei", "en", "et", "se", "sen", "on", "ovat", "kuinka",
    "mitä", "mikä", "miksi", "kun", "tai", "sekä", "voi", "voiko", "minä",
    "miten", "tämä", "tuo", "niin", "jos", "olen", "olla", "ole",
    "kuinka", "kauan", "ennen", "mistä", "missä", "voinko", "sain",
}


class KnowledgeResult(TypedDict):
    title: str
    source: str
    section: str
    status: str
    excerpt: str
    score: int
    content: str


def _tokens(value: str) -> list[str]:
    return [
        token.casefold().strip("._-")
        for token in TOKEN_RE.findall(value)
        if len(token.strip("._-")) >= 2
        and token.casefold().strip("._-") not in STOP_WORDS
    ]


def _read_sections(path: Path) -> list[tuple[str, str, str, str]]:
    try:
        if path.stat().st_size > MAX_DOCUMENT_BYTES:
            return []
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError):
        return []

    title = path.stem.replace("-", " ").replace("_", " ").strip()
    # Only explicitly approved project-specific documents belong in the live RAG corpus.
    # General reference material may remain in the repository but is not indexed.
    scope_match = re.search(r"(?im)^-\s*\*\*RAG Scope:\*\*\s*(.+)$", text)
    if not scope_match or scope_match.group(1).strip().casefold() != "project-specific":
        return []

    status_match = re.search(r"(?im)^-\s*\*\*Status:\*\*\s*(.+)$", text)
    document_status = status_match.group(1).strip() if status_match else "unverified project document"
    sections: list[tuple[str, list[str]]] = []
    current_heading = title
    current_lines: list[str] = []
    seen_heading = False
    for line in text.splitlines():
        if line.startswith("#"):
            if seen_heading and current_lines:
                sections.append((current_heading, current_lines))
            heading_text = line.lstrip("#").strip() or title
            if line.startswith("# ") and title == path.stem.replace("-", " ").replace("_", " ").strip():
                title = heading_text
            current_heading = heading_text
            current_lines = []
            seen_heading = True
        elif seen_heading and not line.startswith((
            "- **Document ID:**",
            "- **Status:**",
            "- **Applies to:**",
            "- **Keywords:**",
            "- **RAG Scope:**",
        )):
            current_lines.append(line)
    if seen_heading and current_lines:
        sections.append((current_heading, current_lines))
    elif not seen_heading:
        sections.append((title, text.splitlines()))

    output: list[tuple[str, str, str, str]] = []
    for heading, lines in sections:
        body = "\n".join(lines).strip()
        if not body:
            continue
        paragraphs = re.split(r"\n\s*\n", body)
        chunk = ""
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            if len(chunk) + len(paragraph) + 2 > MAX_CHUNK_CHARS and chunk:
                output.append((title, heading, document_status, chunk))
                chunk = ""
            chunk = f"{chunk}\n\n{paragraph}".strip()
        if chunk:
            output.append((title, heading, document_status, chunk))
    return output

def search_knowledge(query: str, limit: int = DEFAULT_LIMIT) -> list[KnowledgeResult]:
    """Search local Markdown/TXT sections. Returns only grounded matches."""
    query = query.strip()
    if not query:
        return []
    terms = set(_tokens(query))
    if not terms:
        return []
    limit = max(1, min(int(limit), MAX_LIMIT))
    if not KNOWLEDGE_ROOT.is_dir():
        return []

    results: list[KnowledgeResult] = []
    for path in sorted(KNOWLEDGE_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
            continue
        if path.name.lower() == "readme.md":
            continue
        if any(part.startswith(".") for part in path.relative_to(KNOWLEDGE_ROOT).parts):
            continue
        relative_source = path.relative_to(KNOWLEDGE_ROOT.parent).as_posix()
        for title, heading, document_status, content in _read_sections(path):
            body_tokens = _tokens(content)
            token_set = set(body_tokens)
            matched = {
                term for term in terms
                if term in token_set
                or (len(term) >= 5 and any(token.startswith(term) or term.startswith(token) for token in token_set if len(token) >= 4))
            }
            if not matched:
                continue
            # A multiword question must match more than one content term. This
            # filters chunks that only mention a broad topic word such as "ticket".
            if len(terms) > 1 and len(matched) < 2:
                continue
            score = sum(body_tokens.count(term) for term in matched)
            score += 3 * len(matched)
            score += int(4 * len(matched) / len(terms))
            if any(term in path.name.casefold() for term in terms):
                score += 3
            if any(term in heading.casefold() for term in terms):
                score += 2
            excerpt = re.sub(r"\s+", " ", content).strip()
            if len(excerpt) > 420:
                excerpt = excerpt[:417].rsplit(" ", 1)[0] + "..."
            results.append({
                "title": title,
                "source": relative_source,
                "section": heading,
                "status": document_status,
                "excerpt": excerpt,
                "score": score,
                "content": content[:MAX_CHUNK_CHARS],
            })

    results.sort(key=lambda item: (-item["score"], item["source"], item["section"]))
    # Avoid returning multiple chunks from the same section.
    unique: list[KnowledgeResult] = []
    seen: set[tuple[str, str]] = set()
    for result in results:
        key = (result["source"], result["section"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(result)
        if len(unique) >= limit:
            break
    return unique
