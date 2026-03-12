"""LangGraph state definitions for Opus Orchestrator."""

from typing import Any, Optional

from pydantic import BaseModel, Field

from opus_orchestrator.schemas import (
    BookBlueprint,
    BookIntent,
    Chapter,
    ChapterCritique,
    ChapterDraft,
    Manuscript,
    RawContent,
    Revision,
)


class OpusState(BaseModel):
    """Main state for the Opus Orchestrator graph.

    This state flows through the entire book generation pipeline,
    accumulating data at each stage.
    """

    # --- Input Phase ---
    repo_url: Optional[str] = None
    raw_content: Optional[RawContent] = None
    intent: Optional[BookIntent] = None

    # --- Blueprint Phase ---
    blueprint: Optional[BookBlueprint] = None

    # --- Drafting Phase ---
    current_chapter: int = 0
    drafts: dict[int, ChapterDraft] = Field(default_factory=dict)

    # --- Iteration Phase ---
    iteration_round: int = 0
    critiques: dict[int, list[ChapterCritique]] = Field(default_factory=dict)
    revisions: dict[int, list[Revision]] = Field(default_factory=dict)

    # --- Final Phase ---
    manuscript: Optional[Manuscript] = None

    # --- Metadata ---
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    progress: float = 0.0  # 0.0 to 1.0
    current_stage: str = "ingestion"  # ingestion, blueprint, drafting, iteration, compilation, complete

    # --- Configuration ---
    config: dict[str, Any] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


# Define the graph nodes as functions
# These will be implemented in graph.py


def create_initial_state(
    repo_url: str,
    intent: BookIntent,
    raw_content: Optional[RawContent] = None,
    **config,
) -> OpusState:
    """Create initial state for the orchestrator."""
    return OpusState(
        repo_url=repo_url,
        intent=intent,
        raw_content=raw_content,
        current_stage="ingestion",
        config=config,
    )
