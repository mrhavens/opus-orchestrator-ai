"""Utility functions for Opus Orchestrator."""

from opus_orchestrator.utils.docs import generate_docs
from opus_orchestrator.utils.github_ingest import GitHubIngestor, create_github_ingestor
from opus_orchestrator.utils.s3_ingest import S3Ingestor, create_s3_ingestor
from opus_orchestrator.utils.local_ingest import LocalIngestor, create_local_ingestor
from opus_orchestrator.utils.llm import get_llm_client
from opus_orchestrator.utils.research import (
    ResearchOrchestrator,
    SearchTool,
    WikipediaTool,
    AcademicSearchTool,
    create_research_orchestrator,
)

__all__ = [
    "generate_docs",
    "GitHubIngestor",
    "create_github_ingestor",
    "S3Ingestor",
    "create_s3_ingestor",
    "LocalIngestor",
    "create_local_ingestor",
    "get_llm_client",
    # Research (NEW!)
    "ResearchOrchestrator",
    "SearchTool",
    "WikipediaTool",
    "AcademicSearchTool",
    "create_research_orchestrator",
]
