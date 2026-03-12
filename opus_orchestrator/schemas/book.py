"""Pydantic schemas for Opus Orchestrator."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class BookType(str, Enum):
    """Type of book being generated."""

    FICTION = "fiction"
    NONFICTION = "nonfiction"


class Genre(str, Enum):
    """Fiction genres."""

    MYSTERY = "mystery"
    ROMANCE = "romance"
    THRILLER = "thriller"
    FANTASY = "fantasy"
    SCIENCE_FICTION = "science-fiction"
    HORROR = "horror"
    LITERARY = "literary"
    OTHER = "other"


class NonfictionGenre(str, Enum):
    """Nonfiction genres."""

    BUSINESS = "business"
    SELF_HELP = "self-help"
    HISTORY = "history"
    BIOGRAPHY = "biography"
    SCIENCE = "science"
    PHILOSOPHY = "philosophy"
    MEMOIR = "memoir"
    ACADEMIC = "academic"
    OTHER = "other"


# --- Input Schemas ---


class BookIntent(BaseModel):
    """User's intent for the book project."""

    book_type: BookType
    genre: Optional[str] = None
    working_title: Optional[str] = None
    target_audience: str = Field(description="Who is this book for?")
    intended_outcome: str = Field(description="What should the final product achieve?")
    tone: Optional[str] = None
    target_word_count: int = Field(default=80000, ge=1000, le=500000)
    special_instructions: Optional[str] = None


class RawContent(BaseModel):
    """Raw content extracted from source."""

    content_type: str = Field(description="Type: outline, notes, stream-of-consciousness, etc.")
    text: str = Field(description="The raw content itself")
    metadata: dict[str, Any] = Field(default_factory=dict)


# --- Blueprint Schemas ---


class ChapterBlueprint(BaseModel):
    """Blueprint for a single chapter."""

    chapter_number: int
    title: str
    summary: str = Field(description="Brief summary of chapter content")
    word_count_target: int
    pov_character: Optional[str] = None
    key_events: list[str] = Field(default_factory=list)
    themes: list[str] = Field(default_factory=list)
    scenes: list[dict[str, Any]] = Field(default_factory=list)


class BookBlueprint(BaseModel):
    """Complete blueprint for the book."""

    title: str
    subtitle: Optional[str] = None
    genre: str
    target_audience: str
    target_word_count: int
    structure: str = Field(description="Overall structural approach")
    themes: list[str] = Field(default_factory=list)
    tone: str
    chapters: list[ChapterBlueprint] = Field(default_factory=list)
    characters: list[dict[str, Any]] = Field(default_factory=list, description="For fiction")
    world_elements: dict[str, Any] = Field(default_factory=dict, description="For fiction")
    key_arguments: list[str] = Field(default_factory=list, description="For nonfiction")


# --- Agent Output Schemas ---


class ChapterDraft(BaseModel):
    """A chapter draft from the writer agent."""

    chapter_number: int
    title: str
    content: str
    word_count: int
    notes: Optional[str] = None


class CritiqueScore(BaseModel):
    """Score from a critic agent."""

    criterion: str
    score: float = Field(ge=0.0, le=1.0)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)


class ChapterCritique(BaseModel):
    """Complete critique of a chapter."""

    chapter_number: int
    overall_score: float = Field(ge=0.0, le=1.0)
    criteria_scores: list[CritiqueScore]
    consensus_strengths: list[str] = Field(default_factory=list)
    consensus_weaknesses: list[str] = Field(default_factory=list)
    revision_priority: str = Field(description="major_revisions, minor_revisions, approved")
    notes: Optional[str] = None


class Revision(BaseModel):
    """Revision instructions for a chapter."""

    chapter_number: int
    priority: str = Field(description="major or minor")
    changes_required: list[str] = Field(default_factory=list)
    preserve_elements: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


# --- Final Output Schemas ---


class Chapter(BaseModel):
    """Final chapter in the manuscript."""

    chapter_number: int
    title: str
    content: str
    word_count: int


class Manuscript(BaseModel):
    """Complete manuscript."""

    title: str
    subtitle: Optional[str] = None
    author: str = "Opus Orchestrator AI"
    book_type: BookType
    genre: str
    chapters: list[Chapter]
    total_word_count: int
    frontmatter: dict[str, Any] = Field(default_factory=dict)
    backmatter: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    def to_markdown(self) -> str:
        """Convert to markdown format."""
        lines = []

        # Frontmatter
        if self.frontmatter.get("dedication"):
            lines.append(f"*{self.frontmatter['dedication']}*\n")
        if self.frontmatter.get("epigraph"):
            lines.append(f"> {self.frontmatter['epigraph']}\n")

        # Title
        lines.append(f"# {self.title}")
        if self.subtitle:
            lines.append(f"## {self.subtitle}")
        lines.append(f"\n*by {self.author}*\n")

        # TOC
        if self.frontmatter.get("include_toc", True):
            lines.append("## Table of Contents\n")
            for ch in self.chapters:
                lines.append(f"{ch.chapter_number}. [{ch.title}](#chapter-{ch.chapter_number})")
            lines.append("")

        # Chapters
        for ch in self.chapters:
            lines.append(f"## Chapter {ch.chapter_number}: {ch.title}\n")
            lines.append(ch.content)
            lines.append("")

        return "\n".join(lines)


# --- State Schemas ---


class IterationState(BaseModel):
    """State for iteration tracking."""

    round: int = 0
    chapter_number: int
    critiques: list[ChapterCritique] = Field(default_factory=list)
    current_score: float = 0.0
    approved: bool = False
    revisions_requested: list[Revision] = Field(default_factory=list)
