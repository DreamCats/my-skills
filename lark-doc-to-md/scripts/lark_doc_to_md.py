#!/usr/bin/env python3
import argparse
import json
import os

from doc_utils import extract_doc_id
from lark_cli import get_blocks
from renderer import LarkDocRenderer

DEFAULT_LANGUAGE_MAP = {"1": "text"}

try:
    from language_map import LANGUAGE_MAP
except Exception:
    LANGUAGE_MAP = {}


def load_language_map(path):
    mapping = dict(DEFAULT_LANGUAGE_MAP)
    mapping.update(LANGUAGE_MAP)
    if path:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        for k, v in data.items():
            mapping[str(k)] = v
    return mapping


def main():
    parser = argparse.ArgumentParser(description="Export Lark doc to Markdown")
    parser.add_argument("--doc-id", help="Document ID")
    parser.add_argument("--doc-url", help="Document URL")
    parser.add_argument("--out", required=True, help="Output markdown path")
    parser.add_argument("--assets", help="Assets directory (default: <out_dir>/assets)")
    parser.add_argument("--language-map", help="JSON mapping for code language")
    parser.add_argument("--no-download", action="store_true", help="Skip downloading assets")
    args = parser.parse_args()

    doc_id = extract_doc_id(args.doc_id, args.doc_url)
    out_path = os.path.abspath(args.out)
    out_dir = os.path.dirname(out_path) or os.getcwd()
    assets_dir = args.assets or os.path.join(out_dir, "assets")
    assets_dir = os.path.abspath(assets_dir)
    assets_rel = os.path.relpath(assets_dir, out_dir)

    language_map = load_language_map(args.language_map)

    data = get_blocks(doc_id)
    items = data.get("items", [])

    renderer = LarkDocRenderer(
        items=items,
        doc_id=doc_id,
        assets_dir=assets_dir,
        assets_rel=assets_rel,
        language_map=language_map,
        download_assets=not args.no_download,
    )
    markdown = renderer.render()

    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(markdown)


if __name__ == "__main__":
    main()
