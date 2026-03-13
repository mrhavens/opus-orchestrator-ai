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
from opus_orchestrator.langgraph_workflow import OpusGraph, run_opus, OpusGraphState
from opus_orchestrator.autogen_critique import CritiqueCrew, create_critique_crew
from opus_orchestrator.utils.github_ingest import GitHubIngestor, create_github_ingestor
from opus_orchestrator.frameworks import StoryFramework

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
    # LangGraph
    "OpusGraph",
    "OpusGraphState",
    "run_opus",
    "StoryFramework",
    # Main (legacy)
    "OpusOrchestrator",
]

# Import legacy orchestrator for backward compatibility
from opus_orchestrator.orchestrator import OpusOrchestrator
