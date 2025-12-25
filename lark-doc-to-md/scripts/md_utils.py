import os
from urllib.parse import unquote

IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"]


def safe_unquote(url):
    if not url:
        return ""
    try:
        return unquote(url)
    except Exception:
        return url


def apply_text_style(text, style):
    styled = text
    if style.get("inline_code"):
        styled = f"`{styled}`"
    if style.get("bold"):
        styled = f"**{styled}**"
    if style.get("italic"):
        styled = f"*{styled}*"
    if style.get("underline"):
        styled = f"<u>{styled}</u>"
    if style.get("strikethrough"):
        styled = f"~~{styled}~~"
    link = style.get("link") or {}
    url = safe_unquote(link.get("url", "")) if isinstance(link, dict) else ""
    if url:
        styled = f"[{styled}]({url})"
    return styled


def text_from_elements(elements, mention_resolver=None):
    parts = []
    for el in elements:
        if "text_run" in el:
            tr = el["text_run"]
            content = tr.get("content", "")
            style = tr.get("text_element_style", {}) or {}
            text = apply_text_style(content, style)
            parts.append(text)
        elif "mention_user" in el:
            user_id = el["mention_user"].get("user_id", "")
            if mention_resolver and user_id:
                parts.append(mention_resolver(user_id))
            else:
                parts.append(f"@{user_id}" if user_id else "@user")
        elif "mention_doc" in el:
            doc = el["mention_doc"]
            title = doc.get("title") or "doc"
            url = safe_unquote(doc.get("url", ""))
            parts.append(f"[{title}]({url})" if url else title)
        elif "equation" in el:
            eq = el["equation"].get("content", "")
            parts.append(f"${eq}$")
        elif "file" in el:
            token = el["file"].get("file_token", "")
            parts.append(f"`file:{token}`" if token else "`file`")
        elif "inline_block" in el:
            parts.append("`inline_block`")
        else:
            parts.append("")
    return "".join(parts)


def escape_md_table_cell(text):
    if text is None:
        return ""
    value = text.replace("|", "\\|")
    value = value.replace("\n", "<br>")
    return value


def detect_image_ext(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as fh:
        header = fh.read(32)
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if header.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if header.startswith(b"GIF87a") or header.startswith(b"GIF89a"):
        return ".gif"
    if header.startswith(b"RIFF") and b"WEBP" in header[8:16]:
        return ".webp"
    if header.startswith(b"BM"):
        return ".bmp"
    if header.lstrip().startswith(b"<?xml") or header.lstrip().startswith(b"<svg"):
        return ".svg"
    return ""
