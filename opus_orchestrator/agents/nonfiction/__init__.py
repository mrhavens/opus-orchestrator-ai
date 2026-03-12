"""Nonfiction agents for Opus Orchestrator.

Based on Nonfiction Fortress Level 1-3 methodology.
"""

from opus_orchestrator.agents.nonfiction.researcher import (
    AnalystAgent,
    FactCheckerAgent,
    NonfictionEditorAgent,
    NonfictionWriterAgent,
    ResearcherAgent,
)

__all__ = [
    "ResearcherAgent",
    "AnalystAgent",
    "NonfictionWriterAgent",
    "FactCheckerAgent",
    "NonfictionEditorAgent",
]
