import json
import os
from html import escape as html_escape
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from lark_cli import get_user_info, run_cmd
from md_utils import detect_image_ext, escape_md_table_cell, text_from_elements, IMAGE_EXTS


class LarkDocRenderer:
    def __init__(self, items, doc_id, assets_dir, assets_rel, language_map, download_assets):
        self.items = items
        self.doc_id = doc_id
        self.assets_dir = assets_dir
        self.assets_rel = assets_rel
        self.language_map = language_map
        self.download_assets = download_assets
        self.index = {it["block_id"]: it for it in items}
        self.user_cache = {}

    def find_root(self):
        for it in self.items:
            if it.get("block_type") == 1 and not it.get("parent_id"):
                return it
        return self.index.get(self.doc_id)

    def render(self):
        root = self.find_root()
        if not root:
            return ""
        lines = []
        title = self.get_page_title(root)
        if title:
            lines.append(f"# {title}")
            lines.append("")
        children = root.get("children", [])
        lines.extend(self.render_children(children, list_level=0))
        content = "\n".join(lines).rstrip() + "\n"
        return content

    def get_page_title(self, root):
        page = root.get("page") or {}
        title = text_from_elements(page.get("elements", []), self.resolve_mention_user)
        title = title.strip()
        if not title:
            return ""
        if root.get("children"):
            first_child = self.index.get(root["children"][0])
            if first_child and first_child.get("block_type") in range(3, 12):
                level = first_child.get("block_type") - 2
                key = f"heading{level}"
                heading = first_child.get(key, {})
                text = text_from_elements(heading.get("elements", []), self.resolve_mention_user)
                if text.strip() == title:
                    return ""
        return title

    def resolve_mention_user(self, user_id):
        if user_id in self.user_cache:
            return self.user_cache[user_id]
        user_id_type = "user_id"
        if user_id.startswith("ou_"):
            user_id_type = "open_id"
        elif user_id.startswith("on_"):
            user_id_type = "union_id"
        try:
            info = get_user_info(user_id, user_id_type=user_id_type)
        except Exception:
            result = f"@{user_id}"
            self.user_cache[user_id] = result
            return result
        name = info.get("name") or info.get("en_name") or user_id
        avatar = ""
        avatar_info = info.get("avatar") or {}
        if isinstance(avatar_info, dict):
            avatar = avatar_info.get("avatar_72") or avatar_info.get("avatar_origin") or ""
            avatar = self.adjust_avatar_size(avatar)
        if avatar:
            result = f"![{name}]({avatar}) {name}"
        else:
            result = f"@{name}"
        self.user_cache[user_id] = result
        return result

    def adjust_avatar_size(self, url):
        if not url:
            return url
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        if "image_size" in query:
            query["image_size"] = ["16x16"]
            new_query = urlencode(query, doseq=True)
            return urlunparse(
                (parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment)
            )
        return url

    def render_children(self, child_ids, list_level):
        lines = []
        for idx, cid in enumerate(child_ids):
            block = self.index.get(cid)
            if not block:
                continue
            block_lines, block_type = self.render_block(block, list_level)
            if not block_lines:
                continue
            lines.extend(block_lines)
            if idx < len(child_ids) - 1:
                next_block = self.index.get(child_ids[idx + 1])
                next_type = next_block.get("block_type") if next_block else None
                if self.should_blank_after(block_type, list_level):
                    lines.append("")
                elif list_level == 0 and block_type in (12, 13, 17) and next_type not in (12, 13, 17):
                    lines.append("")
        return lines

    def should_blank_after(self, block_type, list_level):
        if list_level > 0:
            return False
        if block_type in (12, 13, 17):
            return False
        return True

    def render_block(self, block, list_level):
        block_type = block.get("block_type")
        if block_type == 2:
            text = text_from_elements(block["text"].get("elements", []), self.resolve_mention_user)
            return [text], block_type
        if block_type in range(3, 12):
            level = block_type - 2
            key = f"heading{level}"
            heading = block.get(key, {})
            text = text_from_elements(heading.get("elements", []), self.resolve_mention_user)
            return [f"{'#' * level} {text}"], block_type
        if block_type == 12:
            text = text_from_elements(block["bullet"].get("elements", []), self.resolve_mention_user)
            indent = "    " * list_level
            lines = [f"{indent}- {text}"]
            children = block.get("children", [])
            if children:
                lines.extend(self.render_children(children, list_level + 1))
            return lines, block_type
        if block_type == 13:
            text = text_from_elements(block["ordered"].get("elements", []), self.resolve_mention_user)
            seq = block["ordered"].get("style", {}).get("sequence")
            index = seq if seq and str(seq).isdigit() else "1"
            indent = "    " * list_level
            lines = [f"{indent}{index}. {text}"]
            children = block.get("children", [])
            if children:
                lines.extend(self.render_children(children, list_level + 1))
            return lines, block_type
        if block_type == 14:
            code = block["code"]
            text = text_from_elements(code.get("elements", []), self.resolve_mention_user)
            lang_id = code.get("style", {}).get("language")
            lang = self.language_map.get(str(lang_id), "text")
            lines = [f"```{lang}", text.rstrip("\n"), "```"]
            return lines, block_type
        if block_type == 15:
            text = text_from_elements(block["quote"].get("elements", []), self.resolve_mention_user)
            q_lines = text.split("\n") if text else [""]
            lines = [f"> {line}" for line in q_lines]
            return lines, block_type
        if block_type == 17:
            todo = block["todo"]
            text = text_from_elements(todo.get("elements", []), self.resolve_mention_user)
            done = todo.get("style", {}).get("done", False)
            check = "x" if done else " "
            indent = "    " * list_level
            lines = [f"{indent}- [{check}] {text}"]
            children = block.get("children", [])
            if children:
                lines.extend(self.render_children(children, list_level + 1))
            return lines, block_type
        if block_type == 19:
            content_lines = self.render_children(block.get("children", []), list_level=0)
            if not content_lines:
                return ["> **提示**"], block_type
            first = content_lines[0]
            lines = [f"> **提示** {first}" if first else "> **提示**"]
            for line in content_lines[1:]:
                lines.append(f"> {line}")
            return lines, block_type
        if block_type == 22:
            return ["---"], block_type
        if block_type == 27:
            token = block["image"].get("token")
            if token:
                rel_path = self.download_media(token)
                return [f"![]({rel_path})"], block_type
            return [], block_type
        if block_type == 31:
            lines = self.render_table(block)
            return lines, block_type
        if block_type == 43:
            token = block["board"].get("token")
            if token:
                rel_path = self.download_board(token)
                return [f"![]({rel_path})"], block_type
            return [], block_type
        if block_type == 21:
            token = block.get("diagram", {}).get("token")
            if token:
                rel_path = self.download_board(token)
                return [f"![]({rel_path})"], block_type
            return [], block_type
        if block_type in (24, 25, 34):
            children = block.get("children", [])
            return self.render_children(children, list_level), block_type
        return [], block_type

    def download_media(self, token):
        for ext in IMAGE_EXTS:
            candidate = os.path.join(self.assets_dir, token + ext)
            if os.path.exists(candidate):
                return os.path.join(self.assets_rel, token + ext)
        abs_path = os.path.join(self.assets_dir, token)
        if self.download_assets and not os.path.exists(abs_path):
            os.makedirs(self.assets_dir, exist_ok=True)
            cmd = [
                "lark-cli",
                "download-media",
                token,
                abs_path,
                "--extra",
                json.dumps({"drive_route_token": self.doc_id}),
            ]
            run_cmd(cmd)
        ext = detect_image_ext(abs_path)
        if ext:
            final_path = abs_path + ext
            if not os.path.exists(final_path) and os.path.exists(abs_path):
                os.rename(abs_path, final_path)
            elif os.path.exists(abs_path):
                os.remove(abs_path)
            return os.path.join(self.assets_rel, token + ext)
        return os.path.join(self.assets_rel, token)

    def download_board(self, token):
        filename = f"{token}.png"
        abs_path = os.path.join(self.assets_dir, filename)
        if self.download_assets and not os.path.exists(abs_path):
            os.makedirs(self.assets_dir, exist_ok=True)
            cmd = ["lark-cli", "get-board-image", token, abs_path]
            run_cmd(cmd)
        return os.path.join(self.assets_rel, filename)

    def render_table(self, block):
        table = block["table"]
        prop = table.get("property", {})
        rows = prop.get("row_size", 0)
        cols = prop.get("column_size", 0)
        cells = table.get("cells", [])
        merge_info = prop.get("merge_info", [])
        complex_table = any(
            (info.get("row_span", 1) > 1 or info.get("col_span", 1) > 1)
            for info in merge_info
        )
        matrix = []
        for idx, cell_id in enumerate(cells):
            r = idx // cols if cols else 0
            c = idx % cols if cols else 0
            while len(matrix) <= r:
                matrix.append([None] * cols)
            span = merge_info[idx] if idx < len(merge_info) else {"row_span": 1, "col_span": 1}
            matrix[r][c] = (cell_id, span)
        if complex_table:
            return self.render_html_table(matrix, rows, cols)
        return self.render_md_table(matrix, rows, cols)

    def render_md_table(self, matrix, rows, cols):
        table_rows = []
        for r in range(rows):
            row_cells = []
            for c in range(cols):
                cell = matrix[r][c] if r < len(matrix) else None
                cell_id = cell[0] if cell else None
                text = self.get_cell_text(cell_id) if cell_id else ""
                row_cells.append(escape_md_table_cell(text))
            table_rows.append(row_cells)
        if not table_rows:
            return []
        header = "| " + " | ".join(table_rows[0]) + " |"
        divider = "| " + " | ".join(["---"] * cols) + " |"
        body = ["| " + " | ".join(row) + " |" for row in table_rows[1:]]
        return [header, divider] + body

    def render_html_table(self, matrix, rows, cols):
        skip = [[False] * cols for _ in range(rows)]
        lines = ["<table>"]
        for r in range(rows):
            lines.append("  <tr>")
            for c in range(cols):
                if skip[r][c]:
                    continue
                cell = matrix[r][c] if r < len(matrix) else None
                cell_id = cell[0] if cell else None
                span = cell[1] if cell else {"row_span": 1, "col_span": 1}
                row_span = max(int(span.get("row_span", 1)), 1)
                col_span = max(int(span.get("col_span", 1)), 1)
                for dr in range(row_span):
                    for dc in range(col_span):
                        if dr == 0 and dc == 0:
                            continue
                        if r + dr < rows and c + dc < cols:
                            skip[r + dr][c + dc] = True
                text = self.get_cell_text(cell_id) if cell_id else ""
                text = html_escape(text).replace("\n", "<br>")
                attrs = []
                if row_span > 1:
                    attrs.append(f"rowspan=\"{row_span}\"")
                if col_span > 1:
                    attrs.append(f"colspan=\"{col_span}\"")
                attr_str = " " + " ".join(attrs) if attrs else ""
                lines.append(f"    <td{attr_str}>{text}</td>")
            lines.append("  </tr>")
        lines.append("</table>")
        return lines

    def get_cell_text(self, cell_id):
        if not cell_id:
            return ""
        cell = self.index.get(cell_id, {})
        parts = []
        for cid in cell.get("children", []):
            child = self.index.get(cid)
            if not child:
                continue
            bt = child.get("block_type")
            if bt == 2:
                parts.append(text_from_elements(child["text"].get("elements", []), self.resolve_mention_user))
            elif bt in range(3, 12):
                level = bt - 2
                key = f"heading{level}"
                parts.append(text_from_elements(child.get(key, {}).get("elements", []), self.resolve_mention_user))
            elif bt == 12:
                parts.append(text_from_elements(child["bullet"].get("elements", []), self.resolve_mention_user))
            elif bt == 13:
                parts.append(text_from_elements(child["ordered"].get("elements", []), self.resolve_mention_user))
            elif bt == 14:
                parts.append(text_from_elements(child["code"].get("elements", []), self.resolve_mention_user))
            elif bt == 15:
                parts.append(text_from_elements(child["quote"].get("elements", []), self.resolve_mention_user))
            elif bt == 17:
                parts.append(text_from_elements(child["todo"].get("elements", []), self.resolve_mention_user))
        return "\n".join([p for p in parts if p])
