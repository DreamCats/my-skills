# Claude Code Skills Collection

A comprehensive collection of specialized skills for extending Claude Code's capabilities across various domains including development workflows, communication tools, and system integrations.

## Overview

This repository contains a curated set of skills that transform Claude from a general-purpose AI into specialized agents equipped with domain-specific knowledge, tools, and workflows. Each skill is self-contained and can be used independently or in combination with others.

## 📋 技能总览

| 技能类别 | 技能名称 | 主要功能 | 语言 |
|---------|---------|---------|------|
| **核心开发** | skill-developer | 技能开发元框架 | Python |
| **核心开发** | skill-creator | 技能创建工具 | Python |
| **MCP集成** | mcp-builder | MCP服务器构建指南 | Python/TypeScript |
| **MCP集成** | byted-codebase | 字节码本MCP集成 | Python |
| **MCP集成** | chrome-mcp | Chrome浏览器MCP集成 | Python |
| **MCP集成** | github-mcp | GitHub MCP集成 | Python |
| **飞书协作** | byted-lark-cli | 飞书CLI工具 | Python |
| **飞书协作** | lark-send-msg | 飞书消息发送 | Python |
| **飞书协作** | lark-md-to-doc | Markdown转飞书文档 | Python |
| **飞书协作** | lark-doc-to-md | 飞书文档转Markdown | Python |
| **字节工具** | byted-logid | 字节日志ID工具 | Python |
| **开发工具** | git-tag | Git标签管理 | Bash |
| **开发工具** | review-go | Go代码审查 | Python |
| **图像工具** | ark-generate-image | 图像生成 | Python |
| **图像工具** | polish-image-prompt | 提示词优化 | Python |
| **效率工具** | utools | 跨平台工具箱 | Python |

## Skills Included

### 🛠️ Core Development Skills

#### [skill-developer](./skill-developer/)
Meta-skill for creating and managing Claude Code skills. Provides comprehensive guidance on skill development patterns, best practices, and the skill system architecture.

**Key Features:**
- Skill creation workflows
- Hook mechanisms and triggers
- Advanced patterns and troubleshooting
- Best practices for skill development

#### [skill-creator](./skill-creator/)
Guide for creating effective skills with proper structure, documentation, and packaging. Includes tools for skill initialization and validation.

**Key Features:**
- Skill initialization scripts
- Packaging and validation tools
- Progressive disclosure design principles
- Reusable resource management

### 🔌 Integration Skills

#### [mcp-builder](./mcp-builder/)
Comprehensive guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools.

**Key Features:**
- Agent-centric design principles
- Python and TypeScript implementation guides
- Evaluation-driven development
- Best practices for tool design

#### [byted-codebase](./byted-codebase/)
ByteDance codebase MCP tool integration with pre-configured authentication and region settings.

**Key Features:**
- Pre-configured PSM and region settings
- Python wrapper for MCP server communication
- Code search and repository management
- Integration with ByteDance internal tools

### 📋 Communication & Collaboration

#### [byted-lark-cli](./byted-lark-cli/)
Lark CLI tool integration for Feishu (飞书) operations including document queries, knowledge space management, messaging, and file operations.

**Key Features:**
- Document content queries
- Knowledge space node management
- Message sending (text, rich text, images)
- File upload and media operations
- Batch processing capabilities

#### [byted-logid](./byted-logid/)
ByteDance log ID generation and management utilities.

**Key Features:**
- Log ID generation
- Log query utilities
- Integration with ByteDance logging systems

### 📋 Communication & Collaboration

#### [byted-lark-cli](./byted-lark-cli/)
Lark CLI tool integration for Feishu (飞书) operations including document queries, knowledge space management, messaging, and file operations.

**Key Features:**
- Document content queries
- Knowledge space node management
- Message sending (text, rich text, images)
- File upload and media operations
- Batch processing capabilities

#### [byted-logid](./byted-logid/)
ByteDance log ID generation and management utilities.

**Key Features:**
- Log ID generation
- Log query utilities
- Integration with ByteDance logging systems

#### [lark-send-msg](./lark-send-msg/)
飞书消息发送工具，支持发送文本、富文本、图片等多种消息类型。

**Key Features:**
- 支持多种消息类型（文本、富文本、图片）
- 简单易用的命令行接口
- 飞书群组消息发送

#### [lark-md-to-doc](./lark-md-to-doc/)
将Markdown文档转换为飞书文档的工具。

