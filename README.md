# Opus Orchestrator AI

> A comprehensive AI-powered book generation system with LangGraph, CrewAI, and AutoGen.

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/LangGraph-✅-green.svg" alt="LangGraph">
  <img src="https://img.shields.io/badge/CrewAI-✅-green.svg" alt="CrewAI">
  <img src="https://img.shields.io/badge/AutoGen-✅-green.svg" alt="AutoGen">
  <img src="https://img.shields.io/badge/Pydantic-✅-green.svg" alt="Pydantic">
</p>

## 🎯 What is Opus?

Opus is an AI-powered book generation system that creates professional manuscripts using multiple AI agent frameworks. It supports **fiction** and **nonfiction** with intelligent purpose classification.

## ✨ Features

- **Multi-Framework Orchestration**: LangGraph, CrewAI, and AutoGen
- **Intelligent Purpose Classification**: Automatically determines reader purpose
- **100+ Content Frameworks**: From textbooks to RPG modules
- **Checkpoint/Resume**: Long generations can resume from failure
- **REST API + CLI**: Programmatic or command-line usage

## 🚀 Quick Start

```bash
# Install
pip install opus-orchestrator

# Generate a book (fiction)
opus generate --concept "A robot who dreams of being human" --genre sci-fi

# Generate a book (nonfiction)
opus generate --book-type nonfiction --purpose learn --category technology "How to build an AI app"

# Resume from checkpoint
opus generate --thread-id abc123 --resume
```

## 📚 Framework Library

Opus supports **100+ frameworks** organized by content type:

### Nonfiction Categories

| Category | Frameworks | Purpose |
|----------|-----------|---------|
| **Tutorial/How-To** | Tutorial, Howto, Minimalist How-To, Challenge-Response | Learn to do something |
| **Explanation** | Concept Explainer, Explainer, Socratic Method | Understand a concept |
| **Transformation** | Transformation Journey, Mountain Structure, Atomic Habits | Personal change |
| **Decision** | Big Idea, Problem-Solution, Case Study | Make informed decisions |
| **Reference** | Technical Manual, Quick Reference, Encyclopedia | Look up information |
| **Inspiration** | Visionary, Narrative, Memoir | Feel motivated |

### Educational/Academic

| Category | Frameworks |
|----------|-----------|
| **Textbooks** | Comprehensive Textbook, Textbook Chapter, Workbook |
| **Courses** | Online Course, Curriculum/Syllabus, Study Guide |
| **Academic** | Empirical Paper, Theoretical Paper, Literature Review, Thesis |
| **Research** | Position Paper, Policy Brief, Meta-Analysis |

### Creative/Interactive

| Category | Frameworks |
|----------|-----------|
| **Branching** | Choose Your Own Adventure, Gamebook, Visual Novel |
| **Epistolary** | Epistolary Novel, Found Documents |
| **Manifesto** | Manifesto, Open Letter |
| **Experimental** | Infinite Story, Fractal Narrative, Scrapbook |
| **Performance** | Podcast Script, Screenplay, Stage Play |

### RPG/Tabletop Gaming

| Category | Frameworks |
|----------|-----------|
| **Core** | Core Rulebook, Quickstart |
| **GM Guides** | Game Master Guide, Adventure Module, Campaign Setting |
| **Supplements** | Player's Companion, Monster Manual, Sourcebook |
| **Adventure Types** | Dungeon Crawl, Hex Crawl, Sandbox |

## 🔧 Configuration

### Environment Variables

```bash
export OPENAI_API_KEY="your-key"  # or
export MINIMAX_API_KEY="your-key"
```

### Config File (`opus.yaml`)

```yaml
agent:
  model: gpt-4o
  temperature: 0.7
  max_tokens: 4000

output:
  format: markdown
  save_to_file: true
```

## 💻 CLI Commands

