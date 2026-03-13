"""Main Opus Orchestrator - Snowflake Method Implementation with Multiple Frameworks.

Full pipeline supporting multiple story frameworks and GitHub ingestion.
"""

import asyncio
import os
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv

load_dotenv()

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
from opus_orchestrator.frameworks import (
    StoryFramework,
    FRAMEWORKS,
    get_framework_for_genre,
    get_framework_prompt,
)
from opus_orchestrator.schemas import (
    BookBlueprint,
    BookIntent,
    BookType,
    Chapter,
    ChapterBlueprint,
    ChapterCritique,
    ChapterDraft,
    Manuscript,
    RawContent,
)
from opus_orchestrator.state import OpusState
from opus_orchestrator.utils.github_ingest import GitHubIngestor

# Nonfiction taxonomy - Purpose × Structure matrix
from opus_orchestrator.nonfiction import (
    PurposeClassifier,
    ReaderPurpose,
)
from opus_orchestrator.nonfiction_taxonomy import (
    select_framework,
    get_frameworks_for_purpose,
    NONFICTION_FRAMEWORKS,
    PURPOSE_STRUCTURE_MATRIX,
    StructuralPattern,
    NonfictionCategory,
)


class OpusOrchestrator:
    """Main orchestrator implementing multiple story frameworks."""

    def __init__(
        self,
        repo_url: str | None = None,
        book_type: str = "fiction",
        genre: Optional[str] = None,
        target_audience: str = "general readers",
        intended_outcome: str = "complete novel",
        tone: Optional[str] = None,
        target_word_count: int = 80000,
        framework: str = "snowflake",
        config: Optional[OpusConfig] = None,
        # Nonfiction-specific options
        purpose: Optional[str] = None,
        category: Optional[str] = None,
    ):
        """Initialize the Opus Orchestrator with selectable framework.
        
        Args:
            repo_url: GitHub URL for content
            book_type: "fiction" or "nonfiction"
            genre: Genre (for framework suggestions)
            target_audience: Who is this for
            intended_outcome: What to produce
            tone: Desired tone
            target_word_count: Target length
            framework: Story framework to use (snowflake, three-act, save-the-cat, 
                      hero-journey, story-circle, seven-point, fichtean)
            config: Optional config override
        """
        self.config = config or get_config()

        if not self.config.agent.api_key:
            self.config.agent.api_key = os.environ.get("MINIMAX_API_KEY") or os.environ.get("OPENAI_API_KEY")

        self.book_type = BookType(book_type.lower())
        self.repo_url = repo_url
        
        # Handle framework
        if isinstance(framework, str):
            try:
                self.framework = StoryFramework(framework.lower())
            except ValueError:
                # Default to snowflake if invalid
                self.framework = StoryFramework.SNOWFLAKE
        else:
            self.framework = framework
        
        # Get framework info
        self.framework_info = FRAMEWORKS.get(self.framework, FRAMEWORKS[StoryFramework.SNOWFLAKE])

        # ================================================================
        # NONFICTION: Purpose Classification & Framework Selection
        # ================================================================
        self.purpose: Optional[ReaderPurpose] = None
        self.nonfiction_framework: Optional[dict] = None
        self.framework_stages: list[str] = []
        
        if self.book_type == BookType.NONFICTION:
            # Classify purpose if not explicitly provided
            if purpose:
                try:
                    self.purpose = ReaderPurpose(purpose.lower())
                except ValueError:
                    # Default will be determined by classifier
                    self.purpose = None
            
            # If purpose not yet determined, classify from intent
            if not self.purpose:
                self._classify_purpose_from_intent(
                    concept=intended_outcome,  # Using outcome as proxy for concept
                    target_audience=target_audience,
                )
            
            # Select appropriate framework based on purpose
            self._select_nonfiction_framework(category)
        
        # ================================================================

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
        
        # Snowflake method outputs
        self.one_sentence: str = ""
        self.one_paragraph: str = ""
        self.character_sheets: str = ""
        self.four_page_outline: str = ""
        self.character_charts: str = ""
        self.scene_list: str = ""
        self.scene_descriptions: str = ""
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

    # =========================================================================
    # NONFICTION: Purpose Classification & Framework Selection
    # =========================================================================
    
    def _classify_purpose_from_intent(
        self,
        concept: str,
        target_audience: str,
    ) -> None:
        """Classify purpose from book intent using keyword classifier.
        
        Args:
            concept: The book concept/title
            target_audience: Target audience description
        """
        classifier = PurposeClassifier()
        result = classifier._keyword_classify(
            concept=concept or "",
            target_audience=target_audience,
            intended_outcome=self.intent.intended_outcome or "",
        )
        
        self.purpose = result.purpose
        print(f"[NONFICTION] Purpose classified: {self.purpose.value} (confidence: {result.confidence:.2f})")
        print(f"[NONFICTION] Reasoning: {result.reasoning}")
    
    def _select_nonfiction_framework(self, category: Optional[str] = None) -> None:
        """Select the best framework based on purpose and category.
        
        Args:
            category: Optional nonfiction category (business, self_help, etc.)
        """
        if not self.purpose:
            # Default to UNDERSTAND if not classified
            self.purpose = ReaderPurpose.UNDERSTAND
        
        # Map category string to NonfictionCategory enum
        category_enum = None
        if category:
            try:
                category_enum = NonfictionCategory(category.lower())
            except ValueError:
                pass
        
        # Select framework using taxonomy
        framework = select_framework(
            purpose=self.purpose,
            category=category_enum,
            user_preferred_framework=None,
        )
        
        self.nonfiction_framework = framework
        self.framework_stages = framework.get("stages", [])
        
        print(f"[NONFICTION] Framework selected: {framework.get('name', 'Unknown')}")
        print(f"[NONFICTION] Structure: {framework.get('structure', 'N/A')}")
        print(f"[NONFICTION] Stages ({len(self.framework_stages)}):")
        for i, stage in enumerate(self.framework_stages[:5], 1):
            print(f"  {i}. {stage}")
        if len(self.framework_stages) > 5:
            print(f"  ... and {len(self.framework_stages) - 5} more")
    
    def get_framework_context(self) -> dict[str, Any]:
        """Get the framework context for passing to agents.
        
        Returns:
            Dict with framework name, purpose, stages, and prompt template
        """
        if self.book_type == BookType.NONFICTION and self.nonfiction_framework:
            return {
                "framework_name": self.nonfiction_framework.get("name", ""),
                "framework_purpose": self.purpose.value if self.purpose else "",
                "structure": self.nonfiction_framework.get("structure", ""),
                "stages": self.framework_stages,
                "prompt_template": self.nonfiction_framework.get("prompt_template", ""),
                "tone_guidance": self.nonfiction_framework.get("tone_guidance", ""),
            }
        else:
            # Return fiction framework context
            return {
                "framework_name": self.framework.value,
                "framework_purpose": "entertainment",
                "structure": "narrative",
                "stages": [],
                "prompt_template": "",
                "tone_guidance": "",
            }
    
    def generate_stage_outline(
        self,
        stage_name: str,
        stage_index: int,
        context: dict[str, Any],
    ) -> str:
        """Generate a chapter/section outline for a given stage.
        
        Args:
            stage_name: Name of the framework stage
            stage_index: Index of the stage
            context: Additional context (book concept, etc.)
            
        Returns:
            Generated outline for the stage
        """
        if not self.nonfiction_framework:
            return f"Chapter {stage_index + 1}: {stage_name}"
        
        # Build prompt for this specific stage
        prompt = f"""Generate a detailed outline for a book section.

Framework Stage: {stage_name}
Stage Number: {stage_index + 1} of {len(self.framework_stages)}

Book Context:
- Concept: {context.get('concept', 'N/A')}
- Purpose: {self.purpose.value if self.purpose else 'N/A'}
- Target Audience: {self.intent.target_audience}

Framework: {self.nonfiction_framework.get('name', 'N/A')}
Structure: {self.nonfiction_framework.get('structure', 'N/A')}

Generate a detailed outline with:
1. Section title
2. Key points to cover (3-5)
3. Word count target
4. Tone guidance for this section
"""
        return prompt
    
    # =========================================================================

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

    # =========================================================================
    # GITHUB INGESTION
    # =========================================================================

    def ingest_from_github(self, repo: str, include_readme: bool = True) -> RawContent:
        """Ingest content from a GitHub repository.
        
        Args:
            repo: "owner/repo" format (e.g., "mrhavens/my-notes")
            include_readme: Whether to include README files
            
        Returns:
            RawContent with the combined text from the repo
        """
        from opus_orchestrator.utils.github_ingest import GitHubIngestor
        
        print(f"📥 Loading from GitHub: {repo}")
        
        github_token = self.config.github_token or os.environ.get("GITHUB_TOKEN")
        ingestor = GitHubIngestor(token=github_token)
        
        result = ingestor.ingest_repo(repo, include_readme=include_readme)
        
        print(f"   Found {result['file_count']} files")
        print(f"   Total content: {result['total_chars']:,} characters")
        
        return RawContent(
            content_type="github",
            text=result["combined_text"],
            metadata={
                "repo": repo,
                "files": list(result["files"].keys()),
                "file_count": result["file_count"],
            },
        )

    # =========================================================================
    # SNOWFLAKE METHOD STAGES
    # =========================================================================

    async def snowflake_stage_1(self) -> str:
        """Stage 1: One sentence summary.
        
        Take your one-paragraph story summary and cut it down to one sentence.
        """
        print("❄️ SNOWFLAKE STAGE 1: One sentence summary...")
        
        raw_content = self.state.raw_content.text if self.state.raw_content else ""
        
        user_prompt = f"""Create a ONE SENTENCE summary of this story concept.

The sentence should contain:
- Protagonist's name (or descriptor)
- Their goal
- The conflict/obstacle
- The stakes

Example: "In a world where magic is forbidden, a young mage must master forbidden arts to save her dying brother, even if it means sparking a war with the ruling theocracy."

## Your seed content:
{raw_content}

## Task:
Write ONE compelling sentence that captures the entire story.
"""
        response = await self.agents["architect"].call_llm(
            system_prompt="You are an expert story architect. Create concise, compelling summaries.",
            user_prompt=user_prompt,
        )
        
        self.one_sentence = response.strip()
        print(f"   → {self.one_sentence}")
        
        return self.one_sentence

    async def snowflake_stage_2(self) -> str:
        """Stage 2: One paragraph outline (framework-dependent).
        
        Expand the one sentence to a paragraph with setup, 3 acts, and resolution.
        Uses the selected story framework.
        """
        print(f"❄️ SNOWFLAKE STAGE 2: One paragraph outline ({self.framework_info['name']})...")
        
        # Get framework-specific prompt
        framework_system_prompt = get_framework_prompt(self.framework)
        
        user_prompt = f"""Expand this one-sentence summary into a full one-paragraph story outline.

Use the {self.framework_info['name']} framework: {self.framework_info.get('description', '')}

## One sentence:
{self.one_sentence}

## Task:
Write one detailed paragraph (4-8 sentences) that tells the complete story arc.
"""
        response = await self.agents["architect"].call_llm(
            system_prompt=framework_system_prompt,
            user_prompt=user_prompt,
        )
        
        self.one_paragraph = response.strip()
        print(f"   → {self.one_paragraph[:200]}...")
        
        return self.one_paragraph

    async def snowflake_stage_3(self) -> str:
        """Stage 3: Character sheets (one page per major character).
        
        Create character sheets for all major characters.
        """
        print("❄️ SNOWFLAKE STAGE 3: Character sheets...")
        
        user_prompt = f"""Create character sheets for all major characters in this story.

For each character, provide:
- Name
- Role (protagonist, antagonist, love interest, mentor, etc.)
- Age and physical description
- Background/history (2-3 sentences)
- Want (external goal)
- Need (internal growth)
- Fear
- Secret
- Character arc (how do they change?)

## Story outline:
{self.one_paragraph}

## Task:
Write comprehensive character sheets for all major characters.
"""
        response = await self.agents["character_lead"].execute(
            {"characters": [], "raw_content": self.one_paragraph},
            {},
        )
        
        self.character_sheets = response.output if isinstance(response.output, str) else str(response.output)
        print(f"   → Created character sheets ({len(self.character_sheets)} chars)")
        
        return self.character_sheets

    async def snowflake_stage_4(self) -> str:
        """Stage 4: Four-page outline.
        
        Expand each sentence of the one-paragraph outline into a full page.
        """
        print("❄️ SNOWFLAKE STAGE 4: Four-page outline...")
        
        user_prompt = f"""Expand this one-paragraph outline into a detailed four-page outline.

For each major section (setup, 3 acts, resolution), provide:
- Multiple scenes
- Character motivations
- Plot developments
- World details
- Dialogue hooks

This should be approximately 4 pages worth of outline material.

## Current outline:
{self.one_paragraph}

## Characters:
{self.character_sheets[:1000]}...

## Task:
Write a comprehensive four-page outline covering the entire story.
"""
        response = await self.agents["architect"].call_llm(
            system_prompt="You are an expert story architect. Create detailed, scene-by-scene outlines.",
            user_prompt=user_prompt,
        )
        
        self.four_page_outline = response.strip()
        print(f"   → Created four-page outline ({len(self.four_page_outline)} chars)")
        
        return self.four_page_outline

    async def snowflake_stage_5(self) -> str:
        """Stage 5: Detailed character charts.
        
        Expand character sheets into full character charts with dialogue samples.
        """
        print("❄️ SNOWFLAKE STAGE 5: Detailed character charts...")
        
        user_prompt = f"""Create detailed character charts for all major characters.

For each character include:
- Full backstory
- Psychological profile
- Speech patterns (with sample dialogue)
- Character quirks
- Relationships with other characters
- How they appear to others vs. who they really are
- Key scenes they're in

## Characters (basic):
{self.character_sheets}

## Story outline:
{self.one_paragraph}

## Task:
Write comprehensive, detailed character charts.
"""
        response = await self.agents["character_lead"].execute(
            {"characters": [], "raw_content": self.four_page_outline},
            {},
        )
        
        self.character_charts = response.output if isinstance(response.output, str) else str(response.output)
        print(f"   → Created detailed character charts")
        
        return self.character_charts

    async def snowflake_stage_6(self) -> str:
        """Stage 6: Scene list (framework-dependent).
        
        Create a list of all scenes using the selected framework.
        """
        print(f"❄️ SNOWFLAKE STAGE 6: Scene list ({self.framework_info['name']})...")
        
        # Get framework-specific prompt
        framework_system_prompt = get_framework_prompt(self.framework)
        
        words_per_scene = 1500  # Average scene length
        num_scenes = max(10, self.intent.target_word_count // words_per_scene)
        
        # Get framework beats if available
        framework_beats = ""
        if "beats" in self.framework_info:
            framework_beats = f"\n\n## Framework Beats:\n"
            for beat_name, beat_desc in self.framework_info["beats"]:
                framework_beats += f"- {beat_name}: {beat_desc}\n"
        
        user_prompt = f"""Create a complete SCENE LIST for this story using the {self.framework_info['name']}.

Target: approximately {num_scenes} scenes for a {self.intent.target_word_count:,} word novel.

{framework_beats}

## Four-page outline:
{self.four_page_outline}

## Characters:
{self.character_charts[:1000]}...

## Task:
Create a comprehensive scene list with all scenes needed.
"""
        response = await self.agents["architect"].call_llm(
            system_prompt=framework_system_prompt,
            user_prompt=user_prompt,
        )
        
        self.scene_list = response.strip()
        
        # Parse scene count
        scene_count = self.scene_list.count("Scene ") + self.scene_list.count("Chapter")
        print(f"   → Scene list created ({scene_count}+ scenes)")
        
        return self.scene_list

    async def snowflake_stage_7(self) -> str:
        """Stage 7: Scene descriptions.
        
        Expand each scene into a full description (like index card back).
        """
        print("❄️ SNOWFLAKE STAGE 7: Scene descriptions...")
        
        user_prompt = f"""Expand the scene list into detailed scene descriptions.

For each scene, provide:
- Opening beat
- Key dialogue points
- Conflict moment
- Turning point
- Closing beat

This is like writing the back of each index card - you know what happens but not the full prose.

## Scene list:
{self.scene_list}

## Characters:
{self.character_charts[:500]}...

## Task:
Write detailed descriptions for key scenes (at least 20 most important scenes).
"""
        response = await self.agents["architect"].call_llm(
            system_prompt="You are an expert story architect. Create vivid scene descriptions.",
            user_prompt=user_prompt,
        )
        
        self.scene_descriptions = response.strip()
        print(f"   → Scene descriptions created")
        
        return self.scene_descriptions

    async def create_style_guide(self) -> str:
        """Create the style guide for prose."""
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

        print("   ✅ Style guide created")
        return self.style_guide

    async def write_chapter(self, chapter_num: int, total_chapters: int) -> ChapterDraft:
        """Write a single chapter."""
        print(f"✍️  Writing chapter {chapter_num}/{total_chapters}...")
        
        # Build chapter spec from our pre-writing
        chapter_context = f"""
## Story context (from Snowflake pre-writing):

ONE SENTENCE: {self.one_sentence}
ONE PARAGRAPH: {self.one_paragraph}
SCENE LIST: {self.scene_list[:1000]}...
STYLE GUIDE: {self.style_guide[:500]}...

## Task:
Write Chapter {chapter_num} following the scene list and style guide.
Make it vivid, engaging, and true to the characters.
"""
        
        voice = self.agents["voice"]
        target_words = self.intent.target_word_count // total_chapters
        
        response = await voice.write_chapter(
            {
                "chapter_number": chapter_num,
                "title": f"Chapter {chapter_num}",
                "summary": f"Chapter {chapter_num} based on scene list",
                "word_count_target": target_words,
                "key_events": [],
            },
            chapter_context,
            {},
        )

        if not response.success:
            raise Exception(f"Chapter writing failed: {response.error}")

        output = response.output if isinstance(response.output, dict) else {"content": str(response.output)}
        
        draft = ChapterDraft(
            chapter_number=chapter_num,
            title=f"Chapter {chapter_num}",
            content=output.get("content", ""),
            word_count=output.get("word_count", len(output.get("content", "").split())),
        )

        self.state.drafts[chapter_num] = draft
        progress = 0.5 + (0.4 * chapter_num / total_chapters)
        self.state.progress = progress

        print(f"   ✅ Chapter {chapter_num}: {draft.word_count} words")

        return draft

    async def critique_chapter(self, chapter_num: int) -> ChapterCritique:
        """Critique a chapter."""
        draft = self.state.drafts.get(chapter_num)
        if not draft:
            raise ValueError(f"No draft for chapter {chapter_num}")

        editor = self.agents["editor"]
        response = await editor.review_chapter(
            draft.model_dump(),
            {"title": self.one_sentence, "genre": self.intent.genre or "general", "total_chapters": len(self.state.blueprint.chapters) if self.state.blueprint else 0},
            {},
        )

        if not response.success:
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

        return critique

    async def iterate_chapter(self, chapter_num: int, max_iterations: int = 2) -> Chapter:
        """Iterate on a chapter."""
        for iteration in range(1, max_iterations + 1):
            critique = await self.critique_chapter(chapter_num)
            
            if critique.overall_score >= self.config.iteration.approval_threshold:
                print(f"   ✅ Chapter {chapter_num} approved! (score: {critique.overall_score:.2f})")
                break
            else:
                print(f"   🔄 Iteration {iteration}: score {critique.overall_score:.2f}")
        
        draft = self.state.drafts.get(chapter_num)
        
        return Chapter(
            chapter_number=chapter_num,
            title=draft.title,
            content=draft.content,
            word_count=draft.word_count,
        )

    async def generate_blueprint(self) -> BookBlueprint:
        """Generate the book blueprint."""
        words_per_chapter = 3000
        num_chapters = max(3, self.intent.target_word_count // words_per_chapter)
        
        blueprint = BookBlueprint(
            title=self.intent.working_title or "Untitled",
            genre=self.intent.genre or "general",
            target_audience=self.intent.target_audience,
            target_word_count=self.intent.target_word_count,
            structure="three-act",
            themes=[],
            tone=self.intent.tone or "neutral",
            chapters=[
                ChapterBlueprint(
                    chapter_number=i,
                    title=f"Chapter {i}",
                    summary=f"Chapter {i}",
                    word_count_target=words_per_chapter,
                )
                for i in range(1, num_chapters + 1)
            ],
        )

        self.state.blueprint = blueprint
        self.state.current_stage = "blueprint"
        self.state.progress = 0.1

        return blueprint

    async def compile_manuscript(self) -> Manuscript:
        """Compile all chapters into final manuscript."""
        num_chapters = len(self.state.blueprint.chapters)
        
        chapters = []
        for i in range(1, num_chapters + 1):
            await self.write_chapter(i, num_chapters)
            chapter = await self.iterate_chapter(i)
            chapters.append(chapter)

        manuscript = Manuscript(
            title=self.state.blueprint.title,
            book_type=self.book_type,
            genre=self.intent.genre or "general",
            chapters=chapters,
            total_word_count=sum(c.word_count for c in chapters),
            frontmatter={
                "one_sentence": self.one_sentence,
                "one_paragraph": self.one_paragraph,
                "include_toc": True,
            },
        )

        self.state.manuscript = manuscript
        self.state.current_stage = "complete"
        self.state.progress = 1.0

        return manuscript

    # =========================================================================
    # MAIN RUN METHOD - FULL SNOWFLAKE
    # =========================================================================

    async def run(self) -> Manuscript:
        """Run the full pipeline with selected framework."""
        framework_name = self.framework_info.get("name", "Unknown")
        
        print(f"\n{'='*60}")
        print(f"❄️  OPUS ORCHESTRATOR - {framework_name.upper()}")
        print(f"{'='*60}")
        print(f"Framework: {self.framework_info.get('description', '')}\n")

        await self.ingest()

        # Pre-writing stages
        await self.snowflake_stage_1()  # One sentence
        await self.snowflake_stage_2()  # One paragraph/outline with framework
        await self.snowflake_stage_3()  # Character sheets
        await self.snowflake_stage_4()  # Expanded outline
        await self.snowflake_stage_5()  # Detailed character charts
        await self.snowflake_stage_6()  # Scene list
        await self.snowflake_stage_7()  # Scene descriptions
        
        # Style and writing
        await self.create_style_guide()
        
        # Generate blueprint
        await self.generate_blueprint()

        # Write and critique chapters
        manuscript = await self.compile_manuscript()

        print(f"\n{'='*60}")
        print("✅ COMPLETE!")
        print(f"{'='*60}")
        print(f"📖 Title: {manuscript.title}")
        print(f"📄 Words: {manuscript.total_word_count:,}")
        print(f"📑 Chapters: {len(manuscript.chapters)}")
        print(f"🎯 Framework: {framework_name}")

        return manuscript

    def save_manuscript(self, output_path: Optional[Path] = None) -> Path:
        """Save manuscript and pre-writing to files."""
        if not self.state.manuscript:
            raise ValueError("No manuscript to save. Run first.")

        output_dir = output_path or Path("./output")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save manuscript
        manuscript_path = output_dir / f"{self.state.manuscript.title.lower().replace(' ', '_')}.md"
        with open(manuscript_path, "w") as f:
            f.write(self.state.manuscript.to_markdown())

        # Save pre-writing
        prewriting_path = output_dir / f"{self.state.manuscript.title.lower().replace(' ', '_')}_prewriting.md"
        with open(prewriting_path, "w") as f:
            f.write(f"# Pre-Writing: {self.state.manuscript.title}\n\n")
            f.write(f"## Stage 1: One Sentence\n{self.one_sentence}\n\n")
            f.write(f"## Stage 2: One Paragraph\n{self.one_paragraph}\n\n")
            f.write(f"## Stage 3: Character Sheets\n{self.character_sheets}\n\n")
            f.write(f"## Stage 4: Four-Page Outline\n{self.four_page_outline}\n\n")
            f.write(f"## Stage 5: Character Charts\n{self.character_charts}\n\n")
            f.write(f"## Stage 6: Scene List\n{self.scene_list}\n\n")
            f.write(f"## Stage 7: Scene Descriptions\n{self.scene_descriptions}\n\n")

        return manuscript_path
