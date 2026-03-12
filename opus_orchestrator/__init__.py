"""Opus Orchestrator AI.

Full-flow AI book generation using LangGraph, CrewAI, AutoGen, and PydanticAI.
Integrates Fiction Fortress and Nonfiction Fortress methodologies.
"""

from opus_orchestrator.agents.fiction import (
    ArchitectAgent,
    CharacterLeadAgent,
    EditorAgent,
    VoiceAgent,
    WorldsmithAgent,
)
from opus_orchestrator.agents.nonfiction import (
    AnalystAgent,
    FactCheckerAgent,
    NonfictionEditorAgent,
    NonfictionWriterAgent,
    ResearcherAgent,
)
from opus_orchestrator.config import OpusConfig, get_config
from opus_orchestrator.schemas import (
    BookIntent,
    BookType,
    Manuscript,
    RawContent,
)
from opus_orchestrator.state import OpusState, create_initial_state

__all__ = [
    # Config
    "OpusConfig",
    "get_config",
    # State
    "OpusState",
    "create_initial_state",
    # Schemas
    "BookIntent",
    "BookType",
    "Manuscript",
    "RawContent",
    # Fiction Agents
    "ArchitectAgent",
    "CharacterLeadAgent",
    "EditorAgent",
    "VoiceAgent",
    "WorldsmithAgent",
    # Nonfiction Agents
    "ResearcherAgent",
    "AnalystAgent",
    "NonfictionWriterAgent",
    "FactCheckerAgent",
    "NonfictionEditorAgent",
    # Main
    "OpusOrchestrator",
]

# Import orchestrator at bottom to avoid circular imports
from opus_orchestrator.orchestrator import OpusOrchestrator
