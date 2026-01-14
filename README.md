# Gloomhaven 2E Rules Extraction

> **Pre-extracted markdown files are included in `gloomhaven_output/` for convenience.**

> ⚠️ **Disclaimer:** This is heavily vibe-coded. It works, but don't expect production-quality code.

Converts Gloomhaven Second Edition rulebook (PDF) and FAQ (HTML) into clean, structured markdown.

## Usage

```fish
uv sync
just all
```

Output: `gloomhaven_output/`

## Features

- Clean markdown structure with page markers
- FAQ spoilers wrapped in `<details>` tags
- 50%+ size reduction
- Ready for LLM ingestion

## Sources

**Rulebook:** [Google Drive](https://drive.google.com/file/d/16TmmCKa6zVVObj2qM-vIj9RcEAC3nfMT/view)  
**FAQ:** https://cephalofairgames.github.io/gloomhaven2e-faq/

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- [just](https://github.com/casey/just)
