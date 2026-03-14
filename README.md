# Opus Orchestrator AI

> A comprehensive AI-powered book generation system with LangGraph, CrewAI, and AutoGen.

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/LLM-MiniMax_M2.5-green.svg" alt="MiniMax">
  <img src="https://img.shields.io/badge/KDP-Ready-orange.svg" alt="KDP">
  <img src="https://img.shields.io/badge/Docker-k3s-blue.svg" alt="Docker/k3s">
</p>

## 🎯 What is Opus?

Opus is an AI-powered book generation system that creates professional manuscripts. It supports **fiction** and **nonfiction** with intelligent purpose classification, multiple export formats, and professional publishing workflows.

## ✨ Features

### Core Capabilities
- **Multi-Framework Orchestration**: LangGraph, CrewAI, and AutoGen
- **Intelligent Purpose Classification**: Automatically determines reader purpose
- **100+ Content Frameworks**: From textbooks to RPG modules
- **Checkpoint/Resume**: Long generations can resume from failure

### Input Sources
- **GitHub Repository**: Ingest from any public/private repo
- **S3/Backblaze**: Cloud storage ingestion
- **Local Files**: Direct file input

### Output Formats
- **Scrivener Export**: Chapter-by-chapter with `binder.json`
- **LaTeX**: 31 professional templates
- **HTML**: Styled web output
- **PDF**: Via LaTeX compilation

### Publishing
- **KDP Templates**: 5 trim sizes (5x8, 5.5x8.5, 6x9, 8x8, 8.5x11)
- **31 LaTeX Templates**: Novel, memoir, academic, RPG, cookbook, etc.
- **ISBN/Metadata**: Full publishing metadata support

### Deployment
- **Docker Compose**: Full local stack
- **k3s/Helm**: Production Kubernetes
- **REST API**: Programmatic access

## 🚀 Quick Start

```bash
# Install
pip install opus-orchestrator

# Generate a book (fiction)
opus generate --concept "A robot who dreams of being human" --genre sci-fi

# Generate a book (nonfiction)
opus generate --book-type nonfiction --purpose learn "How to build an AI app"

# Serve API
opus serve --port 8000
```

## 📚 Framework Library

Opus supports **100+ frameworks** organized by content type:

### Nonfiction

| Category | Frameworks | Purpose |
|----------|-----------|---------|
| **Tutorial/How-To** | Tutorial, Howto, Minimalist How-To | Learn to do |
| **Explanation** | Concept Explainer, Socratic Method | Understand |
| **Transformation** | Transformation Journey, Atomic Habits | Personal change |
| **Decision** | Big Idea, Case Study | Make decisions |
| **Reference** | Technical Manual, Quick Reference | Look up info |

### Fiction

| Category | Frameworks |
|----------|-----------|
| **Snowflake** | One-page to novel |
| **Three-Act** | Classic structure |
| **Hero's Journey** | Mythic structure |
| **Save the Cat** | Screenwriting |
| **Story Circle** | Dan Harmon's 8-part |

### RPG/Game Books

| Category | Frameworks |
|----------|-----------|
| **Rulebook** | Core rules, system |
| **Adventure** | Dungeon module, campaign |
| **CYOA** | Choose Your Own Adventure |

## 📄 Output Formats

### Scrivener Export
```python
from opus_orchestrator import export_to_scrivener

result = export_to_scrivener(
    manuscript,
    "My Book",
    split_chapters=True,
    branch="draft/chapter-1",
    push_to_remote=True,
)
```
Output: Individual `.md` files + `binder.json`

### LaTeX Templates (31)
```python
from opus_orchestrator import export_to_latex

export_to_latex(manuscript, "My Book", "out.tex", 
    template="kdp-trade")
```

**Templates:**
- **KDP**: pocket, trade, 6x9, square, large
- **Genre**: novel, memoir, romance, thriller, sci-fi
- **Academic**: textbook, academic, cleanthesis, classicthesis
- **Specialty**: poetry, cookbook, screenplay, RPG

### HTML Export
```python
from opus_orchestrator import export_to_html

html = export_to_html(manuscript, "My Book", 
    template="memoir")
```

## 🏭 Deployment

### Docker Compose
```bash
# Quick start
cp .env.example .env
# Add your MINIMAX_API_KEY and GITHUB_TOKEN

docker-compose -f deployments/docker-compose.yml up -d
```

### k3s/Helm
```bash
# Install Opus API
helm install opus deployments/k3s/opus-orchestrator/

# Install TeX Live API (for PDF compilation)
helm install texlive deployments/k3s/texlive-api/
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

## ⚙️ Configuration

### Environment Variables
```bash
export MINIMAX_API_KEY="your-key"  # Primary
export GITHUB_TOKEN="your-token"
```

### Config File
```yaml
agent:
  provider: minimax
  model: MiniMax/MiniMax-M2.5
  temperature: 0.7

output:
  format: markdown
  save_to_file: true
  split_chapters: true
```

## 🧠 Architecture

```
User Input → Intent Classification → Framework Selection
    ↓
Purpose Detection (learn/understand/transform/decide)
    ↓
Framework匹配 (100+ frameworks)
    ↓
Agent Selection (purpose-specific)
    ↓
Generation (LangGraph/CrewAI/AutoGen)
    ↓
Output (Scrivener/LaTeX/HTML/PDF)
```

## 📁 Project Structure

```
opus_orchestrator/
├── orchestrator.py          # Main orchestration
├── server.py               # REST API
├── cli.py                  # CLI
├── langgraph_workflow.py   # LangGraph pipeline
├── nonfiction/             # Nonfiction system
│   ├── classifier.py       # Purpose classifier
│   └── frameworks.py       # 35+ frameworks
├── frameworks.py           # Fiction frameworks
├── scrivener_export.py    # Scrivener output
├── latex_compile.py        # LaTeX export
├── html_export.py          # HTML output
├── texlive_client.py       # TeX Live API
├── templates/
│   └── latex/             # 31 templates
└── deployments/
    ├── docker-compose.yml
    └── k3s/
```

## 📦 Test Suite

```bash
# Run tests
pytest tests/ -v

# Test categories
tests/
├── test_github_ingest.py   # GitHub ingestion
├── test_s3_ingest.py      # S3/Backblaze
├── test_generation.py     # Document generation
├── test_output_push.py    # Output push
└── test_e2e.py           # End-to-end
```

## 🔗 Links

- [GitHub](https://github.com/mrhavens/opus-orchestrator-ai)
- [Issues](https://github.com/mrhavens/opus-orchestrator-ai/issues)
- [BECOMINGONE](https://github.com/mrhavens/becomingone)

## 📜 License

MIT

## 👤 Author

Mark Havens

---

*Built with ♥ using MiniMax M2.5*
