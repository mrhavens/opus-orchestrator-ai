#!/usr/bin/env python3
"""Opus Orchestrator CLI.

Standalone CLI for running Opus book generation without OpenClaw.

Usage:
    opus --help
    opus generate --concept "Your story idea"
    opus serve --port 8000  # Start API server
    opus docs               # Show documentation
    
    # Or use as API client:
    opus --api-url http://localhost:8000 generate --concept "..."

Local mode (default): Runs generation locally using LangGraph/CrewAI
API mode: Sends requests to Opus API server

Usage:
    opus [GLOBAL_OPTIONS] <command> [OPTIONS]

Examples:
  # Local generation
  opus generate --concept "A robot dreams of love"
  
  # API client mode
  opus --api-url http://localhost:8000 generate --concept "..."
  opus --api-url https://opus-api.example.com generate --repo owner/repo
        """

import argparse
import asyncio
import os
import sys
import json
import requests
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


# =============================================================================
# API CLIENT
# =============================================================================

class OpusAPIClient:
    """Client for Opus REST API."""
    
    def __init__(self, base_url: str):
        """Initialize API client.
        
        Args:
            base_url: Base URL of Opus API server
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def health(self) -> dict:
        """Check API health."""
        return self._get("/health")
    
    def frameworks(self) -> dict:
        """List available frameworks."""
        return self._get("/frameworks")
    
    def generate(
        self,
        concept: str = None,
        repo: str = None,
        framework: str = "snowflake",
        genre: str = "fiction",
        book_type: str = "fiction",
        target_word_count: int = 5000,
        chapters: int = 3,
        tone: str = "literary",
        use_crewai: bool = False,
        use_autogen: bool = True,
    ) -> dict:
        """Generate a manuscript.
        
        Args:
            concept: Seed concept
            repo: GitHub repo to ingest
            framework: Story framework
            genre: Genre
            book_type: Book type
            target_word_count: Target word count
            chapters: Number of chapters
            tone: Writing tone
            use_crewai: Use CrewAI
            use_autogen: Use AutoGen critique
            
        Returns:
            Generation result dict
        """
        payload = {
            "framework": framework,
            "genre": genre,
            "book_type": book_type,
            "target_word_count": target_word_count,
            "chapters": chapters,
            "tone": tone,
            "use_crewai": use_crewai,
        }
        
        if concept:
            payload["concept"] = concept
        if repo:
            payload["repo"] = repo
        
        return self._post("/generate", payload)
    
    def ingest(self, repo: str, include_readme: bool = True) -> dict:
        """Ingest from GitHub.
        
        Args:
            repo: GitHub repo (owner/repo)
            include_readme: Include README files
            
        Returns:
            Ingested content
        """
        return self._post("/ingest", {
            "repo": repo,
            "include_readme": include_readme,
        })
    
    def _get(self, endpoint: str) -> dict:
        """GET request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def _post(self, endpoint: str, data: dict) -> dict:
        """POST request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()


def get_api_client(api_url: str = None) -> OpusAPIClient | None:
    """Get API client if URL provided.
    
    Args:
        api_url: API base URL
        
    Returns:
        OpusAPIClient or None
    """
    if api_url:
        return OpusAPIClient(api_url)
    return None


def setup_cli() -> argparse.ArgumentParser:
    """Set up the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="opus",
        description="""Opus Orchestrator AI - Full-flow AI book generation

A comprehensive book generation system using LangGraph, CrewAI, AutoGen, 
and PydanticAI for professional manuscript production.

Examples:
  opus generate --concept "A robot dreams of love" --framework snowflake
  opus serve --port 8080
  opus --api-url http://localhost:8000 generate --concept "..."
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="Opus Orchestrator AI v0.2.0",
    )
    
    # Global option for API client mode
    parser.add_argument(
        "--api-url",
        help="Use API server at this URL (client mode). Without this, runs locally.",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # -------------------------------------------------------------------------
    # GENERATE COMMAND
    # -------------------------------------------------------------------------
    gen_parser = subparsers.add_parser(
        "generate",
        help="Generate a book/manuscript",
        description="Generate a complete manuscript from a concept or GitHub repo",
    )
    gen_parser.add_argument(
        "--concept", "-c",
        help="Seed concept or story idea",
    )
    gen_parser.add_argument(
        "--repo", "-r",
        help="GitHub repo to ingest (owner/repo format)",
    )
    gen_parser.add_argument(
        "--framework", "-f",
        default="snowflake",
        choices=["snowflake", "three-act", "save-the-cat", "hero-journey", 
                 "story-circle", "seven-point", "fichtean"],
        help="Story framework to use",
    )
    gen_parser.add_argument(
        "--genre", "-g",
        default="fiction",
        help="Genre (fiction, nonfiction, sci-fi, fantasy, romance, etc.)",
    )
    gen_parser.add_argument(
        "--type", "-t",
        dest="book_type",
        default="fiction",
        choices=["fiction", "nonfiction"],
        help="Book type",
    )
    gen_parser.add_argument(
        "--words", "-w",
        type=int,
        default=5000,
        help="Target word count (default: 5000)",
    )
    gen_parser.add_argument(
        "--chapters", "-n",
        type=int,
        default=3,
        help="Number of chapters (default: 3)",
    )
    gen_parser.add_argument(
        "--tone",
        default="literary",
        help="Writing tone (default: literary)",
    )
    gen_parser.add_argument(
        "--output", "-o",
        help="Output file path (local)",
    )
    gen_parser.add_argument(
        "--save-s3",
        help="Save to S3 bucket (bucket/path format)",
    )
    gen_parser.add_argument(
        "--save-s3-endpoint",
        help="S3 endpoint URL (for MinIO, DO Spaces, etc.)",
    )
    gen_parser.add_argument(
        "--save-repo",
        help="Save to GitHub repo (owner/repo format)",
    )
    gen_parser.add_argument(
        "--save-branch",
        default="main",
        help="GitHub branch to commit to (default: main)",
    )
    gen_parser.add_argument(
        "--save-commit-msg",
        help="Commit message for GitHub save",
    )
    gen_parser.add_argument(
        "--local",
        "-l",
        help="Local file or directory to use as source",
    )
    gen_parser.add_argument(
        "--use-crewai",
        action="store_true",
        help="Use CrewAI crews instead of LangGraph",
    )
    gen_parser.add_argument(
        "--no-autogen",
        action="store_true",
        help="Disable AutoGen critique",
    )
    gen_parser.add_argument(
        "--verbose", "-V",
        action="store_true",
        help="Enable verbose output",
    )
    
    # -------------------------------------------------------------------------
    # SERVE COMMAND (OpenAPI Server)
    # -------------------------------------------------------------------------
    serve_parser = subparsers.add_parser(
        "serve",
        help="Start OpenAPI REST server",
        description="Start a REST API server with OpenAPI documentation",
    )
    serve_parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)",
    )
    serve_parser.add_argument(
        "--port", "-p",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)",
    )
    serve_parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload on code changes",
    )
    
    # -------------------------------------------------------------------------
    # UI COMMAND (Web Interface)
    # -------------------------------------------------------------------------
    ui_parser = subparsers.add_parser(
        "ui",
        help="Start web UI only (no API)",
        description="Start the novice-friendly web interface",
    )
    ui_parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)",
    )
    ui_parser.add_argument(
        "--port", "-p",
        type=int,
        default=8080,
        help="Port to bind to (default: 8080)",
    )
    
    # -------------------------------------------------------------------------
    # INGEST COMMAND (GitHub)
    # -------------------------------------------------------------------------
    ingest_parser = subparsers.add_parser(
        "ingest",
        help="Ingest content from GitHub",
        description="Fetch and analyze content from a GitHub repository",
    )
    ingest_parser.add_argument(
        "--repo", "-r",
        required=True,
        help="GitHub repo (owner/repo format)",
    )
    ingest_parser.add_argument(
        "--output", "-o",
        help="Output file for ingested content",
    )
    ingest_parser.add_argument(
        "--include-readme",
        action="store_true",
        default=True,
        help="Include README files (default: True)",
    )
    ingest_parser.add_argument(
        "--preview",
        action="store_true",
        help="Show preview of ingested content",
    )
    
    # -------------------------------------------------------------------------
    # INGEST-S3 COMMAND
    # -------------------------------------------------------------------------
    s3_parser = subparsers.add_parser(
        "ingest-s3",
        help="Ingest content from S3/MinIO",
        description="Fetch and analyze content from S3-compatible storage",
    )
    s3_parser.add_argument(
        "--bucket", "-b",
        required=True,
        help="S3 bucket name",
    )
    s3_parser.add_argument(
        "--prefix", "-p",
        default="",
        help="Object key prefix",
    )
    s3_parser.add_argument(
        "--endpoint", "-e",
        help="S3 endpoint URL (for MinIO, DO Spaces, etc.)",
    )
    s3_parser.add_argument(
        "--output", "-o",
        help="Output file for ingested content",
    )
    s3_parser.add_argument(
        "--preview",
        action="store_true",
        help="Show preview of ingested content",
    )
    s3_parser.add_argument(
        "--list-objects",
        action="store_true",
        help="List objects instead of downloading",
    )
    
    # -------------------------------------------------------------------------
    # INGEST-LOCAL COMMAND
    # -------------------------------------------------------------------------
    local_parser = subparsers.add_parser(
        "ingest-local",
        help="Ingest content from local files/directories",
        description="Fetch and analyze content from local files and directories",
    )
    local_parser.add_argument(
        "path",
        help="File or directory path to ingest",
    )
    local_parser.add_argument(
        "--extensions", "-e",
        help="Comma-separated file extensions (default: txt,md,markdown,notes,draft)",
    )
    local_parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Don't scan subdirectories",
    )
    local_parser.add_argument(
        "--output", "-o",
        help="Output file for ingested content",
    )
    local_parser.add_argument(
        "--preview",
        action="store_true",
        help="Show preview of ingested content",
    )
    local_parser.add_argument(
        "--summarize",
        action="store_true",
        help="Summarize content instead of full ingest",
    )
    local_parser.add_argument(
        "--max-length",
        type=int,
        default=10000,
        help="Max length for summary (default: 10000)",
    )
    
    # -------------------------------------------------------------------------
    # FRAMEWORKS COMMAND
    # -------------------------------------------------------------------------
    subparsers.add_parser(
        "frameworks",
        help="List available story frameworks",
        description="Show all available story frameworks with descriptions",
    )
    
    # -------------------------------------------------------------------------
    # CONFIG COMMAND
    # -------------------------------------------------------------------------
    config_parser = subparsers.add_parser(
        "config",
        help="Show configuration",
        description="Display current configuration settings",
    )
    config_parser.add_argument(
        "--show-keys",
        action="store_true",
        help="Show API keys (masked)",
    )
    config_parser.add_argument(
        "--env",
        action="store_true",
        help="Show environment variables needed",
    )
    
    # -------------------------------------------------------------------------
    # DOCS COMMAND
    # -------------------------------------------------------------------------
    docs_parser = subparsers.add_parser(
        "docs",
        help="Show documentation",
        description="Display comprehensive documentation",
    )
    docs_parser.add_argument(
        "--format", "-f",
        choices=["terminal", "markdown", "html"],
        default="terminal",
        help="Output format (default: terminal)",
    )
    docs_parser.add_argument(
        "--output", "-o",
        help="Output file path",
    )
    
    # -------------------------------------------------------------------------
    # API COMMAND
    # -------------------------------------------------------------------------
    api_parser = subparsers.add_parser(
        "api",
        help="Show OpenAPI specification",
        description="Display or export OpenAPI schema",
    )
    api_parser.add_argument(
        "--format", "-f",
        choices=["json", "yaml"],
        default="yaml",
        help="Output format (default: yaml)",
    )
    api_parser.add_argument(
        "--output", "-o",
        help="Output file path",
    )
    
    return parser


async def run_generate(args: argparse.Namespace) -> int:
    """Run the generation command."""
    from opus_orchestrator import run_opus, OpusOrchestrator
    from opus_orchestrator.crews import create_fiction_crew, create_nonfiction_crew
    
    print(f"\n{'='*60}")
    print("📚 OPUS ORCHESTRATOR AI")
    print(f"{'='*60}\n")
    
    # Check for API client mode
    if args.api_url:
        client = OpusAPIClient(args.api_url)
        
        print(f"🌐 API Client Mode")
        print(f"   Server: {args.api_url}\n")
        
        # Call API
        try:
            result = client.generate(
                concept=args.concept,
                repo=args.repo,
                framework=args.framework,
                genre=args.genre,
                book_type=args.book_type,
                target_word_count=args.words,
                chapters=args.chapters,
                tone=args.tone,
                use_crewai=args.use_crewai,
                use_autogen=not args.no_autogen,
            )
            
            print(f"✅ Generation complete!")
            print(f"   Words: {result.get('word_count', 'N/A'):,}")
            print(f"   Chapters: {result.get('chapters', 'N/A')}")
            print(f"   Framework: {result.get('framework', 'N/A')}\n")
            
            manuscript = result.get("manuscript", "")
            
        except Exception as e:
            print(f"❌ API Error: {e}")
            return 1
    else:
        # LOCAL MODE - run locally
        # Determine the seed concept
        seed_concept = args.concept
        
        if args.local:
            # Ingest from local files/directory
            from opus_orchestrator import LocalIngestor
            
            print(f"📂 Ingesting from local: {args.local}")
            
            ingestor = LocalIngestor()
            result = ingestor.ingest(args.local)
            
            full_text = result["combined_text"]
            print(f"   ✅ Loaded {len(full_text):,} characters from {result['file_count']} files")
            print(f"   📄 Files: {', '.join(list(result['files'].keys())[:5])}")
            if result['file_count'] > 5:
                print(f"   ... and {result['file_count'] - 5} more")
            print()
            
            seed_concept = full_text
        elif args.repo:
            # Ingest from GitHub - use FULL content
            print(f"📥 Ingesting from GitHub: {args.repo}")
            
            orch = OpusOrchestrator(
                book_type=args.book_type,
                genre=args.genre,
                target_word_count=args.words,
                framework=args.framework,
            )
            
            content = orch.ingest_from_github(args.repo)
            
            # Use full content as seed
            full_text = content.text
            print(f"   ✅ Loaded {len(full_text):,} characters from {content.metadata['file_count']} files")
            print(f"   📄 Files: {', '.join(content.metadata['files'])}\n")
            
            seed_concept = full_text
        
        if not seed_concept:
            print("Error: Please provide --concept or --repo")
            return 1
        
        # Show generation parameters
        print(f"🏠 Local Mode")
        print(f"🎯 Generating {args.words:,} words ({args.chapters} chapters)")
        print(f"   Framework: {args.framework}")
        print(f"   Genre: {args.genre}")
        print(f"   Type: {args.book_type}")
        print(f"   Tone: {args.tone}")
        print(f"   CrewAI: {args.use_crewai}")
        print(f"   AutoGen: {not args.no_autogen}")
        print()
        
        use_autogen = not args.no_autogen
        
        if args.use_crewai:
            # Use CrewAI crews
            print("🛠️  Using CrewAI crews...\n")
            
            if args.book_type == "fiction":
                crew = create_fiction_crew(
                    genre=args.genre,
                    tone=args.tone,
                    target_word_count=args.words // args.chapters,
                )
                
                story = crew.write_full_story(
                    story_outline=seed_concept[:10000],  # Limit for crew context
                    character_sheets="",
                    style_guide=f"Tone: {args.tone}",
                    num_chapters=args.chapters,
                )
                
                manuscript = "\n\n---\n\n".join(story)
            else:
                crew = create_nonfiction_crew(
                    topic=args.genre,
                    tone=args.tone,
                    target_word_count=args.words,
                )
                
                manuscript = crew.write_section(
                    section_outline=seed_concept[:10000],
                    style_guide=f"Tone: {args.tone}",
                )
        else:
            # Use LangGraph pipeline
            result = await run_opus(
                seed_concept=seed_concept,
                framework=args.framework,
                genre=args.genre,
                target_word_count=args.words,
                use_autogen=use_autogen,
            )
            
            manuscript = result.get("manuscript", str(result))
    
    # Build full manuscript content with metadata
    manuscript_content = f"""# Opus Generated Manuscript

