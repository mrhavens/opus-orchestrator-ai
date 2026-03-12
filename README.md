# Opus Orchestrator AI

> Full-flow AI book generation orchestrator using LangGraph, CrewAI, AutoGen, and PydanticAI. Integrates Fiction Fortress and Nonfiction Fortress for professional manuscript production.

## Overview

Opus Orchestrator AI transforms raw content (notes, outlines, stream-of-consciousness, essays, logs) into fully edited, publication-ready manuscripts. It combines:

- **LangGraph** — Workflow orchestration and state management
- **CrewAI** — Role-based agent crews
- **AutoGen** — Complex multi-agent negotiations
- **PydanticAI** — Structured output validation
- **Fiction Fortress** — Complete fiction writing methodology
- **Nonfiction Fortress** — Complete non-fiction writing methodology

## Architecture

```
[GitHub Repo Input]
        │
        ▼
┌───────────────────┐
│   INGESTOR AGENT  │ ──► Extracts raw content from repo
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ INTENT ANALYZER   │ ──► Analyzes goals, audience, intended outcome
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   BLUEPRINT       │ ──► Generates detailed book blueprint
└────────┬──────────┘
         │
         ▼
    ┌────┴────┐
    │ ITERATE │
    └────┬────┘
         │
    ┌────▼─────────────┐
    │ CREW EXECUTION   │ ──► Runs agent crews per chapter
    │ • Writer         │
    │ • Critics (3+)   │
    │ • Editor         │
    │ • Proofreader    │
    └────┬─────────────┘
         │
    ┌────▼─────────────┐
    │ REVIEW & REVISE  │ ──► Internal critic circle
    └────┬─────────────┘
         │
         └─────────────┬────► [Loop back if needed]
                        │
                        ▼
              ┌─────────────────┐
              │ COMPILED .MD    │
              │ MANUSCRIPT      │
              └─────────────────┘
```

## Installation

```bash
git clone https://github.com/mrhavens/opus-orchestrator-ai.git
cd opus-orchestrator-ai
pip install -e .
```

## Quick Start

```python
from opus_orchestrator import OpusOrchestrator

orchestrator = OpusOrchestrator(
    repo_url="https://github.com/user/my-book-ideas",
    book_type="fiction",  # or "nonfiction"
    genre="science-fiction",
    target_audience="adult sci-fi readers",
    intended_outcome="complete novel, ~80k words"
)

# Run the full pipeline
manuscript = await orchestrator.run()
print(f"Generated: {manuscript.word_count} words")
```

## Configuration

See `config.example.yaml` for full configuration options.

## Project Structure

```
opus_orchestrator/
├── __init__.py           # Main exports
├── config.py             # Configuration management
├── state.py              # LangGraph state definitions
├── graph.py              # Main workflow graph
├── agents/
│   ├── __init__.py
│   ├── base.py           # Base agent class
│   ├── fiction/          # Fiction Fortress agents
│   │   ├── architect.py
│   │   ├── worldsmith.py
│   │   ├── character_lead.py
│   │   ├── voice.py
│   │   └── editor.py
│   └── nonfiction/       # Nonfiction Fortress agents
│       ├── researcher.py
│       ├── analyst.py
│       ├── writer.py
│       ├── fact_checker.py
│       └── editor.py
├── crews/
│   ├── __init__.py
│   ├── fiction_crew.py   # Fiction writing crew
│   └── nonfiction_crew.py
├── schemas/
│   ├── __init__.py
│   ├── book.py           # Book-level schemas
│   ├── chapter.py        # Chapter schemas
│   └── critique.py       # Critique schemas
└── utils/
    ├── __init__.py
    ├── github.py         # GitHub ingestion
    └── output.py        # Output generation
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
ruff check .
ruff format .
```

## Dependencies

- langgraph
- crewai
- autogen
- pydantic-ai
- pydantic
- httpx
- pygithub
- pyyaml

## License

MIT

---

*Built with the WE Architecture — witness and co-creation in code.*
