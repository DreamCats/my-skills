---
name: byted-codebase
description: 字节码本MCP工具（已默认配置PSM: bytedance.mcp.codebase, Region: CN, Token: code_pat_UPByoMOUvKmqTforneex），提供简洁的命令行和Python接口，包含codebase特有工具使用示例和CN区域优化建议
type: domain
---

# 字节码本 MCP 工具（CN 区域 - 默认配置版）

## 默认配置说明

脚本已内置以下配置，无需每次指定：

- **PSM**: `bytedance.mcp.codebase`
- **Region**: `CN`（中国区域）
- **认证**: `Authorization=Bearer code_pat_UPByoMOUvKmqTforneex`

## 快速开始

### 1. 命令行使用（简洁版）

```bash
# 列出所有可用工具（无需参数）
.claude/skills/byted-logid/scripts/bytedance_mcp.py list-tools

# 调用码本搜索工具（简洁版）
.claude/skills/byted-logid/scripts/bytedance_mcp.py call --tool code_search --params '{
  "query": "useEffect hook",
  "limit": 10
}'

# 获取仓库信息
.claude/skills/byted-logid/scripts/bytedance_mcp.py call --tool repo_info --params '{
  "repo_name": "tiktok-backend"
}'
```

### 2. Python API 使用（默认配置）

```python
from bytedance_mcp import ByteDanceMCP

# 直接使用默认配置
mcp = ByteDanceMCP()  # 已内置CN区域配置

# 获取工具列表
tools = mcp.list_tools()
print(f"可用工具数量: {len(tools.get('result', []))}")

# 搜索代码
results = mcp.call_tool("code_search", {
    "query": "authentication middleware",
    "limit": 20
})
```

## 故障排除

### 1. 连接问题

```bash
# 测试连接
./bytedance_mcp.py list-tools

# 如果失败，检查网络
ping codebase.byted.org
```

### 2. 认证失败

```python
# 验证token有效性
def verify_token():
    try:
        mcp = ByteDanceMCP()
        result = mcp.list_tools()
        print("✅ Token有效")
        return True
    except RuntimeError as e:
        print(f"❌ 认证失败: {e}")
        print("请检查token: code_pat_UPByoMOUvKmqTforneex")
        return False
```

### 3. 查询无结果

```bash
# 检查查询参数
./bytedance_mcp.py call --tool code_search --params '{
  "query": "your_search_term",
  "limit": 10,
  "path_pattern": "**/*.py"  # 尝试移除路径限制
}'

# 放宽搜索条件
./bytedance_mcp.py call --tool code_search --params '{
  "query": "class User",
  "language": "python",
  "limit": 5
}'
```

## 实用脚本示例

### 每日代码统计

```bash
#!/bin/bash
# daily_stats.sh - 每日代码统计

echo "=== 今日代码统计 ==="

# 获取昨日提交的MR
./bytedance_mcp.py call --tool merge_requests --params '{
  "state": "merged",
  "updated_after": "$(date -d yesterday +%Y-%m-%d)"
}' | jq '.result | length' | echo "昨日合并MR数: $(cat)"

# 搜索昨日新增的代码
./bytedance_mcp.py call --tool code_search --params '{
  "query": "$(date +%Y-%m-%d)",
  "time_range": "1day",
  "limit": 5
}' | jq '.result[].path' | echo "昨日更新文件: $(cat | wc -l) 个"
```

### 代码质量检查

```python
#!/usr/bin/env python3
# quality_check.py - 代码质量检查

from bytedance_mcp import ByteDanceMCP
import json

def check_error_handling(repo_name):
    """检查错误处理代码"""
    mcp = ByteDanceMCP()

    # 搜索try-catch模式
    results = mcp.call_tool("code_search", {
        "query": "try { catch (",
        "repo": repo_name,
        "language": "typescript",
        "limit": 100
    })

    files_with_errors = {}
    for result in results.get("result", []):
        filepath = result["path"]

        # 检查是否有日志记录
        log_check = mcp.call_tool("code_search", {
            "query": "console.error logger.error",
            "repo": repo_name,
            "path_pattern": filepath,
            "limit": 1
        })

        if not log_check.get("result"):
            files_with_errors[filepath] = "缺少错误日志记录"

    return files_with_errors

# 使用示例
issues = check_error_handling("frontend-monorepo")
for file, issue in issues.items():
    print(f"⚠️  {file}: {issue}")
```

## 相关资源

- [bytedance_mcp.py 源码](./scripts/bytedance_mcp.py)
- [Codebase 工具文档](https://codebase.byted.org/docs/tools)
- [CN 区域最佳实践](./docs/cn-best-practices.md)