Framework: {args.framework}
Genre: {args.genre}
Type: {args.book_type}
Chapters: {args.chapters}
Target Words: {args.words:,}

---

{manuscript}
"""
    
    word_count = len(manuscript.split())
    
    # Save to local file
    output_path = args.output
    if output_path or args.save_s3 or args.save_repo:
        # Determine filename
        if not output_path:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"opus_manuscript_{timestamp}.md"
        
        with open(output_path, "w") as f:
            f.write(manuscript_content)
        
        print(f"   💾 Saved locally: {output_path}")
    
    # Save to S3
    if args.save_s3:
        from opus_orchestrator import S3Ingestor
        
        bucket, key = args.save_s3.split("/", 1) if "/" in args.save_s3 else (args.save_s3, "")
        if not key:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            key = f"manuscripts/opus_{timestamp}.md"
        
        print(f"   🪣 Saving to S3: {bucket}/{key}")
        
        s3 = S3Ingestor(endpoint_url=args.save_s3_endpoint, bucket=bucket)
        
        # Upload the manuscript content
        import io
        from botocore.config import Config
        
        s3.s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=manuscript_content.encode("utf-8"),
            ContentType="text/markdown",
        )
        
        print(f"   ✅ Uploaded to S3: s3://{bucket}/{key}")
    
    # Save to GitHub repo
    if args.save_repo:
        import requests
        
        print(f"   📤 Saving to GitHub: {args.save_repo}")
        
        github_token = os.environ.get("GITHUB_TOKEN")
        if not github_token:
            print("   ⚠️  GITHUB_TOKEN not set, cannot save to repo")
        else:
            # Parse owner/repo
            owner, repo = args.save_repo.split("/")
            
            # Create filename
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"manuscript_{timestamp}.md"
            
            # Get current branch
            branch = args.save_branch
            
            # Create/update file via GitHub API
            import base64
            
            api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/manuscripts/{filename}"
            
            headers = {
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json",
            }
            
            # Check if file exists to get SHA
            existing = requests.get(api_url, headers=headers)
            sha = existing.json().get("sha") if existing.status_code == 200 else None
            
            # Create content
            content_b64 = base64.b64encode(manuscript_content.encode("utf-8")).decode("utf-8")
            
            data = {
                "message": args.save_commit_msg or f"Add generated manuscript: {filename}",
                "content": content_b64,
                "branch": branch,
            }
            if sha:
                data["sha"] = sha
            
            resp = requests.put(api_url, headers=headers, json=data)
            
            if resp.status_code in [200, 201]:
                print(f"   ✅ Committed to GitHub: {args.save_repo}/manuscripts/{filename}")
            else:
                print(f"   ⚠️  GitHub save failed: {resp.status_code} - {resp.text}")
    
    print(f"\n{'='*60}")
    print(f"✅ COMPLETE!")
    print(f"   Words: {word_count:,}")
    if not args.output and not args.save_s3 and not args.save_repo:
        print(f"   Output: {output_path}")
    print(f"{'='*60}\n")
    
    return 0


async def run_serve(args: argparse.Namespace) -> int:
    """Start the OpenAPI server."""
    print(f"\n🚀 Starting Opus API Server...")
    print(f"   Host: {args.host}")
    print(f"   Port: {args.port}")
    print(f"   Docs: http://{args.host}:{args.port}/docs\n")
    
    try:
        from opus_orchestrator.server import run_server
        await run_server(host=args.host, port=args.port, reload=args.reload)
    except ImportError:
        print("Error: Run `pip install fastapi uvicorn` to enable API server")
        return 1
    
    return 0


async def run_ui(args: argparse.Namespace) -> int:
    """Start the web UI only."""
    print(f"\n🎨 Starting Opus Web UI...")
    print(f"   Host: {args.host}")
    print(f"   Port: {args.port}")
    print(f"   UI: http://{args.host}:{args.port}/\n")
    
    try:
        from opus_orchestrator.server import create_app
        import uvicorn
        
        app = create_app(include_ui=True)
        config = uvicorn.Config(app, host=args.host, port=args.port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()
    except ImportError as e:
        print(f"Error: {e}")
        print("Run `pip install fastapi uvicorn` to enable web UI")
        return 1
    
    return 0


def run_ingest(args: argparse.Namespace) -> int:
    """Ingest content from GitHub."""
    from opus_orchestrator import OpusOrchestrator
    
    print(f"\n📥 Ingesting from GitHub: {args.repo}\n")
    
    # Check for API client mode
    if args.api_url:
        client = OpusAPIClient(args.api_url)
        print(f"🌐 API Client Mode: {args.api_url}\n")
        
        try:
            result = client.ingest(args.repo, include_readme=args.include_readme)
            content_text = result.get("content", "")
            file_count = result.get("file_count", 0)
            files = result.get("files", [])
        except Exception as e:
            print(f"❌ API Error: {e}")
            return 1
    else:
        # Local mode
        orch = OpusOrchestrator(book_type="fiction")
        content = orch.ingest_from_github(args.repo, include_readme=args.include_readme)
        content_text = content.text
        file_count = content.metadata["file_count"]
        files = content.metadata["files"]
    
    print(f"✅ Loaded {len(content_text):,} characters")
    print(f"   Files: {file_count}")
    print(f"   File list: {', '.join(files)}\n")
    
    if args.preview:
        print("📄 PREVIEW (first 2000 chars):")
        print("-" * 40)
        print(content_text[:2000])
        print("-" * 40)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(content_text)
        print(f"\n💾 Saved to: {args.output}")
    
    return 0


def run_s3_ingest(args: argparse.Namespace) -> int:
    """Ingest content from S3/MinIO."""
    from opus_orchestrator import S3Ingestor
    
    print(f"\n🪣 Ingesting from S3: {args.bucket}/{args.prefix}\n")
    
    if args.endpoint:
        print(f"   Endpoint: {args.endpoint}")
    
    ingestor = S3Ingestor(
        endpoint_url=args.endpoint,
        bucket=args.bucket,
    )
    
    if args.list_objects:
        # Just list objects
        objects = ingestor.list_objects(bucket=args.bucket, prefix=args.prefix)
        print(f"📦 Objects ({len(objects)}):")
        for obj in objects[:20]:
            print(f"   {obj['key']} ({obj['size']:,} bytes)")
        if len(objects) > 20:
            print(f"   ... and {len(objects) - 20} more")
        return 0
    
    # Ingest content
    result = ingestor.ingest_bucket(
        bucket=args.bucket,
        prefix=args.prefix,
    )
    
    print(f"✅ Loaded {result['total_chars']:,} characters")
    print(f"   Files: {result['file_count']}")
    print(f"   File list: {', '.join(result['files'].keys())}\n")
    
    if args.preview:
        print("📄 PREVIEW (first 2000 chars):")
        print("-" * 40)
        print(result["combined_text"][:2000])
        print("-" * 40)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(result["combined_text"])
        print(f"\n💾 Saved to: {args.output}")
    
    return 0


def run_local_ingest(args: argparse.Namespace) -> int:
    """Ingest content from local files/directories."""
    from opus_orchestrator import LocalIngestor
    
    print(f"\n📂 Ingesting from local: {args.path}\n")
    
    # Parse extensions
    extensions = None
    if args.extensions:
        extensions = [ext.strip() for ext in args.extensions.split(",")]
    
    # Create ingestor
    ingestor = LocalIngestor()
    
    # Ingest
    result = ingestor.ingest(
        path=args.path,
        extensions=extensions,
        recursive=not args.no_recursive,
    )
    
    if args.summarize:
        content = ingestor.summarize(result["combined_text"], args.max_length)
    else:
        content = result["combined_text"]
    
    print(f"✅ Loaded {result['total_chars']:,} characters")
    print(f"   Files: {result['file_count']}")
    print(f"   Root: {result['path']}")
    
    files_list = list(result["files"].keys())
    print(f"   File list: {', '.join(files_list[:10])}")
    if len(files_list) > 10:
        print(f"   ... and {len(files_list) - 10} more")
    
    if args.summarize:
        print(f"   📝 Summarized to {args.max_length} characters")
    
    print()
    
    if args.preview:
        print("📄 PREVIEW (first 2000 chars):")
        print("-" * 40)
        print(content[:2000])
        print("-" * 40)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(content)
        print(f"\n💾 Saved to: {args.output}")
    
    return 0


def run_frameworks(args: argparse.Namespace) -> int:
    """List available frameworks."""
    from opus_orchestrator.frameworks import FRAMEWORKS
    
    print("\n📚 AVAILABLE STORY FRAMEWORKS\n")
    print("=" * 50)
    
    for framework, info in FRAMEWORKS.items():
        name = info.get("name", framework.value if hasattr(framework, "value") else str(framework))
        desc = info.get("description", "")
        stages = info.get("stages", [])
        beats = info.get("beats", [])
        
        print(f"\n{name}")
        print(f"  {desc}")
        
        if stages:
            print(f"  Stages: {len(stages)}")
            for i, stage in enumerate(stages[:3], 1):
                print(f"    {i}. {stage}")
            if len(stages) > 3:
                print(f"    ... and {len(stages) - 3} more")
        
        if beats:
            print(f"  Beats: {len(beats)}")
            for beat in beats[:3]:
                print(f"    • {beat}")
            if len(beats) > 3:
                print(f"    ... and {len(beats) - 3} more")
    
    print("\n" + "=" * 50)
    return 0


def run_config(args: argparse.Namespace) -> int:
    """Show configuration."""
    from opus_orchestrator.config import get_config
    
    config = get_config()
    
    print("\n⚙️  OPUS CONFIGURATION\n")
    print("=" * 40)
    
    print(f"\n🔹 Agent")
    print(f"   Provider: {config.agent.provider}")
    print(f"   Model: {config.agent.model}")
    print(f"   Temperature: {config.agent.temperature}")
    print(f"   Max Tokens: {config.agent.max_tokens or 'None'}")
    
    print(f"\n🔹 Iteration")
    print(f"   Min Critic Rounds: {config.iteration.min_critic_rounds}")
    print(f"   Max Critic Rounds: {config.iteration.max_critic_rounds}")
    print(f"   Approval Threshold: {config.iteration.approval_threshold}")
    
    print(f"\n🔹 Output")
    print(f"   Format: {config.output.format}")
    print(f"   Include TOC: {config.output.include_toc}")
    print(f"   Output Dir: {config.output.output_dir}")
    
    print(f"\n🔹 Integrations")
    print(f"   GitHub Token: {'✓ Set' if config.github_token else '✗ Not Set'}")
    print(f"   API Key: {'✓ Set' if config.agent.api_key else '✗ Not Set'}")
    
    if args.show_keys:
        print(f"\n🔹 API Keys (unmasked)")
        print(f"   OPENAI_API_KEY: {os.environ.get('OPENAI_API_KEY', 'Not Set')[:20]}...")
        print(f"   MINIMAX_API_KEY: {os.environ.get('MINIMAX_API_KEY', 'Not Set')[:20]}...")
        print(f"   GITHUB_TOKEN: {os.environ.get('GITHUB_TOKEN', 'Not Set')[:20]}...")
    
    if args.env:
        print(f"\n📋 ENVIRONMENT VARIABLES NEEDED:")
        print("-" * 40)
        print("OPENAI_API_KEY=sk-...  # Required for LLM")
        print("GITHUB_TOKEN=ghp_...   # For private repos")
        print("MINIMAX_API_KEY=sk-...  # Optional alternative")
    
    print()
    return 0


def run_docs(args: argparse.Namespace) -> int:
    """Show documentation."""
    from opus_orchestrator.utils.docs import generate_docs
    
    docs = generate_docs(format=args.format)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(docs)
        print(f"📄 Documentation saved to: {args.output}")
    else:
        print(docs)
    
    return 0


def run_api(args: argparse.Namespace) -> int:
    """Show OpenAPI spec."""
    from opus_orchestrator.server import get_openapi_spec
    
    spec = get_openapi_spec(format=args.format)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(spec)
        print(f"📄 OpenAPI spec saved to: {args.output}")
    else:
        print(spec)
    
    return 0


async def main_async(args: argparse.Namespace) -> int:
    """Async main function."""
    commands = {
        "generate": run_generate,
        "serve": run_serve,
        "ui": run_ui,
        "ingest": run_ingest,
        "ingest-s3": run_s3_ingest,
        "ingest-local": run_local_ingest,
        "frameworks": run_frameworks,
        "config": run_config,
        "docs": run_docs,
        "api": run_api,
    }
    
    if args.command in commands:
        if args.command in ["generate", "serve", "ui"]:
            return await commands[args.command](args)
        else:
            return commands[args.command](args)
    else:
        # No command given, show help
        args.parser.print_help()
        return 0


def main():
    """Main entry point."""
    parser = setup_cli()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
