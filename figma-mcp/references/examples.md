# Figma MCP 示例

以下示例基于当前可用工具：`get_figma_data` 和 `download_figma_images`。

## 1. 拉取文件基础信息（get_figma_data）

仅提供 fileKey：

```bash
python3 scripts/figma_mcp.py call \
  --name get_figma_data \
  --args '{"fileKey":"AbCdEf123456"}' \
  --pretty
```

指定 nodeId（通常来自 URL 的 node-id 参数）：

```bash
python3 scripts/figma_mcp.py call \
  --name get_figma_data \
  --args '{"fileKey":"AbCdEf123456","nodeId":"1234:5678"}' \
  --pretty
```

注意：`depth` 为可选且官方建议不要随意使用，除非用户明确要求深度遍历。

## 2. 下载图片（download_figma_images）

示例使用参数文件方式，避免命令行过长。

`/tmp/figma_images.json` 示例：

```json
{
  "fileKey": "AbCdEf123456",
  "localPath": "/Users/bytedance/.figma_mcp/assets",
  "nodes": [
    {
      "nodeId": "1234:5678",
      "fileName": "icon_login.svg"
    },
    {
      "nodeId": "2345:6789",
      "imageRef": "123abc456def",
      "fileName": "hero_banner.png",
      "needsCropping": true,
      "cropTransform": [[1, 0, 0], [0, 1, 0]],
      "requiresImageDimensions": true,
      "filenameSuffix": "v1"
    }
  ],
  "pngScale": 2
}
```

执行命令：

```bash
python3 scripts/figma_mcp.py call \
  --name download_figma_images \
  --args-file /tmp/figma_images.json \
  --pretty
```

说明：
- `fileKey` 来自 Figma URL 的 `/file/<fileKey>/` 或 `/design/<fileKey>/`。
- `nodeId` 来自 URL 的 `node-id` 参数。
- `imageRef` 仅在节点包含位图填充时使用，下载 SVG 时可省略。
- `localPath` 必须是绝对路径，脚本会自动创建目录。

## 3. 通用排查

- 提示缺少参数：先看 `inputSchema.required` 字段。
- 传参格式报错：检查 JSON 是否有效，或用 `--args-file`。
- 需要临时更换密钥：
  `FIGMA_API_KEY=xxx python3 scripts/figma_mcp.py ...`
