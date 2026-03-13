# Opus Orchestrator AI

> Full-flow AI book generation system using **LangGraph**, **CrewAI**, **AutoGen**, and **PydanticAI**

A comprehensive, production-ready system for generating publication-ready manuscripts from raw content.

---

## ⚡ Quick Start

```bash
# Install
pip install opus-orchestrator-ai

# Generate a manuscript (local mode)
opus generate --concept "A robot dreams of electric sheep" --words 5000

# Or use API server mode
opus serve --port 8000
opus --api-url http://localhost:8000 generate --concept "Your idea"
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      OPUS ORCHESTRATOR AI                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │   INGEST   │───►│   LANGGRAPH │───►│    OUTPUT           │  │
│  │   LAYER    │    │   WORKFLOW  │    │    (Manuscript)     │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
│         │                  │                                       │
│    ┌────┴────┐       ┌────┴────┐                                 │
│    ▼         ▼       ▼         ▼                                  │
│ GitHub    S3/MinIO  CrewAI   AutoGen                              │
│ Ingestor  Ingestor   Agents   Critique                             │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                   VALIDATION LAYER                          │  │
│  │                    PydanticAI                               │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Features

### Core Generation

| Feature | Description | Status |
|---------|-------------|--------|
| **Snowflake Method** | 7-stage fractal expansion from sentence to novel | ✅ |
| **Story Frameworks** | 7 frameworks: Snowflake, 3-Act, Save the Cat, Hero's Journey, Story Circle, 7-Point, Fichtean | ✅ |
| **LangGraph Workflow** | State machine with streaming progress | ✅ |
| **AutoGen Critique** | Multi-agent debate (LiteraryCritic, GenreExpert, StoryEditor) | ✅ |
| **PydanticAI Validation** | Structured output validation with type-safe schemas | ✅ |

### Agent Systems

| Agent | Role | Status |
|-------|------|--------|
| **ArchitectAgent** | Story structure & blueprint | ✅ |
| **WorldsmithAgent** | World-building & setting | ✅ |
| **CharacterLeadAgent** | Character development | ✅ |
| **VoiceAgent** | Narrative voice & tone | ✅ |
| **EditorAgent** | Editorial review | ✅ |
| **ResearcherAgent** (Nonfiction) | Fact-finding | ✅ |
| **AnalystAgent** (Nonfiction) | Argument analysis | ✅ |

### Ingestion Sources

| Source | Description | Status |
|--------|-------------|--------|
| **GitHub** | Fetch from public/private repos | ✅ |
| **S3/MinIO** | S3-compatible object storage | ✅ |
| **Local Files** | Direct file input | ✅ |

### Deployment

| Mode | Description | Status |
|------|-------------|--------|
| **CLI** | Standalone command-line tool | ✅ |
| **API Server** | FastAPI REST server | ✅ |
| **API Client** | Client mode for remote servers | ✅ |
| **Python Module** | Import as library | ✅ |

### Output Options

| Destination | CLI Flag | Description |
|------------|----------|-------------|
| **Local File** | `--output FILE` | Save to local filesystem |
| **S3/MinIO** | `--save-s3 BUCKET/PATH` | Upload to S3-compatible storage |
| **GitHub** | `--save-repo OWNER/REPO` | Commit to GitHub repository |

---

## 🚀 Usage

### CLI Commands

```bash
# Generate manuscript (local, save to file)
opus generate --concept "Your story idea" --framework snowflake --words 5000

# Generate from GitHub
opus generate --repo owner/repo --framework hero-journey --words 80000

# Generate and save to S3/MinIO
opus generate --concept "..." --save-s3 my-bucket/manuscripts/
opus generate --concept "..." --save-s3 my-bucket/path/ --save-s3-endpoint https://nyc3.digitaloceanspaces.com

# Generate and save to GitHub repo
opus generate --concept "..." --save-repo owner/my-manuscripts
opus generate --concept "..." --save-repo owner/my-manuscripts --save-branch develop --save-commit-msg "New story draft"

# Generate from S3, save to GitHub
opus generate --repo owner/repo --save-repo owner/output-repo

# Generate from S3, save to different S3 bucket
opus ingest-s3 --bucket input-bucket --prefix notes/ | opus generate --save-s3 output-bucket/

# Ingest from S3/MinIO
opus ingest-s3 --bucket my-bucket --prefix notes/ --output content.txt

# Start API server
opus serve --port 8000

# Use as API client
opus --api-url http://localhost:8000 generate --concept "..."

# List frameworks
opus frameworks

# Show config
opus config

# Show docs
opus docs
```

### Python API

```python
from opus_orchestrator import run_opus

