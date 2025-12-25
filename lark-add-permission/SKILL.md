---
name: lark-add-permission
description: 使用 lark-cli add-permission 为飞书云文档添加协作者权限；适用于为用户/群/部门/群组/知识空间成员授予查看、编辑或管理权限。
---

# lark-add-permission

## 概述

为飞书云文档添加协作者权限，输出可直接执行的 `lark-cli add-permission` 命令，并在必要时提示用户补齐文档/协作者/权限参数。

## 适用场景

- 需要给飞书文档添加协作者权限（单次或批量脚本化）。
- 需要明确协作者类型、权限级别、是否通知对方。

## 工作流

1. 收集文档信息：`token`、`doc-type`（如 docx、sheet、wiki 等）。
2. 收集协作者信息：`member-type` + `member-id`，以及可选的 `collaborator-type`。
3. 选择权限：`perm`（view/edit/full_access），wiki 场景可指定 `perm-type`。
4. 组装并执行命令，可选 `--notification`。

## 命令模板

```bash
lark-cli add-permission \
  --doc-type <DOC_TYPE> \
  --member-type <MEMBER_TYPE> \
  --member-id <MEMBER_ID> \
  --perm <PERM> \
  <TOKEN> \
  [--perm-type <PERM_TYPE>] \
  [--collaborator-type <COLLABORATOR_TYPE>] \
  [--notification]
```

## 常见示例

**给 docx 文档添加用户查看权限（按 openid）：**

```bash
lark-cli add-permission \
  --doc-type docx \
  --member-type openid \
  --member-id ou_xxxxxx \
  --perm view \
  docx_xxxxxx
```

**给 sheet 添加群组编辑权限（按 groupid，并通知）：**

```bash
lark-cli add-permission \
  --doc-type sheet \
  --member-type groupid \
  --member-id gc_xxxxxx \
  --perm edit \
  --notification \
  sht_xxxxxx
```

**给 wiki 文档添加成员权限（指定 container）：**

```bash
lark-cli add-permission \
  --doc-type wiki \
  --member-type userid \
  --member-id 123456 \
  --collaborator-type wiki_space_member \
  --perm view \
  --perm-type container \
  wiki_xxxxxx
```

## 参考

需要完整参数枚举与约束时，读取 `references/add_permission.md`。
