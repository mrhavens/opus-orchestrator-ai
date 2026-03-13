"""Opus Orchestrator AI.

Full-flow AI book generation using LangGraph, CrewAI, AutoGen, and PydanticAI.
Integrates Fiction Fortress and Nonfiction Fortress methodologies.

Usage:
    python -m opus_orchestrator generate --concept "Your story idea"
    opus generate --concept "Your story idea"  # If installed
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
from opus_orchestrator.utils.s3_ingest import S3Ingestor, create_s3_ingestor
from opus_orchestrator.frameworks import StoryFramework
from opus_orchestrator.crews import (
    OpusCrew,
    FictionCrew,
    NonfictionCrew,
    create_fiction_crew,
    create_nonfiction_crew,
)
from opus_orchestrator.pydanticai_agent import (
    OpusPydanticAgent,
    StorySeed,
    CharacterProfile,
    ChapterOutline,
    ChapterDraft,
    CritiqueResult,
    StyleGuide,
    create_story_seed_agent,
    create_character_agent,
    create_chapter_outline_agent,
    create_chapter_draft_agent,
    create_critique_agent,
    create_style_guide_agent,
)

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
    # Crews
    "OpusCrew",
    "FictionCrew",
    "NonfictionCrew",
    "create_fiction_crew",
    "create_nonfiction_crew",
    # PydanticAI (NEW!)
    "OpusPydanticAgent",
    "StorySeed",
    "CharacterProfile",
    "ChapterOutline",
    "ChapterDraft",
    "CritiqueResult",
    "StyleGuide",
    "create_story_seed_agent",
    "create_character_agent",
    "create_chapter_outline_agent",
    "create_chapter_draft_agent",
    "create_critique_agent",
    "create_style_guide_agent",
    # Main
    "OpusOrchestrator",
    "CritiqueCrew",
    "create_critique_crew",
    "GitHubIngestor",
    "create_github_ingestor",
    # S3/MinIO (NEW!)
    "S3Ingestor",
    "create_s3_ingestor",
]

# Import legacy orchestrator for backward compatibility
from opus_orchestrator.orchestrator import OpusOrchestrator