# Simple generation
result = await run_opus(
    seed_concept="A robot dreams of love",
    framework="snowflake",
    genre="science-fiction",
    target_word_count=5000,
)

manuscript = result["manuscript"]
```

### Using CrewAI

```python
from opus_orchestrator.crews import create_fiction_crew

crew = create_fiction_crew(
    genre="science-fiction",
    tone="literary",
    target_word_count=2000,
)

story = crew.write_full_story(
    story_outline="Your outline...",
    character_sheets="...",
    style_guide="Tone: literary",
    num_chapters=5,
)
```

### Using PydanticAI Validation

```python
from opus_orchestrator import create_style_guide_agent

agent = create_style_guide_agent()
result = agent.run_sync("Create a style guide for a literary novel")

# Result is a validated StyleGuide object
print(result.tone)        # "Contemplative and introspective"
print(result.pacing)      # "Deliberate with moments of acceleration"
```

### API Server

```python
from opus_orchestrator.server import app, run_server

# Run server
await run_server(host="0.0.0.0", port=8000)

# Or with uvicorn directly
# uvicorn opus_orchestrator.server:app --port 8000
```

### API Client

```python
from opus_orchestrator.cli import OpusAPIClient

client = OpusAPIClient("http://localhost:8000")

# Health check
health = client.health()

# Generate
result = client.generate(
    concept="A robot dreams",
    framework="snowflake",
    target_word_count=5000,
)

print(result["manuscript"])
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | Yes (or MINIMAX_API_KEY) |
| `MINIMAX_API_KEY` | MiniMax API key | No |
| `GITHUB_TOKEN` | GitHub token for private repos | No |
| `AWS_ACCESS_KEY_ID` | AWS access key for S3 | No |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key for S3 | No |
| `S3_ENDPOINT_URL` | Custom S3 endpoint (MinIO, DO Spaces) | No |

### Configuration File

```yaml
# config.yaml
agent:
  provider: openai
  model: gpt-4o
  temperature: 0.7
  max_tokens: null

iteration:
  min_critic_rounds: 2
  max_critic_rounds: 5
  approval_threshold: 0.8

output:
  format: markdown
  include_toc: true
  output_dir: ./output
```

---

## 📚 Story Frameworks

### Implemented Frameworks

| Framework | Type | Stages/Beats |
|-----------|------|---------------|
| **Snowflake Method** | Fractal | 7 stages |
| **Three-Act Structure** | Linear | 7 beats |
| **Save the Cat** | Screenplay | 15 beats |
| **Hero's Journey** | Mythic | 12 stages |
| **Story Circle** | Circular | 8 beats |
| **7-Point Plot** | Structural | 7 beats |
| **Fichtean Curve** | Episodic | 7 beats |

---

## 🧩 Project Structure

```
opus_orchestrator/
├── __init__.py           # Main exports
├── __main__.py           # CLI entry point
├── cli.py                # CLI implementation
├── server.py             # FastAPI server
├── orchestrator.py       # Main orchestrator
├── langgraph_workflow.py # LangGraph pipeline
├── autogen_critique.py  # AutoGen critique crew
├── pydanticai_agent.py  # PydanticAI agents
├── config.py             # Configuration
├── frameworks.py          # Story frameworks
│
├── agents/               # Agent implementations
│   ├── fiction/          # Fiction agents
│   │   ├── architect.py
│   │   ├── worldsmith.py
│   │   ├── character_lead.py
│   │   ├── voice.py
│   │   └── editor.py
│   └── nonfiction/      # Nonfiction agents
│       ├── researcher.py
│       ├── analyst.py
│       ├── writer.py
│       ├── fact_checker.py
│       └── editor.py
│
├── crews/               # CrewAI crews
│   ├── base_crew.py     # Base crew class
│   ├── fiction_crew.py  # Fiction crew
│   └── nonfiction_crew.py
│
├── schemas/              # Pydantic schemas
│   └── book.py
│
└── utils/               # Utilities
    ├── github_ingest.py # GitHub ingestion
    ├── s3_ingest.py    # S3/MinIO ingestion
    ├── llm.py          # LLM client
    └── docs.py         # Documentation generator
```

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=opus_orchestrator tests/

# Lint
ruff check .

# Format
ruff format .
```

---

## 📄 License

MIT License

---

## 🤝 Built With

- **LangGraph** - Workflow orchestration
- **CrewAI** - Multi-agent systems
- **AutoGen** - Complex agent conversations
- **PydanticAI** - Structured output validation
- **FastAPI** - REST API server
- **OpenAI** - LLM provider

---

*Built with the WE Architecture — witness and co-creation in code.*
