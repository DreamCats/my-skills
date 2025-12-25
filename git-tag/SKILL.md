---
name: git-tag
description: 通过检查最新 tag 和最近的 git 日志来创建 git 发布 tag，提出版本总结和 tag 消息，然后选择性地推送到远程。（Create git release tags by inspecting the latest tag and recent git log, proposing a version bump and tag message, then optionally pushing to remote.）
metadata:
  short-description: Create release tags from git log
---

# Git Tag

当用户要创建/更新 Git tag、生成发布标签、或询问如何打 tag 并推送时使用本技能。

## 工作流

1. 校验仓库状态

- 确认在 Git 仓库内：`git rev-parse --is-inside-work-tree`
- 查看工作区是否干净：`git status --porcelain`
- 若存在未提交改动，提示风险并询问是否继续

2. 获取最近一次 tag

- 首选：`git describe --tags --abbrev=0`
- 备选：`git tag --sort=-creatordate | head -n 1`
- 若没有任何 tag，明确询问起始版本（如 `v0.1.0` 或 `0.1.0`）
- 保持与既有 tag 前缀一致（有 `v` 就继续用 `v`）

3. 汇总最近改动

- 有 tag 时：`git log <last_tag>..HEAD --pretty=format:'%h %s'`
- 无 tag 时：`git log --pretty=format:'%h %s'`（必要时限制数量）
- 生成简短变更列表，供用户确认
- 如需自动生成 tag message，使用脚本：`python3 scripts/gen_tag_message.py`

4. 推断新版本号（可被用户覆盖）

- 参考语义化版本：
  - **重大变化**：提交信息包含 `BREAKING` / `!:` / 明确不兼容
  - **新功能**：含 `feat` / `feature`
  - **修复/微调**：含 `fix` / `perf` / `chore` 等
- 若无法判断，默认小版本或补丁版本，并向用户确认

5. 生成 tag 内容并创建 annotated tag

- 建议用多行 tag message：
  - `Release vX.Y.Z` + 变更列表
- 用文件写入更稳妥：
  - 自动生成：`python3 scripts/gen_tag_message.py --tag vX.Y.Z --output /tmp/tagmsg.txt`
  - 或手动：`cat <<'EOF' > /tmp/tagmsg.txt`（内容）
  - `git tag -a <tag> -F /tmp/tagmsg.txt`
- 若 tag 已存在，询问是改名还是换一个版本号

6. 询问是否推送远端

- 仅在用户确认后执行：
  - `git push origin <tag>`
- 如需推送全部新 tag，再用：`git push --tags`

## 关键注意点

- 若远端可能有新 tag，先 `git fetch --tags`
- 不自动删除或重写 tag；如需修改必须先询问用户
- 输出应包含：
  - 最近 tag、变更摘要、建议版本号、最终 tag 内容、是否推送

## 脚本：自动生成 tag message

位置：`scripts/gen_tag_message.py`

常用示例：

- `python3 scripts/gen_tag_message.py --tag v1.2.3 --output /tmp/tagmsg.txt`
- `python3 scripts/gen_tag_message.py --since-tag v1.2.0 --max 50`

参数说明：

- `--tag`：用于标题行 `Release <tag>`（可选）
- `--since-tag`：指定基准 tag，不传则自动取最近 tag
- `--max`：限制提交数量
- `--output`：输出到文件（默认 stdout）
