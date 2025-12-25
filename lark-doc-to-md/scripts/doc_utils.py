import re
from urllib.parse import parse_qs, urlparse

from lark_cli import resolve_wiki_node


def extract_doc_id(doc_id, doc_url):
    if doc_id:
        return doc_id
    if not doc_url:
        raise ValueError("doc_id or doc_url is required")
    parsed = urlparse(doc_url)
    query = parse_qs(parsed.query)
    for key in ("doc_id", "docId", "document_id"):
        if key in query and query[key]:
            return query[key][0]
    segments = [seg for seg in parsed.path.split("/") if seg]
    for idx, seg in enumerate(segments):
        if seg == "wiki" and idx + 1 < len(segments):
            return resolve_wiki_node(segments[idx + 1])
    for idx, seg in enumerate(segments):
        if seg in ("docx", "docs", "doc", "wiki") and idx + 1 < len(segments):
            return segments[idx + 1]
    match = re.search(r"[A-Za-z0-9]{20,}", doc_url)
    if match:
        if "/wiki/" in parsed.path:
            return resolve_wiki_node(match.group(0))
        return match.group(0)
    raise ValueError(f"Unable to extract doc_id from url: {doc_url}")
