"""Main Opus Orchestrator class."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Optional

from opus_orchestrator import get_config
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
from opus_orchestrator.config import OpusConfig
from opus_orchestrator.schemas import (
    BookBlueprint,
    BookIntent,
    BookType,
    Chapter,
    ChapterCritique,
    ChapterDraft,
    Manuscript,
    RawContent,
)
from opus_orchestrator.state import OpusState


class OpusOrchestrator:
    """Main orchestrator for AI book generation.

    Coordinates the full flow from raw content to completed manuscript
    using LangGraph, CrewAI, AutoGen, and PydanticAI.
    """

    def __init__(
        self,
        repo_url: str | None = None,
        book_type: str = "fiction",
        genre: Optional[str] = None,
        target_audience: str = "general readers",
        intended_outcome: str = "complete manuscript",
        tone: Optional[str] = None,
        target_word_count: int = 80000,
        config: Optional[OpusConfig] = None,
    ):
        """Initialize the Opus Orchestrator.

        Args:
            repo_url: GitHub URL containing raw content
            book_type: "fiction" or "nonfiction"
            genre: Genre for fiction or nonfiction subgenre
            target_audience: Description of target readers
            intended_outcome: What the final product should achieve
            tone: Desired tone of writing
            target_word_count: Target word count for the book
            config: Optional configuration override
        """
        self.config = config or get_config()

        # Convert string to BookType
        self.book_type = BookType(book_type.lower())
        self.repo_url = repo_url

        # Build intent
        self.intent = BookIntent(
            book_type=self.book_type,
            genre=genre,
            target_audience=target_audience,
            intended_outcome=intended_outcome,
            tone=tone,
            target_word_count=target_word_count,
        )

        # Initialize agents based on book type
        self._init_agents()

        # State
        self.state: Optional[OpusState] = None

    def _init_agents(self) -> None:
        """Initialize agents based on book type."""
        if self.book_type == BookType.FICTION:
            self.agents = {
                "architect": ArchitectAgent(self.config.agent),
                "worldsmith": WorldsmithAgent(self.config.agent),
                "character_lead": CharacterLeadAgent(self.config.agent),
                "voice": VoiceAgent(self.config.agent),
                "editor": EditorAgent(self.config.agent),
            }
        else:
            self.agents = {
                "researcher": ResearcherAgent(self.config.agent),
                "analyst": AnalystAgent(self.config.agent),
                "writer": NonfictionWriterAgent(self.config.agent),
                "fact_checker": FactCheckerAgent(self.config.agent),
                "editor": NonfictionEditorAgent(self.config.agent),
            }

    async def ingest(self, content: Optional[RawContent] = None) -> OpusState:
        """Ingest raw content from repository.

        Args:
            content: Optional pre-processed content

        Returns:
            Updated state with raw content
        """
        if self.repo_url and not content:
            # TODO: Implement GitHub ingestion
            content = RawContent(
                content_type="repository",
                text="[Content would be extracted from GitHub repository]",
                metadata={"repo_url": self.repo_url},
            )

        self.state = create_initial_state(
            repo_url=self.repo_url or "",
            intent=self.intent,
            raw_content=content,
        )

        return self.state

    async def analyze_intent(self) -> OpusState:
        """Analyze intent and generate blueprint."""
        # TODO: Implement LLM-based intent analysis
        self.state.current_stage = "blueprint"
        return self.state

    async def generate_blueprint(self) -> BookBlueprint:
        """Generate the book blueprint.

        Returns:
            Complete book blueprint
        """
        # TODO: Implement blueprint generation using agents
        blueprint = BookBlueprint(
            title=self.intent.working_title or "Untitled",
            genre=self.intent.genre or "general",
            target_audience=self.intent.target_audience,
            target_word_count=self.intent.target_word_count,
            structure="three-act",
            themes=[],
            tone=self.intent.tone or "neutral",
            chapters=[],
        )

        self.state.blueprint = blueprint
        self.state.current_stage = "drafting"
        self.state.progress = 0.1

        return blueprint

    async def write_chapter(self, chapter_num: int) -> ChapterDraft:
        """Write a single chapter.

        Args:
            chapter_num: Chapter number to write

        Returns:
            Chapter draft
        """
        # TODO: Implement chapter writing with agents
        draft = ChapterDraft(
            chapter_number=chapter_num,
            title=f"Chapter {chapter_num}",
            content=f"[Chapter {chapter_num} content would be generated here]",
            word_count=2000,
        )

        self.state.drafts[chapter_num] = draft
        self.state.progress = 0.1 + (chapter_num / (self.state.blueprint.target_word_count / 3000))

        return draft

    async def critique_chapter(self, chapter_num: int) -> ChapterCritique:
        """Critique a chapter.

        Args:
            chapter_num: Chapter number to critique

        Returns:
            Chapter critique
        """
        # TODO: Implement critic crew using AutoGen
        critique = ChapterCritique(
            chapter_number=chapter_num,
            overall_score=0.85,
            criteria_scores=[],
            consensus_strengths=["Strong voice", "Good pacing"],
            consensus_weaknesses=["Minor continuity issue"],
            revision_priority="minor_revisions",
        )

        if chapter_num not in self.state.critiques:
            self.state.critiques[chapter_num] = []
        self.state.critiques[chapter_num].append(critique)

        return critique

    async def iterate_chapter(self, chapter_num: int) -> Chapter:
        """Iterate on a chapter until approved.

        Args:
            chapter_num: Chapter number to iterate

        Returns:
            Final approved chapter
        """
        max_rounds = self.config.iteration.max_critic_rounds

        for round_num in range(1, max_rounds + 1):
            self.state.iteration_round = round_num

            # Get draft
            draft = self.state.drafts.get(chapter_num)
            if not draft:
                draft = await self.write_chapter(chapter_num)

            # Critique
            critique = await self.critique_chapter(chapter_num)

            # Check approval
            if critique.overall_score >= self.config.iteration.approval_threshold:
                break

            # TODO: Implement revision based on critique

        # Return final chapter
        return Chapter(
            chapter_number=chapter_num,
            title=draft.title,
            content=draft.content,
            word_count=draft.word_count,
        )

    async def compile_manuscript(self) -> Manuscript:
        """Compile all chapters into final manuscript.

        Returns:
            Complete manuscript
        """
        chapters = []

        if self.state.blueprint:
            for i in range(1, len(self.state.blueprint.chapters) + 1):
                chapter = await self.iterate_chapter(i)
                chapters.append(chapter)

        manuscript = Manuscript(
            title=self.state.blueprint.title if self.state.blueprint else "Untitled",
            book_type=self.book_type,
            genre=self.intent.genre or "general",
            chapters=chapters,
            total_word_count=sum(c.word_count for c in chapters),
        )

        self.state.manuscript = manuscript
        self.state.current_stage = "complete"
        self.state.progress = 1.0

        return manuscript

    async def run(self) -> Manuscript:
        """Run the full orchestrator pipeline.

        Returns:
            Complete manuscript
        """
        # Ingest
        await self.ingest()

        # Analyze intent
        await self.analyze_intent()

        # Generate blueprint
        await self.generate_blueprint()

        # Write and iterate chapters
        await self.compile_manuscript()

        return self.state.manuscript

    def save_manuscript(self, output_path: Optional[Path] = None) -> Path:
        """Save manuscript to file.

        Args:
            output_path: Optional output path

        Returns:
            Path to saved file
        """
        if not self.state.manuscript:
            raise ValueError("No manuscript to save. Run first.")

        output_path = output_path or self.config.output.output_dir / f"{self.state.manuscript.title.lower().replace(' ', '_')}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(self.state.manuscript.to_markdown())

        return output_path
