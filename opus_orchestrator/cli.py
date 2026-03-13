#!/usr/bin/env python3
"""Opus Orchestrator CLI.

Standalone CLI for running Opus book generation without OpenClaw.

Usage:
    opus --help
    opus generate --concept "Your story idea"
    opus serve --port 8000  # Start API server
    opus docs               # Show documentation
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


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
  opus docs
  opus ingest --repo mrhavens/my-book
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="Opus Orchestrator AI v0.2.0",
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
        help="Output file path",
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
    # INGEST COMMAND
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
    
    # Determine the seed concept
    seed_concept = args.concept
    
    if args.repo:
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
    
    # Save output
    output_path = args.output
    if not output_path:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"opus_manuscript_{timestamp}.md"
    
    with open(output_path, "w") as f:
        f.write(f"# Opus Generated Manuscript\n\n")
        f.write(f"Framework: {args.framework}\n")
        f.write(f"Genre: {args.genre}\n")
        f.write(f"Type: {args.book_type}\n")
        f.write(f"Chapters: {args.chapters}\n")
        f.write(f"Target Words: {args.words:,}\n\n")
        f.write(f"---\n\n")
        f.write(manuscript)
    
    word_count = len(manuscript.split())
    
    print(f"\n{'='*60}")
    print(f"✅ COMPLETE!")
    print(f"   Words: {word_count:,}")
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


def run_ingest(args: argparse.Namespace) -> int:
    """Ingest content from GitHub."""
    from opus_orchestrator import OpusOrchestrator
    
    print(f"\n📥 Ingesting from GitHub: {args.repo}\n")
    
    orch = OpusOrchestrator(book_type="fiction")
    content = orch.ingest_from_github(args.repo, include_readme=args.include_readme)
    
    print(f"✅ Loaded {len(content.text):,} characters")
    print(f"   Files: {content.metadata['file_count']}")
    print(f"   File list: {', '.join(content.metadata['files'])}\n")
    
    if args.preview:
        print("📄 PREVIEW (first 2000 chars):")
        print("-" * 40)
        print(content.text[:2000])
        print("-" * 40)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(content.text)
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
        "ingest": run_ingest,
        "frameworks": run_frameworks,
        "config": run_config,
        "docs": run_docs,
        "api": run_api,
    }
    
    if args.command in commands:
        if args.command in ["generate", "serve"]:
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
