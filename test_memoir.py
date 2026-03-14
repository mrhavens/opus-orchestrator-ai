#!/usr/bin/env python3
"""Test memoir ingestion."""

import asyncio
import os

# Set token
os.environ["GITHUB_TOKEN"] = "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"

async def main():
    from opus_orchestrator.nonfiction.intake import determine_intake
    from opus_orchestrator.nonfiction import ReaderPurpose
    
    print("=== Testing Memoir Sources ===\n")
    
    # 1. Determine purpose
    result = await determine_intake(
        concept="A memoir about love, loss, and transformation",
        purpose="transform",
        category="memoir"
    )
    print(f"1. PURPOSE: {result.purpose.value}")
    print(f"   Framework: {result.framework.get('name')}")
    print(f"   Stages: {len(result.framework.get('stages', []))}")
    print(f"   Source: {result.source}")
    
    # 2. Try GitHub sources
    print("\n2. Ingesting from GitHub...")
    from opus_orchestrator.utils.multi_source_ingest import ingest_multiple
    
    sources = [
        {"type": "github", "repo": "mrhavens/The-Last-Love-Story"},
    ]
    
    result = await ingest_multiple(sources)
    print(f"   Success: {result.successful_sources}/{result.total_sources}")
    print(f"   Content: {len(result.merged_content)} chars")

if __name__ == "__main__":
    asyncio.run(main())
