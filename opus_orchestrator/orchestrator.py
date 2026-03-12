"""Main Opus Orchestrator class."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv

# Load local environment
load_dotenv("/home/solaria/.openclaw/workspace/opus-orchestrator-ai/.env")

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
    """Main orchestrator for AI book generation."""

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
        """Initialize the Opus Orchestrator."""
        self.config = config or get_config()

        # Set API key from environment if not in config
        if not self.config.agent.api_key:
            self.config.agent.api_key = os.environ.get("MINIMAX_API_KEY") or os.environ.get("OPENAI_API_KEY")

        self.book_type = BookType(book_type.lower())
        self.repo_url = repo_url

        self.intent = BookIntent(
            book_type=self.book_type,
            genre=genre,
            target_audience=target_audience,
            intended_outcome=intended_outcome,
            tone=tone,
            target_word_count=target_word_count,
        )

        self._init_agents()
        self.state: Optional[OpusState] = None
        self.style_guide: str = ""

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
        """Ingest raw content from repository."""
        if self.repo_url and not content:
            content = RawContent(
                content_type="repository",
                text="[Content would be extracted from GitHub repository]",
                metadata={"repo_url": self.repo_url},
            )

        self.state = OpusState(
            repo_url=self.repo_url or "",
            intent=self.intent,
            raw_content=content,
            current_stage="ingestion",
        )

        return self.state

    async def generate_blueprint(self) -> BookBlueprint:
        """Generate the book blueprint using the Architect agent."""
        print(f"🧠 Generating blueprint with {self.config.agent.provider}/{self.config.agent.model}...")

        # Call Architect
        architect = self.agents["architect"]
        response = await architect.execute(
            {
                "raw_content": self.state.raw_content.text if self.state.raw_content else "",
                "intent": self.intent.model_dump(),
            },
            {},
        )

        if not response.success:
            raise Exception(f"Blueprint generation failed: {response.error}")

        # Parse response into blueprint
        # For now, create a basic blueprint from the response
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

        # Try to extract chapters from response if it's detailed
        response_text = response.output if isinstance(response.output, str) else str(response.output)
        
        # Basic chapter structure (in real impl, would parse LLM output)
        words_per_chapter = 3000
        num_chapters = max(3, self.intent.target_word_count // words_per_chapter)
        
        for i in range(1, num_chapters + 1):
            blueprint.chapters.append(
                BookBlueprint.model_construct(
                    chapter_number=i,
                    title=f"Chapter {i}",
                    summary=f"Chapter {i} of the story",
                    word_count_target=words_per_chapter,
                )
            )

        self.state.blueprint = blueprint
        self.state.current_stage = "blueprint"
        self.state.progress = 0.2

        print(f"✅ Blueprint generated: {num_chapters} chapters planned")
        
        return blueprint

    async def create_style_guide(self) -> str:
        """Create style guide using Voice agent."""
        print("🎨 Creating style guide...")

        voice = self.agents["voice"]
        response = await voice.execute(
            {
                "genre": self.intent.genre or "general",
                "tone": self.intent.tone or "neutral",
                "target_audience": self.intent.target_audience,
            },
            {},
        )

        if response.success:
            self.style_guide = response.output if isinstance(response.output, str) else str(response.output)
        else:
            self.style_guide = "Professional fiction prose style."

        print("✅ Style guide created")
        return self.style_guide

    async def write_chapter(self, chapter_num: int) -> ChapterDraft:
        """Write a single chapter using Voice agent."""
        blueprint = self.state.blueprint
        if not blueprint or chapter_num > len(blueprint.chapters):
            raise ValueError(f"No blueprint or chapter {chapter_num} not found")

        chapter_spec = blueprint.chapters[chapter_num - 1]
        
        print(f"✍️  Writing chapter {chapter_num}/{len(blueprint.chapters)}...")

        voice = self.agents["voice"]
        response = await voice.write_chapter(
            chapter_spec.model_dump(),
            self.style_guide,
            {},
        )

        if not response.success:
            raise Exception(f"Chapter writing failed: {response.error}")

        output = response.output if isinstance(response.output, dict) else {"content": str(response.output)}
        
        draft = ChapterDraft(
            chapter_number=chapter_num,
            title=chapter_spec.title,
            content=output.get("content", ""),
            word_count=output.get("word_count", len(output.get("content", "").split())),
        )

        self.state.drafts[chapter_num] = draft
        
        progress = 0.2 + (0.6 * chapter_num / len(blueprint.chapters))
        self.state.progress = progress

        print(f"✅ Chapter {chapter_num} written: {draft.word_count} words")

        return draft

    async def critique_chapter(self, chapter_num: int) -> ChapterCritique:
        """Critique a chapter using Editor agent."""
        draft = self.state.drafts.get(chapter_num)
        if not draft:
            raise ValueError(f"No draft for chapter {chapter_num}")

        print(f"🔍 Critiquing chapter {chapter_num}...")

        editor = self.agents["editor"]
        response = await editor.review_chapter(
            draft.model_dump(),
            {
                "title": self.state.blueprint.title if self.state.blueprint else "Untitled",
                "genre": self.intent.genre or "general",
                "total_chapters": len(self.state.blueprint.chapters) if self.state.blueprint else 0,
            },
            {},
        )

        if not response.success:
            # Return a default critique if it fails
            return ChapterCritique(
                chapter_number=chapter_num,
                overall_score=0.7,
                criteria_scores=[],
                consensus_strengths=["Good effort"],
                consensus_weaknesses=[],
                revision_priority="minor_revisions",
            )

        output = response.output if isinstance(response.output, dict) else {"critique": str(response.output)}
        
        critique = ChapterCritique(
            chapter_number=chapter_num,
            overall_score=output.get("score", 0.7),
            criteria_scores=[],
            consensus_strengths=[],
            consensus_weaknesses=[],
            revision_priority="minor_revisions",
        )

        if chapter_num not in self.state.critiques:
            self.state.critiques[chapter_num] = []
        self.state.critiques[chapter_num].append(critique)

        print(f"✅ Chapter {chapter_num} critiqued: score {critique.overall_score:.2f}")

        return critique

    async def iterate_chapter(self, chapter_num: int, max_iterations: int = 2) -> Chapter:
        """Iterate on a chapter until approved or max iterations reached."""
        draft = self.state.drafts.get(chapter_num)
        
        for iteration in range(1, max_iterations + 1):
            print(f"🔄 Iteration {iteration}/{max_iterations} for chapter {chapter_num}")
            
            # Critique
            critique = await self.critique_chapter(chapter_num)
            
            # Check if approved
            if critique.overall_score >= self.config.iteration.approval_threshold:
                print(f"✅ Chapter {chapter_num} approved!")
                break
            
            # If not approved and have more iterations, could revise here
            # For now, we'll proceed with what we have
        
        # Get final draft
        draft = self.state.drafts.get(chapter_num)
        
        return Chapter(
            chapter_number=chapter_num,
            title=draft.title,
            content=draft.content,
            word_count=draft.word_count,
        )

    async def compile_manuscript(self) -> Manuscript:
        """Compile all chapters into final manuscript."""
        if not self.state.blueprint:
            raise ValueError("No blueprint. Run generate_blueprint first.")

        num_chapters = len(self.state.blueprint.chapters)
        print(f"\n📚 Compiling manuscript: {num_chapters} chapters\n")

        chapters = []
        
        for i in range(1, num_chapters + 1):
            # Write chapter
            await self.write_chapter(i)
            
            # Iterate/critique
            chapter = await self.iterate_chapter(i)
            chapters.append(chapter)

        manuscript = Manuscript(
            title=self.state.blueprint.title,
            book_type=self.book_type,
            genre=self.intent.genre or "general",
            chapters=chapters,
            total_word_count=sum(c.word_count for c in chapters),
        )

        self.state.manuscript = manuscript
        self.state.current_stage = "complete"
        self.state.progress = 1.0

        print(f"\n✅ Manuscript complete: {manuscript.total_word_count} words")

        return manuscript

    async def run(self) -> Manuscript:
        """Run the full orchestrator pipeline."""
        print(f"\n{'='*50}")
        print("🎯 OPUS ORCHESTRATOR - Starting")
        print(f"{'='*50}\n")

        # Ingest
        await self.ingest()

        # Generate blueprint
        await self.generate_blueprint()

        # Create style guide
        await self.create_style_guide()

        # Write and iterate chapters
        manuscript = await self.compile_manuscript()

        print(f"\n{'='*50}")
        print("🎉 OPUS ORCHESTRATOR - Complete!")
        print(f"{'='*50}\n")

        return manuscript

    def save_manuscript(self, output_path: Optional[Path] = None) -> Path:
        """Save manuscript to file."""
        if not self.state.manuscript:
            raise ValueError("No manuscript to save. Run first.")

        output_path = output_path or Path("./output") / f"{self.state.manuscript.title.lower().replace(' ', '_')}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(self.state.manuscript.to_markdown())

        return output_path