**Key Features:**
- Markdown到飞书文档格式转换
- 保持文档结构和样式
- 支持批量转换

#### [lark-doc-to-md](./lark-doc-to-md/)
将飞书文档转换为Markdown格式的工具。

**Key Features:**
- 飞书文档到Markdown转换
- 保持内容格式和结构
- 支持文档批量导出

### 🔌 Integration Skills

#### [mcp-builder](./mcp-builder/)
Comprehensive guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools.

**Key Features:**
- Agent-centric design principles
- Python and TypeScript implementation guides
- Evaluation-driven development
- Best practices for tool design

#### [byted-codebase](./byted-codebase/)
ByteDance codebase MCP tool integration with pre-configured authentication and region settings.

**Key Features:**
- Pre-configured PSM and region settings
- Python wrapper for MCP server communication
- Code search and repository management
- Integration with ByteDance internal tools

#### [chrome-mcp](./chrome-mcp/)
Chrome浏览器MCP集成，允许通过MCP协议控制Chrome浏览器。

**Key Features:**
- Chrome浏览器自动化控制
- 页面内容提取和操作
- 与MCP服务器无缝集成

#### [github-mcp](./github-mcp/)
GitHub MCP集成，提供GitHub API访问和操作功能。

**Key Features:**
- GitHub仓库管理
- Issue和PR操作
- 代码审查辅助

### 🚀 Productivity Tools

#### [utools](./utools/)
Integration with uTools - a cross-platform toolbox with plugins for daily tasks and workflow automation.

**Key Features:**
- Cross-platform utility integration
- Plugin-based architecture
- Workflow automation
- Productivity tool access

#### [git-tag](./git-tag/)
Git标签管理工具，简化标签创建和管理流程。

**Key Features:**
- 快速创建Git标签
- 标签版本管理
- 与CI/CD流程集成

#### [review-go](./review-go/)
Go代码审查工具，提供代码质量检查和改进建议。

**Key Features:**
- Go代码静态分析
- 代码风格检查
- 性能优化建议

#### [ark-generate-image](./ark-generate-image/)
图像生成工具，支持多种图像生成服务。

**Key Features:**
- 多平台图像生成服务支持
- 灵活的参数配置
- 批量图像生成

#### [polish-image-prompt](./polish-image-prompt/)
图像提示词优化工具，帮助改进AI图像生成的提示词。

**Key Features:**
- 提示词优化建议
- 风格化和细节增强
- 多语言支持

## Quick Start

### 1. Understanding the Skill System

Skills are activated based on triggers defined in [`skill-rules.json`](./skill-rules.json). Each skill has:
- **Keywords**: Specific terms that trigger the skill
- **Intent Patterns**: Regular expressions matching user intent
- **File Triggers**: Path and content patterns that activate skills

### 2. Using a Skill

When a skill is triggered, Claude will:
1. Load the skill's metadata and description
2. Access the SKILL.md file for detailed instructions
3. Use bundled resources (scripts, references, assets) as needed

### 3. Creating New Skills

Use the skill-creator to build new skills:

```bash
# Initialize a new skill
python skill-creator/scripts/init_skill.py my-new-skill --path ./

# Edit the generated SKILL.md and add resources
# Package the skill when ready
python skill-creator/scripts/package_skill.py my-new-skill
```

## Usage Examples

### 飞书文档操作示例

```bash
# 查询飞书文档内容
lark-cli get-doc-content <文档URL>

# 发送飞书消息
lark-send-msg --chat-id <群组ID> --content "Hello, Team!"

# Markdown转飞书文档
lark-md-to-doc input.md --title "我的文档" --folder "知识库/项目文档"
```

### MCP服务器开发示例

```python
# 使用mcp-builder创建新的MCP服务器
from mcp_builder import MCPServer

server = MCPServer("my-server")
server.add_tool("search", search_function)
server.run()
```

### Git操作示例

```bash
# 使用git-tag创建版本标签
./git-tag/scripts/create_tag.sh v1.0.0 "Release version 1.0.0"

# 使用gcmsge生成提交信息
echo "feat: add new feature" | gcmsge
```

### 图像生成示例

```bash
# 使用ark-generate-image生成图像
./ark-generate-image/scripts/generate.py "a beautiful sunset over mountains"

# 使用polish-image-prompt优化提示词
./polish-image-prompt/scripts/polish.py "simple cat" --style "realistic" --detail "high"
```

