# lark-cli add-permission 参考

## 命令概要

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

## 参数枚举

- doc-type（云文档类型）
  - doc、sheet、file、wiki、bitable、docx、folder、mindnote、minutes、slides
- member-type（协作者 ID 类型）
  - email、openid、unionid、openchat、opendepartmentid、userid、groupid、wikispaceid
- perm（权限角色）
  - view、edit、full_access
- perm-type（仅知识库文档有效）
  - container、single_page
- collaborator-type（协作者类型）
  - user、chat、department、group、wiki_space_member、wiki_space_viewer、wiki_space_editor
- notification
  - 添加权限后是否通知对方，传入即生效

## 输入检查清单

- TOKEN 与 doc-type 是否匹配（例如 docx_xxx 用 docx）。
- member-type 与 member-id 是否一致（例如 openid + ou_xxx）。
- wiki 场景时，是否需要指定 perm-type。
- 是否需要通知对方（--notification）。

## 示例

**按 email 添加用户为可编辑协作者：**

```bash
lark-cli add-permission \
  --doc-type docx \
  --member-type email \
  --member-id user@example.com \
  --perm edit \
  docx_xxxxxx
```

**按部门 ID 添加查看权限：**

```bash
lark-cli add-permission \
  --doc-type sheet \
  --member-type opendepartmentid \
  --member-id od_xxxxxx \
  --perm view \
  sht_xxxxxx
```

**wiki 文档添加空间成员权限（container）：**

```bash
lark-cli add-permission \
  --doc-type wiki \
  --member-type wikispaceid \
  --member-id ws_xxxxxx \
  --collaborator-type wiki_space_member \
  --perm view \
  --perm-type container \
  wiki_xxxxxx
```
