---
name: utools
description: uTools is a cross-platform toolbox that allows you to use a series of plugins to help you complete daily tasks more efficiently.
---

# Utools Skill

Comprehensive assistance with utools development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with utools
- Asking about utools features or APIs
- Implementing utools solutions
- Debugging utools code
- Learning utools best practices

## Quick Reference

### Common Patterns

*Quick reference patterns will be added as you use the skill.*

### Example Code Patterns

**Example 1** (javascript):
```javascript
const writeText = require("./libs/writeText.js");

window.services = {
  writeText,
};
```

**Example 2** (javascript):
```javascript
const idleUBrowsers = utools.getIdleUBrowsers();
console.log(idleUBrowsers);
if (idleUBrowsers.length > 0) {
  utools.ubrowser.goto('https://www.u-tools.cn').run(idleUBrowsers[0].id)
}
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api-reference.md** - Api-Reference documentation
- **basic.md** - Basic documentation
- **information.md** - Information documentation
- **other.md** - Other documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
