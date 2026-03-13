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
from opus_orchestrator.agents.nonfiction.purpose_writers import (
    get_writer_for_purpose,
    select_writer_agent,
    list_available_writers,
    PURPOSE_WRITERS,
)

__all__ = [
    "ResearcherAgent",
    "AnalystAgent",
    "NonfictionWriterAgent",
    "FactCheckerAgent",
    "NonfictionEditorAgent",
    # Purpose-specific writers
    "get_writer_for_purpose",
    "select_writer_agent",
    "list_available_writers",
    "PURPOSE_WRITERS",
]
