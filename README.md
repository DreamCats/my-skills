# Claude Code Skills Collection

A comprehensive collection of specialized skills for extending Claude Code's capabilities across various domains including development workflows, communication tools, and system integrations.

## Overview

This repository contains a curated set of skills that transform Claude from a general-purpose AI into specialized agents equipped with domain-specific knowledge, tools, and workflows. Each skill is self-contained and can be used independently or in combination with others.

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

### 🚀 Productivity Tools

#### [utools](./utools/)
Integration with uTools - a cross-platform toolbox with plugins for daily tasks and workflow automation.

**Key Features:**
- Cross-platform utility integration
- Plugin-based architecture
- Workflow automation
- Productivity tool access

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

**Note**: This is a living collection. Skills are continuously improved based on usage patterns and feedback. The skill system itself evolves to support new capabilities and better integration patterns.