#!/usr/bin/env python3
"""Opus Orchestrator CLI.

Standalone CLI for running Opus book generation without OpenClaw.
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
        description="Opus Orchestrator AI - Full-flow AI book generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a short story
  opus generate --concept "A robot dreams of love" --framework snowflake --words 1000

  # Generate from GitHub repo
  opus generate --repo mrhavens/my-book-ideas --framework hero-journey

  # Run with specific genre
  opus generate --concept "Space opera adventure" --genre sci-fi --words 50000

  # List available frameworks
  opus frameworks
        """,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a book/manuscript")
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
        help="Target word count",
    )
    gen_parser.add_argument(
        "--tone",
        default="literary",
        help="Writing tone",
    )
    gen_parser.add_argument(
        "--output", "-o",
        help="Output file path",
    )
    gen_parser.add_argument(
        "--chapters", "-n",
        type=int,
        default=3,
        help="Number of chapters",
    )
    gen_parser.add_argument(
        "--use-crewai",
        action="store_true",
        help="Use CrewAI crews instead of direct agent calls",
    )
    gen_parser.add_argument(
        "--use-autogen",
        action="store_true",
        default=True,
        help="Use AutoGen for critique (default: True)",
    )
    
    # Frameworks command
    subparsers.add_parser(
        "frameworks",
        help="List available story frameworks",
    )
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Show configuration")
    config_parser.add_argument(
        "--show-keys",
        action="store_true",
        help="Show API keys (masked)",
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
        # Ingest from GitHub
        print(f"📥 Ingesting from GitHub: {args.repo}")
        
        orch = OpusOrchestrator(
            book_type=args.book_type,
            genre=args.genre,
            target_word_count=args.words,
            framework=args.framework,
        )
        
        content = orch.ingest_from_github(args.repo)
        seed_concept = content.text[:5000]  # Use first 5000 chars as seed
        
        print(f"   Loaded {len(content.text):,} characters\n")
    
    if not seed_concept:
        print("Error: Please provide --concept or --repo")
        return 1
    
    print(f"🎯 Generating {args.words:,} words")
    print(f"   Framework: {args.framework}")
    print(f"   Genre: {args.genre}")
    print(f"   Type: {args.book_type}")
    print(f"   CrewAI: {args.use_crewai}")
    print(f"   AutoGen: {args.use_autogen}")
    print()
    
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
                story_outline=seed_concept,
                character_sheets="",
                style_guide=f"Tone: {args.tone}",
                num_chapters=args.chapters,
            )
            
            # Combine chapters
            manuscript = "\n\n---\n\n".join(story)
        else:
            crew = create_nonfiction_crew(
                topic=args.genre,
                tone=args.tone,
                target_word_count=args.words,
            )
            
            manuscript = crew.write_section(
                section_outline=seed_concept,
                style_guide=f"Tone: {args.tone}",
            )
    else:
        # Use LangGraph pipeline
        result = await run_opus(
            seed_concept=seed_concept,
            framework=args.framework,
            genre=args.genre,
            target_word_count=args.words,
            use_autogen=args.use_autogen,
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
        f.write(f"Type: {args.book_type}\n\n")
        f.write(f"---\n\n")
        f.write(manuscript)
    
    word_count = len(manuscript.split())
    
    print(f"\n{'='*60}")
    print(f"✅ COMPLETE!")
    print(f"   Words: {word_count:,}")
    print(f"   Output: {output_path}")
    print(f"{'='*60}\n")
    
    return 0


def run_frameworks(args: argparse.Namespace) -> int:
    """List available frameworks."""
    from opus_orchestrator.frameworks import FRAMEWORKS
    
    print("\n📚 Available Story Frameworks:\n")
    
    for framework, info in FRAMEWORKS.items():
        name = info.get("name", framework.value if hasattr(framework, "value") else str(framework))
        desc = info.get("description", "")
        print(f"  {name}")
        if desc:
            print(f"    {desc}")
        print()
    
    return 0


def run_config(args: argparse.Namespace) -> int:
    """Show configuration."""
    from opus_orchestrator.config import get_config
    
    config = get_config()
    
    print("\n⚙️  Opus Configuration:\n")
    print(f"  Provider: {config.agent.provider}")
    print(f"  Model: {config.agent.model}")
    print(f"  Temperature: {config.agent.temperature}")
    print(f"  Max Tokens: {config.agent.max_tokens}")
    print(f"  GitHub Token: {'✓ Set' if config.github_token else '✗ Not Set'}")
    
    if args.show_keys:
        print(f"  API Key: {'✓ Set' if config.agent.api_key else '✗ Not Set'}")
    
    return 0


async def main_async(args: argparse.Namespace) -> int:
    """Async main function."""
    if args.command == "generate":
        return await run_generate(args)
    elif args.command == "frameworks":
        return run_frameworks(args)
    elif args.command == "config":
        return run_config(args)
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
    
    # Run async main
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
