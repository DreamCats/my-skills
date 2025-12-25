---
name: lark-doc-to-md
description: 将飞书云文档导出为 Markdown，基于 lark-cli get-blocks 解析块结构，下载图片/画板缩略图到 assets/ 并生成相对路径引用。
---

# Lark Doc to Markdown

## 概览

从飞书云文档导出 Markdown：
- 通过 `get-blocks` 拉取块结构（保持 children 顺序）。
- 解析块类型并转换为 Markdown。
- 图片与画板缩略图下载到 `assets/`，MD 中引用相对路径。

## 依赖命令

- `lark-cli get-blocks <DOCUMENT_ID> --all`
- `lark-cli get-node <WIKI_TOKEN>`（当 doc_url 为 /wiki/ 链接时）
- `lark-cli get-user-info <USER_ID>`（当解析 @用户 时）
- `lark-cli download-media <FILE_TOKEN> <OUTPUT_PATH>`
- `lark-cli get-board-image <WHITEBOARD_ID> <OUTPUT_PATH>`

## 脚本用法

```bash
# 先进入技能目录（重要）
cd xxx/skills/lark-doc-to-md

# 使用 doc_id 导出
python3 scripts/lark_doc_to_md.py --doc-id <DOC_ID> --out ./output.md

# 使用 doc_url 导出（自动解析 doc_id；/wiki/ 链接会自动调用 get-node）
python3 scripts/lark_doc_to_md.py --doc-url "https://bytedance.larkoffice.com/docx/<DOC_ID>" --out ./output.md

# 自定义 assets 目录
python3 scripts/lark_doc_to_md.py --doc-id <DOC_ID> --out ./output.md --assets ./assets

# 传入语言映射 JSON（可选）
python3 scripts/lark_doc_to_md.py --doc-id <DOC_ID> --out ./output.md --language-map ./language_map.json
```

## 转换规则（核心）

- **文档标题**：page 块的 title 会输出为首行一级标题（如首个子块已是同名标题则不重复）。
- **标题/正文/列表/引用/代码**：按块类型转换为标准 Markdown。
- **@用户**：解析为 `@名字`；如失败则回退为 `@user_id`。
- **Callout**：转为 Markdown 引用块，首行带 `**提示**`。
- **图片**：`download-media` 下载到 `assets/`，文件名使用 token，Markdown 引用相对路径。
- **画板/流程图/图表**：`get-board-image` 下载缩略图到 `assets/`，Markdown 引用相对路径。
- **表格**：
  - 简单表格 → Markdown 表格
  - 复杂表格（`row_span/col_span > 1`）→ HTML table
  - 表格内图片使用 `<img>`，默认 `max-width:160px` 等比例缩放

## 参考文档

- 块结构参考：`references/飞书文档块结构.md`

## 语言映射

代码块语言由 `code.style.language` 的数值决定，脚本内置映射位于 `scripts/language_map.py`；如需覆盖，可传入 `--language-map` JSON。

语言枚举表参考：`references/language.md`（仅供人工查阅）

JSON 示例：

```json
{
  "28": "json",
  "1": "text"
}
```
