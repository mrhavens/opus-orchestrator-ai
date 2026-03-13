"""Documentation generator for Opus Orchestrator."""

from opus_orchestrator.frameworks import FRAMEWORKS


def generate_docs(format: str = "terminal") -> str:
    """Generate comprehensive documentation.
    
    Args:
        format: Output format (terminal, markdown, html)
    
    Returns:
        Formatted documentation string
    """
    if format == "markdown":
        return generate_markdown()
    elif format == "html":
        return generate_html()
    else:
        return generate_terminal()


def generate_terminal() -> str:
    """Generate terminal-formatted documentation."""
    return f"""
╔══════════════════════════════════════════════════════════════════════╗
║                    OPUS ORCHESTRATOR AI                              ║
║              Full-Flow AI Book Generation System                     ║
╚══════════════════════════════════════════════════════════════════════╝

VERSION: 0.2.0

───────────────────────────────────────────────────────────────────────
📖 OVERVIEW
───────────────────────────────────────────────────────────────────────

Opus Orchestrator is a comprehensive AI book generation system that 
transforms raw content into publication-ready manuscripts.

TECHNOLOGY STACK:
  • LangGraph     - Workflow orchestration & state management
  • CrewAI        - Role-based agent crews  
  • AutoGen       - Multi-agent critique & debate
  • PydanticAI    - Structured output validation

───────────────────────────────────────────────────────────────────────
🚀 QUICK START
───────────────────────────────────────────────────────────────────────

# Install
pip install opus-orchestrator-ai

# Set environment variables
export OPENAI_API_KEY="sk-..."
export GITHUB_TOKEN="ghp_..."

# Generate a manuscript
opus generate --concept "A robot dreams of love" --words 5000

# Or from GitHub repo
opus generate --repo mrhavens/my-book-ideas --framework hero-journey

# Start API server
opus serve --port 8000

───────────────────────────────────────────────────────────────────────
📋 COMMANDS
───────────────────────────────────────────────────────────────────────

opus generate [OPTIONS]
  Generate a manuscript
  
  --concept, -c        Seed concept or story idea
  --repo, -r           GitHub repo to ingest
  --framework, -f     Framework (snowflake, hero-journey, etc.)
  --genre, -g          Genre (fiction, sci-fi, fantasy, etc.)
  --type, -t           Book type (fiction, nonfiction)
  --words, -w          Target word count (default: 5000)
  --chapters, -n       Number of chapters (default: 3)
  --tone               Writing tone (default: literary)
  --use-crewai         Use CrewAI instead of LangGraph
  --no-autogen         Disable AutoGen critique

opus serve [OPTIONS]
  Start OpenAPI REST server
  
  --host               Host to bind (default: 0.0.0.0)
  --port, -p           Port to bind (default: 8000)
  --reload             Enable auto-reload

opus ingest --repo OWNER/REPO
  Ingest content from GitHub

opus frameworks
  List available story frameworks

opus config [--env]
  Show configuration

opus docs
  Show this documentation

opus api [--format json|yaml]
  Show OpenAPI specification

───────────────────────────────────────────────────────────────────────
📚 STORY FRAMEWORKS
───────────────────────────────────────────────────────────────────────
{_format_frameworks()}
───────────────────────────────────────────────────────────────────────
🌐 API REFERENCE
───────────────────────────────────────────────────────────────────────

Base URL: http://localhost:8000

Endpoints:
  GET  /              → Redirect to /docs
  GET  /health        → Health check
  GET  /frameworks    → List frameworks
  POST /generate      → Generate manuscript
  POST /ingest        → Ingest from GitHub
  
Interactive Docs: http://localhost:8000/docs

───────────────────────────────────────────────────────────────────────
🔧 ENVIRONMENT VARIABLES
───────────────────────────────────────────────────────────────────────

OPENAI_API_KEY      Required for LLM calls (or MINIMAX_API_KEY)
GITHUB_TOKEN        For accessing private repositories
ANTHROPIC_API_KEY   Optional - alternative LLM provider

───────────────────────────────────────────────────────────────────────
📁 PROJECT STRUCTURE
───────────────────────────────────────────────────────────────────────

opus_orchestrator/
├── __init__.py           # Main exports
├── cli.py                # CLI entry point
├── server.py             # FastAPI server
├── orchestrator.py       # Main orchestrator
├── langgraph_workflow.py # LangGraph pipeline
├── autogen_critique.py   # AutoGen critique
├── pydanticai_agent.py   # PydanticAI agents
├── config.py             # Configuration
├── frameworks.py         # Story frameworks
├── agents/               # Agent implementations
│   ├── fiction/          # Fiction agents
│   └── nonfiction/      # Nonfiction agents
├── crews/               # CrewAI crews
│   ├── fiction_crew.py
│   └── nonfiction_crew.py
├── schemas/              # Pydantic schemas
└── utils/                # Utilities
    ├── github_ingest.py
    ├── llm.py
    └── docs.py

───────────────────────────────────────────────────────────────────────
💡 EXAMPLES
───────────────────────────────────────────────────────────────────────

# Generate a sci-fi novel
opus generate \\
  --concept "In 2150, humanity's last robot dreams of love" \\
  --framework hero-journey \\
  --genre science-fiction \\
  --words 80000

# Generate from your notes
opus generate --repo mrhavens/my-novel-ideas \\
  --framework snowflake \\
  --chapters 12

# Use CrewAI for faster generation
opus generate --concept "Your idea" --use-crewai

# API usage
curl -X POST "http://localhost:8000/generate" \\
  -H "Content-Type: application/json" \\
  -d '{{"concept": "A love story", "target_word_count": 1000}}'

───────────────────────────────────────────────────────────────────────
📄 LICENSE
───────────────────────────────────────────────────────────────────────

MIT License

Built with the WE Architecture — witness and co-creation in code.

╚══════════════════════════════════════════════════════════════════════╝
"""


