# add-permission 命令使用说明

## 功能

为云文档添加协作者权限

## 基本用法

```bash
lark-cli add-permission <TOKEN> --doc-type <TYPE> --member-type <MTYPE> --member-id <ID> --perm <PERM> [选项]
```

## 必需参数

- `TOKEN`: 云文档 token
- `--doc-type <TYPE>`: 云文档类型
  - 支持类型：`doc`、`sheet`、`file`、`wiki`、`bitable`、`docx`、`folder`、`mindnote`、`minutes`、`slides`
- `--member-type <MTYPE>`: 协作者 ID 类型
  - 支持类型：`email`、`openid`、`unionid`、`openchat`、`opendepartmentid`、`userid`、`groupid`、`wikispaceid`
- `--member-id <ID>`: 协作者 ID
- `--perm <PERM>`: 权限角色
  - 支持角色：`view`（查看）、`edit`（编辑）、`full_access`（完全访问）

## 可选选项

- `--perm-type <PTYPE>`: 权限角色类型（仅知识库文档有效）
  - 支持类型：`container`（默认）、`single_page`
- `--collaborator-type <CTYPE>`: 协作者类型
  - 支持类型：`user`（默认）、`chat`、`department`、`group`、`wiki_space_member`、`wiki_space_viewer`、`wiki_space_editor`
- `--notification`: 添加权限后通知对方
- `-v, --verbose`: 详细输出模式
- `--format <FORMAT>`: 输出格式，支持 `text` 或 `json`（默认: json）

## 示例

### 基本权限添加

```bash
# 给用户添加查看权限
lark-cli add-permission doc_token123 \
  --doc-type docx \
  --member-type email \
  --member-id user@example.com \
  --perm view

# 给用户添加编辑权限
lark-cli add-permission doc_token123 \
  --doc-type docx \
  --member-type email \
  --member-id user@example.com \
  --perm edit
```

### 知识库文档权限

```bash
# 给知识库添加成员
lark-cli add-permission wiki_token123 \
  --doc-type wiki \
  --member-type email \
  --member-id user@example.com \
  --perm full_access \
  --perm-type container
```

### 群组权限

```bash
# 给群组添加查看权限
lark-cli add-permission doc_token123 \
  --doc-type docx \
  --member-type groupid \
  --member-id group_123 \
  --perm view \
  --collaborator-type group
```

### 带通知的权限添加

```bash
# 添加权限并通知对方
lark-cli add-permission doc_token123 \
  --doc-type docx \
  --member-type email \
  --member-id user@example.com \
  --perm edit \
  --notification
```

## 权限级别说明

- **view**: 只能查看文档，不能编辑
- **edit**: 可以编辑文档内容
- **full_access**: 完全访问权限，包括删除和分享

## 常见用途

1. 团队协作文档共享
2. 项目文档权限管理
3. 知识库成员管理
4. 跨部门文档共享