## Project Structure

```
my-skills/
├── README.md                    # 项目主文档（当前文件）
├── skill-rules.json            # 技能激活规则配置
├── .gitignore                  # Git忽略文件
├── .claude/                    # Claude Code配置目录
│   ├── settings.local.json     # 本地设置
│   ├── hooks/                  # 钩子脚本目录
│   └── skills/                 # 已安装的技能
└── [技能目录]/                  # 各个独立技能模块
    ├── SKILL.md               # 技能说明文档（必需）
    ├── scripts/               # 可执行脚本（可选）
    ├── references/            # 参考文档（可选）
    └── assets/                # 资源文件（可选）
```

## Skill Configuration

The [`skill-rules.json`](./skill-rules.json) file controls skill activation with these enforcement levels:

- **suggest**: Skill appears as a suggestion but doesn't block execution
- **block**: Requires skill usage before proceeding (guardrail)
- **warn**: Shows warning but allows proceeding

Priority levels determine activation precedence:
- **critical**: Always trigger when matched
- **high**: Trigger for most matches
- **medium**: Trigger for clear matches
- **low**: Trigger only for explicit matches

## Architecture

### Skill Structure
```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter with name and description
│   └── Markdown instructions
├── scripts/ (optional)
│   └── Executable code (Python, Bash, etc.)
├── references/ (optional)
│   └── Documentation and reference material
└── assets/ (optional)
    └── Templates, images, and output resources
```

### Progressive Disclosure
Skills use a three-level loading system:
1. **Metadata** - Always in context (~100 words)
2. **SKILL.md** - Loaded when skill triggers (<5k words)
3. **Bundled resources** - Loaded as needed (unlimited)

## Development Guidelines

### Creating Effective Skills

1. **Start with concrete examples** - Understand real use cases
2. **Identify reusable components** - Scripts, references, assets
3. **Follow the skill creation process** - Use provided tools
4. **Write in imperative form** - Use verb-first instructions
5. **Test thoroughly** - Create evaluations for complex skills

### Best Practices

- Keep SKILL.md focused on procedural knowledge
- Move detailed reference material to references/
- Use scripts for deterministic operations
- Create evaluations for MCP servers
- Follow language-specific guidelines (Python/TypeScript)

## Requirements

- Claude Code CLI
- Python 3.8+ (for Python-based skills)
- Node.js 16+ (for TypeScript-based skills)
- Specific dependencies listed in individual skill directories

## Contributing

1. Follow the skill creation process outlined in skill-creator
2. Ensure all skills pass validation before packaging
3. Update skill-rules.json when adding new skills
4. Create evaluations for MCP server skills
5. Test skills in real scenarios before submission

## License

See individual skill directories for specific license terms. Most skills include complete terms in LICENSE.txt files.

## Support

For issues or questions:
- Check individual skill documentation
- Review troubleshooting guides in skill directories
- Create evaluations to test skill functionality
- Follow the progressive disclosure principle for efficient context usage

---

## 中文使用说明

### 快速开始

1. **安装Claude Code CLI**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **克隆本仓库**
   ```bash
   git clone <仓库地址> my-skills
   cd my-skills
   ```

3. **配置技能规则**
   编辑 `skill-rules.json` 文件，根据需要调整技能的触发条件和优先级。

4. **使用技能**
   在与Claude对话时，技能会根据触发条件自动激活。你也可以直接使用技能的命令行工具。

### 技能开发最佳实践

1. **渐进式披露**：技能信息分三级加载，确保高效使用上下文
2. **模块化设计**：每个技能独立，避免相互依赖
3. **明确触发条件**：使用精确的关键词和意图模式
4. **完善文档**：每个技能都应包含详细的SKILL.md文档
5. **测试验证**：创建评估用例，确保技能功能正常

### 常见问题

**Q: 技能没有自动触发怎么办？**
A: 检查skill-rules.json中的触发条件是否匹配你的输入，可以尝试使用更明确的关键词。

**Q: 如何创建自定义技能？**
A: 使用skill-creator技能，它提供了完整的技能创建流程和工具。

**Q: 技能冲突如何处理？**
A: 通过调整skill-rules.json中的优先级（priority）来解决冲突，高优先级技能会优先触发。

---

**Note**: This is a living collection. Skills are continuously improved based on usage patterns and feedback. The skill system itself evolves to support new capabilities and better integration patterns.