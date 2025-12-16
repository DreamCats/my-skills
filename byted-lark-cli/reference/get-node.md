# get-node 命令使用说明

## 功能
获取知识空间节点信息

## 基本用法
```bash
lark-cli get-node <TOKEN> [选项]
```

## 参数
- `TOKEN` (必需): 知识空间节点 token

## 选项
- `--obj-type <TYPE>`: 知识空间节点类型（可选）
- `-v, --verbose`: 详细输出模式
- `--format <FORMAT>`: 输出格式，支持 `text` 或 `json`（默认: json）

## 示例

### 基本查询
```bash
# 获取节点信息（JSON 格式输出）
lark-cli get-node wiki_space_token

# 获取节点信息（文本格式输出）
lark-cli get-node wiki_space_token --format text
```

### 指定节点类型
```bash
# 指定节点类型为 origin
lark-cli get-node wiki_space_token --obj-type origin
```

### 调试模式
```bash
# 启用详细日志输出
lark-cli -v get-node wiki_space_token
```

## 返回字段说明
- `node_token`: 节点 token
- `obj_type`: 节点类型
- `node_type`: 节点类型（wiki/mindnote/sheet 等）
- `title`: 节点标题
- `obj_token`: 对象 token
- `parent_node_token`: 父节点 token
- `has_child`: 是否有子节点
- `created_time`: 创建时间
- `modified_time`: 修改时间

## 常见用途
1. 获取知识库结构信息
2. 验证节点是否存在
3. 获取节点的元数据信息
4. 构建知识库目录树