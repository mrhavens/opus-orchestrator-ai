"""OpenAPI Server for Opus Orchestrator.

FastAPI-based REST API with OpenAPI documentation.
"""

import os
from typing import Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv("/home/solaria/.openclaw/workspace/opus-orchestrator-ai/.env")

from opus_orchestrator.config import get_config
from opus_orchestrator import run_opus, OpusOrchestrator
from opus_orchestrator.frameworks import FRAMEWORKS


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class GenerateRequest(BaseModel):
    """Request to generate a manuscript."""
    concept: Optional[str] = Field(None, description="Seed concept or story idea")
    repo: Optional[str] = Field(None, description="GitHub repo to ingest")
    framework: str = Field("snowflake", description="Story framework")
    genre: str = Field("fiction", description="Genre")
    book_type: str = Field("fiction", description="Book type (fiction/nonfiction)")
    target_word_count: int = Field(5000, description="Target word count")
    chapters: int = Field(3, description="Number of chapters")
    tone: str = Field("literary", description="Writing tone")
    use_crewai: bool = Field(False, description="Use CrewAI instead of LangGraph")
    use_autogen: bool = Field(True, description="Use AutoGen critique")


class GenerateResponse(BaseModel):
    """Response from manuscript generation."""
    manuscript: str = Field(..., description="Generated manuscript text")
    word_count: int = Field(..., description="Word count")
    chapters: int = Field(..., description="Number of chapters")
    framework: str = Field(..., description="Framework used")
    genre: str = Field(..., description="Genre")
    status: str = Field("success", description="Generation status")


class IngestRequest(BaseModel):
    """Request to ingest from GitHub."""
    repo: str = Field(..., description="GitHub repo (owner/repo)")
    include_readme: bool = Field(True, description="Include README files")


class IngestResponse(BaseModel):
    """Response from GitHub ingestion."""
    content: str = Field(..., description="Ingested content")
    file_count: int = Field(..., description="Number of files")
    total_chars: int = Field(..., description="Total characters")
    files: list[str] = Field(..., description="File names")


class FrameworkInfo(BaseModel):
    """Information about a story framework."""
    name: str
    description: str
    stages: list[str] = []
    beats: list[str] = []


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    config: dict


# =============================================================================
# APP LIFECYCLE
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """App lifespan handler."""
    # Startup
    config = get_config()
    print(f"🚀 Opus API starting...")
    print(f"   Provider: {config.agent.provider}")
    print(f"   Model: {config.agent.model}")
    yield
    # Shutdown
    print("\n👋 Opus API shutting down...")


# =============================================================================
# CREATE APP
# =============================================================================

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Opus Orchestrator API",
        description="""Full-flow AI book generation API using LangGraph, CrewAI, AutoGen, and PydanticAI.
        
## Features

- **Multiple Frameworks**: Snowflake Method, Hero's Journey, Save the Cat, Three-Act, Story Circle, 7-Point, Fichtean
- **CrewAI Integration**: Agent crews for writing, editing, proofreading
- **AutoGen Critique**: Multi-agent debate for editorial feedback
- **PydanticAI Validation**: Structured output validation
- **GitHub Ingestion**: Pull content from repositories

## Quick Start

1. Generate a manuscript:
```bash
curl -X POST "http://localhost:8000/generate" \\
  -H "Content-Type: application/json" \\
  -d '{"concept": "A robot dreams of love", "target_word_count": 1000}'
```

2. Ingest from GitHub:
```bash
curl -X POST "http://localhost:8000/ingest" \\
  -H "Content-Type: application/json" \\
  -d '{"repo": "owner/my-book-notes"}'
```
""",
        version="0.2.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    
    return app


app = create_app()


# =============================================================================
# ROUTES
# =============================================================================

@app.get("/", tags=["root"])
async def root():
    """Redirect to documentation."""
    return RedirectResponse(url="/docs")


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health():
    """Health check endpoint."""
    config = get_config()
    return HealthResponse(
        status="healthy",
        version="0.2.0",
        config={
            "provider": config.agent.provider,
            "model": config.agent.model,
            "github_token_set": bool(config.github_token),
        },
    )


@app.get("/frameworks", response_model=dict[str, FrameworkInfo], tags=["frameworks"])
async def list_frameworks():
    """List all available story frameworks."""
    result = {}
    for framework, info in FRAMEWORKS.items():
        name = info.get("name", framework.value if hasattr(framework, "value") else str(framework))
        result[name.lower().replace(" ", "_")] = FrameworkInfo(
            name=name,
            description=info.get("description", ""),
            stages=info.get("stages", []),
            beats=[b[0] if isinstance(b, tuple) else b for b in info.get("beats", [])],
        )
    return result


@app.post("/generate", response_model=GenerateResponse, tags=["generate"])
async def generate(request: GenerateRequest, background_tasks: BackgroundTasks):
    """Generate a manuscript from concept or GitHub repo."""
    try:
        # Prepare seed concept
        seed_concept = request.concept
        
        if request.repo:
            # Ingest from GitHub
            orch = OpusOrchestrator(
                book_type=request.book_type,
                genre=request.genre,
                target_word_count=request.target_word_count,
                framework=request.framework,
            )
            content = orch.ingest_from_github(request.repo)
            seed_concept = content.text
        
        if not seed_concept:
            raise HTTPException(status_code=400, detail="Must provide concept or repo")
        
        # Generate
        result = await run_opus(
            seed_concept=seed_concept,
            framework=request.framework,
            genre=request.genre,
            target_word_count=request.target_word_count,
            use_autogen=request.use_autogen,
        )
        
        manuscript = result.get("manuscript", str(result))
        word_count = len(manuscript.split())
        
        return GenerateResponse(
            manuscript=manuscript,
            word_count=word_count,
            chapters=request.chapters,
            framework=request.framework,
            genre=request.genre,
            status="success",
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest", response_model=IngestResponse, tags=["ingest"])
async def ingest(request: IngestRequest):
    """Ingest content from a GitHub repository."""
    try:
        orch = OpusOrchestrator(book_type="fiction")
        content = orch.ingest_from_github(
            request.repo, 
            include_readme=request.include_readme
        )
        
        return IngestResponse(
            content=content.text,
            file_count=content.metadata["file_count"],
            total_chars=len(content.text),
            files=content.metadata["files"],
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# SERVER RUNNER
# =============================================================================

async def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the API server."""
    import uvicorn
    
    uvicorn.run(
        "opus_orchestrator.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )


def get_openapi_spec(format: str = "yaml") -> str:
    """Get OpenAPI specification."""
    import json
    
    spec = app.openapi()
    
    if format == "json":
        return json.dumps(spec, indent=2)
    else:
        # Convert to YAML-like format
        import yaml
        return yaml.dump(spec, default_flow_style=False)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    import uvicorn
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
