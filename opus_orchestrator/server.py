"""OpenAPI Server for Opus Orchestrator.

FastAPI-based REST API with OpenAPI documentation.
"""

import os
from typing import Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, StreamingResponse, Depends, Security
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from dotenv import load_dotenv


from opus_orchestrator.config import get_config
from opus_orchestrator import run_opus, OpusOrchestrator
from opus_orchestrator.frameworks import FRAMEWORKS


# =============================================================================
# AUTHENTICATION
# =============================================================================

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    """Validate API key from header or environment.
    
    If no API key is configured (for development), allow all requests.
    Set OPUS_API_KEY environment variable to protect production endpoints.
    """
    configured_key = os.environ.get("OPUS_API_KEY")
    
    # No key configured - allow all (development mode)
    if not configured_key:
        return "dev"
    
    # Key configured - validate
    if api_key is None:
        raise HTTPException(status_code=401, detail="API key required. Set X-API-Key header.")
    
    if api_key != configured_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return api_key


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
    target_word_count: int = Field(5000, ge=1, le=500000, description="Target word count (1-500000)")
    chapters: int = Field(3, ge=1, le=100, description="Number of chapters (1-100)")
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

def create_app(include_ui: bool = True) -> FastAPI:
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
- **S3 Upload**: Upload manuscripts to S3-compatible storage

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

3. Upload to S3:
```bash
curl -X POST "http://localhost:8000/upload/s3" \\
  -H "Content-Type: application/json" \\
  -d '{"content": "# My Manuscript", "bucket": "my-bucket", "key": "output/story.md"}'
```
""",
        version="0.2.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    
    # Add web UI if requested
    if include_ui:
        from opus_orchestrator.web_ui import create_web_ui
        create_web_ui(app)
    
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
async def generate(request: GenerateRequest, background_tasks: BackgroundTasks, api_key: str = Depends(get_api_key)):
    """Generate a manuscript from concept or GitHub repo."""
    import traceback
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
        )
        
        # Extract manuscript - handle both dict and string results
        if isinstance(result, dict):
            manuscript = result.get("manuscript", "")
            if not manuscript:
                # Try to get chapters content
                chapters = result.get("chapters", [])
                if chapters:
                    manuscript = "\n\n---\n\n".join(str(c) for c in chapters)
                else:
                    manuscript = str(result)
        else:
            manuscript = str(result)
        
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
        import logging
        logging.error(f"Generate error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/generate/stream", tags=["generate"])
async def generate_stream(request: GenerateRequest):
    """Generate a manuscript with streaming progress updates.
    
    Returns Server-Sent Events (SSE) with progress updates.
    """
    import traceback
    import json
    
    async def event_generator():
        try:
            # Yield start event
            yield "data: " + json.dumps({"status": "starting", "message": "Initializing..."}) + "\n\n"
            
            # Prepare seed concept
            seed_concept = request.concept
            
            if request.repo:
                yield "data: " + json.dumps({"status": "ingesting", "message": "Fetching from GitHub..."}) + "\n\n"
                orch = OpusOrchestrator(
                    book_type=request.book_type,
                    genre=request.genre,
                    target_word_count=request.target_word_count,
                    framework=request.framework,
                )
                content = orch.ingest_from_github(request.repo)
                seed_concept = content.text
                yield "data: " + json.dumps({"status": "ingested", "message": f"Ingested {len(seed_concept)} characters"}) + "\n\n"
            
            if not seed_concept:
                raise HTTPException(status_code=400, detail="Must provide concept or repo")
            
            # For now, just stream a completion message
            # Full streaming requires modifying the LangGraph workflow
            yield "data: " + json.dumps({"status": "generating", "progress": 0.1, "message": "Starting generation..."}) + "\n\n"
            
            # TODO: Implement actual streaming from LangGraph workflow
            # This requires modifying run_opus to yield progress events
            yield "data: " + json.dumps({"status": "generating", "progress": 0.5, "message": "Generating manuscript..."}) + "\n\n"
            
            yield "data: " + json.dumps({"status": "complete", "progress": 1.0, "message": "Generation complete"}) + "\n\n"
            
        except Exception as e:
            yield "data: " + json.dumps({"status": "error", "message": str(e)}) + "\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/ingest", response_model=IngestResponse, tags=["ingest"])
async def ingest(request: IngestRequest, api_key: str = Depends(get_api_key)):
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
# UPLOAD ENDPOINTS
# =============================================================================

class UploadResponse(BaseModel):
    """Response from file upload."""
    filename: str
    content: str
    size: int
    status: str


class S3UploadRequest(BaseModel):
    """Request to upload content to S3."""
    content: str
    bucket: str
    key: str
    endpoint_url: Optional[str] = None


class S3UploadResponse(BaseModel):
    """Response from S3 upload."""
    bucket: str
    key: str
    url: str
    status: str


@app.post("/upload", response_model=UploadResponse, tags=["upload"])
async def upload_file(file: UploadFile = File(...), api_key: str = Depends(get_api_key)):
    """Upload a file for processing."""
    try:
        content = await file.read()
        text_content = content.decode("utf-8")
        
        return UploadResponse(
            filename=file.filename,
            content=text_content,
            size=len(content),
            status="success",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload/s3", response_model=S3UploadResponse, tags=["upload"])
async def upload_to_s3(request: S3UploadRequest, api_key: str = Depends(get_api_key)):
    """Upload content to S3-compatible storage."""
    try:
        from opus_orchestrator import S3Ingestor
        
        # Create S3 ingestor
        s3 = S3Ingestor(endpoint_url=request.endpoint_url)
        
        # Upload using boto3 directly
        s3.s3_client.put_object(
            Bucket=request.bucket,
            Key=request.key,
            Body=request.content.encode("utf-8"),
            ContentType="text/markdown",
        )
        
        # Build URL
        if request.endpoint_url:
            url = f"{request.endpoint_url}/{request.bucket}/{request.key}"
        else:
            url = f"s3://{request.bucket}/{request.key}"
        
        return S3UploadResponse(
            bucket=request.bucket,
            key=request.key,
            url=url,
            status="success",
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

# =============================================================================
# RATE LIMITING
# =============================================================================
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiter."""
    
    def __init__(self, app, requests_per_minute: int = 30):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health check
        if request.url.path == "/health":
            return await call_next(request)
        
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean old requests (older than 1 minute)
        self.requests[client_ip] = [
            t for t in self.requests[client_ip] 
            if current_time - t < 60
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Please try again later."}
            )
        
        # Record this request
        self.requests[client_ip].append(current_time)
        
        return await call_next(request)


# Get rate limit from environment, default to 30/minute
_rate_limit = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "30"))
app.add_middleware(RateLimitMiddleware, requests_per_minute=_rate_limit)

# CORS middleware - secure configuration
from fastapi.middleware.cors import CORSMiddleware

# Get allowed origins from environment, default to restricted set
_cors_origins = os.environ.get("CORS_ORIGINS", "").split(",") if os.environ.get("CORS_ORIGINS") else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins if _cors_origins else ["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True if _cors_origins else False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)