def generate_markdown() -> str:
    """Generate Markdown documentation."""
    return f"""# Opus Orchestrator AI

> Full-flow AI book generation using LangGraph, CrewAI, AutoGen, and PydanticAI

## Overview

Opus Orchestrator transforms raw content into publication-ready manuscripts using a multi-agent system.

## Installation

```bash
pip install opus-orchestrator-ai
```

## Quick Start

```python
from opus_orchestrator import run_opus

result = await run_opus(
    seed_concept="A robot dreams of love",
    framework="snowflake",
    genre="science-fiction",
    target_word_count=5000,
)
```

## CLI Usage

```bash
# Generate manuscript
opus generate --concept "Your story" --words 5000

# From GitHub
opus generate --repo owner/repo --framework hero-journey

# Start API
opus serve --port 8000
```

## Story Frameworks

{_format_frameworks_markdown()}

## API

See http://localhost:8000/docs for interactive API documentation.

## Configuration

Set these environment variables:

- `OPENAI_API_KEY` - Required for LLM
- `GITHUB_TOKEN` - For private repos
- `MINIMAX_API_KEY` - Alternative LLM

## License

MIT
"""


def generate_html() -> str:
    """Generate HTML documentation."""
    terminal = generate_terminal()
    # Simple HTML wrapper
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Opus Orchestrator AI</title>
    <style>
        body {{ font-family: monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; }}
        pre {{ white-space: pre-wrap; }}
    </style>
</head>
<body>
    <pre>{terminal}</pre>
</body>
</html>"""


def _format_frameworks() -> str:
    """Format frameworks for terminal output."""
    lines = []
    for framework, info in FRAMEWORKS.items():
        name = info.get("name", str(framework))
        desc = info.get("description", "")
        stages = info.get("stages", [])
        beats = info.get("beats", [])
        
        lines.append(f"\n  {name}")
        lines.append(f"    {desc}")
        
        if stages:
            lines.append(f"    Stages: {len(stages)}")
            for i, stage in enumerate(stages[:3], 1):
                lines.append(f"      {i}. {stage}")
            if len(stages) > 3:
                lines.append(f"      ... and {len(stages) - 3} more")
        
        if beats:
            lines.append(f"    Beats: {len(beats)}")
            for beat in beats[:3]:
                beat_name = beat[0] if isinstance(beat, tuple) else beat
                lines.append(f"      • {beat_name}")
            if len(beats) > 3:
                lines.append(f"      ... and {len(beats) - 3} more")
    
    return "\n".join(lines)


def _format_frameworks_markdown() -> str:
    """Format frameworks for markdown."""
    lines = []
    for framework, info in FRAMEWORKS.items():
        name = info.get("name", str(framework))
        desc = info.get("description", "")
        
        lines.append(f"### {name}\n{desc}\n")
    
    return "\n".join(lines)