```bash
# Generate a book
opus generate --concept "Your book idea" [options]

# Options:
#   --book-type {fiction,nonfiction}  Book type
#   --framework {snowflake,save-the-cat,...}  Story framework
#   --genre {sci-fi,fantasy,romance,...}  Genre
#   --purpose {learn,understand,transform,decide,reference,inspire}  Reader purpose
#   --category {business,leadership,memoir,...}  Nonfiction category
#   --words TARGET_WORD_COUNT  Target word count
#   --thread-id THREAD_ID  Checkpoint ID for resume
#   --resume  Resume from checkpoint

# Serve API
opus serve --port 8000

# List frameworks
opus frameworks

# Ingest from GitHub
opus ingest --repo https://github.com/user/repo
```

## 🔌 REST API

```bash
# Start server
opus serve

# Generate (blocking)
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"concept": "Your book idea", "book_type": "fiction"}'

# Generate (streaming)
curl -X POST http://localhost:8000/generate/stream \
  -H "Content-Type: application/json" \
  -d '{"concept": "Your book idea"}'
```

## 🧠 Architecture

```
User Input → Intent Classification → Framework Selection
    ↓
Purpose Detection (learn/understand/transform/decide/reference/inspire)
    ↓
Framework匹配 (100+ frameworks by category)
    ↓
Agent Selection (purpose-specific writer + critique)
    ↓
Generation Pipeline (LangGraph/CrewAI/AutoGen)
    ↓
Manuscript Output
```

## 📦 Nonfiction Purpose System

The nonfiction pipeline uses **Purpose × Structure** classification:

### Reader Purposes

1. **LEARN_HANDS_ON** — Reader wants to DO something (tutorials, how-to)
2. **UNDERSTAND** — Reader wants to GRASP a concept (explanations)
3. **TRANSFORM** — Reader wants to CHANGE themselves (self-help, memoir)
4. **DECIDE** — Reader wants to MAKE A DECISION (business, analysis)
5. **REFERENCE** — Reader wants to LOOK UP info (manuals, documentation)
6. **BE_INSPIRED** — Reader wants to FEEL motivated (stories, manifestos)

### Framework Selection

The system automatically selects the best framework based on:
- Explicit flags (`--purpose`, `--category`)
- Keyword classification from concept
- Content analysis (for existing blogs/articles)
- Conversational Q&A (when ambiguous)

## 🔄 Checkpointing/Resume

Long generations can fail. Use checkpointing to resume:

```bash
# First run - saves checkpoint
opus generate --concept "My book" --thread-id my-book-001
# If it fails...

# Resume from checkpoint
opus generate --concept "My book" --thread-id my-book-001 --resume
```

## 🤖 Multi-Agent Systems

Opus supports three orchestration backends:

1. **LangGraph** — State machine with checkpointing
2. **CrewAI** — Sequential agent crews
3. **AutoGen** — Multi-agent debate/critique

## 📁 Project Structure

```
opus_orchestrator/
├── orchestrator.py       # Main orchestration
├── langgraph_workflow.py # LangGraph pipeline
├── crews/               # CrewAI crews
├── autogen_critique.py  # AutoGen critique
├── agents/              # Agent definitions
│   ├── fiction/        # Fiction writers
│   └── nonfiction/      # Nonfiction writers + purpose-specific
├── frameworks.py        # Fiction frameworks
├── nonfiction/          # Nonfiction system
│   ├── classifier.py    # Purpose classifier
│   ├── intake.py       # Intake agent
│   ├── expanded_frameworks.py   # 35+ frameworks
│   ├── textbook_frameworks.py   # Educational
│   ├── academic_papers.py       # Academic types
│   ├── creative_frameworks.py   # Interactive
│   └── rpg_frameworks.py       # Tabletop RPG
├── server.py            # REST API
└── cli.py              # CLI
```

## 📄 License

MIT

## 👤 Author

Mark Havens

## 🔗 Links

- [GitHub](https://github.com/mrhavens/opus-orchestrator-ai)
- [Documentation](https://github.com/mrhavens/opus-orchestrator-ai/docs)
