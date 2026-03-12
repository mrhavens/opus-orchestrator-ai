"""LangGraph workflow for Opus Orchestrator - FIXED.

Proper synchronous implementation that works with LangGraph.
Uses sync httpx/requests to avoid event loop issues.
"""

import os
from typing import Any, Optional

from dotenv import load_dotenv

load_dotenv("/home/solaria/.openclaw/workspace/opus-orchestrator-ai/.env")

from pydantic import BaseModel, Field
from enum import Enum

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from opus_orchestrator.frameworks import get_framework_prompt, StoryFramework
from opus_orchestrator.utils.llm_sync import LLMClient


# ============== STATE SCHEMA ==============

class Stage(str, Enum):
    """Workflow stages."""
    SEED = "seed"
    ONE_SENTENCE = "one_sentence"
    ONE_PARAGRAPH = "one_paragraph"
    CHARACTER_SHEETS = "character_sheets"
    FOUR_PAGE_OUTLINE = "four_page_outline"
    CHARACTER_CHARTS = "character_charts"
    SCENE_LIST = "scene_list"
    SCENE_DESCRIPTIONS = "scene_descriptions"
    STYLE_GUIDE = "style_guide"
    WRITING = "writing"
    COMPLETE = "complete"


class Character(BaseModel):
    """Character schema."""
    name: str = ""
    role: str = ""
    description: str = ""
    want: str = ""
    need: str = ""
    fear: str = ""
    arc: str = ""


class PlotBeat(BaseModel):
    """Scene/beat schema."""
    name: str = ""
    description: str = ""


class ChapterPlan(BaseModel):
    """Chapter plan schema."""
    chapter_number: int = 0
    title: str = ""
    summary: str = ""
    word_count_target: int = 3000


class PreWriting(BaseModel):
    """Pre-writing output schema."""
    one_sentence: str = ""
    one_paragraph: str = ""
    characters: list[Character] = Field(default_factory=list)
    outline_sections: list[str] = Field(default_factory=list)
    character_details: dict[str, str] = Field(default_factory=dict)
    scene_list: list[PlotBeat] = Field(default_factory=list)
    chapter_plans: list[ChapterPlan] = Field(default_factory=list)
    scene_descriptions: dict[str, str] = Field(default_factory=dict)
    framework_used: str = "snowflake"


class ChapterState(BaseModel):
    """Chapter writing state."""
    content: str = ""
    word_count: int = 0
    critique_score: float = 0.0
    iterations: int = 0
    approved: bool = False


class OpusGraphState(BaseModel):
    """Main state for LangGraph."""
    stage: Stage = Stage.SEED
    framework: str = "snowflake"
    genre: str = "general"
    target_word_count: int = 80000
    seed_concept: str = ""
    
    prewriting: PreWriting = Field(default_factory=PreWriting)
    style_guide: str = ""
    
    current_chapter: int = 0
    chapters: dict[int, ChapterState] = Field(default_factory=dict)
    
    manuscript: str = ""
    total_word_count: int = 0
    
    validation_errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    
    progress: float = 0.0
    messages: list[str] = Field(default_factory=list)


# ============== WORKFLOW ==============

class OpusGraph:
    """LangGraph workflow - synchronous implementation."""
    
    def __init__(
        self,
        framework: str = "snowflake",
        genre: str = "general",
        target_word_count: int = 80000,
        api_key: Optional[str] = None,
    ):
        self.framework = framework
        self.genre = genre
        self.target_word_count = target_word_count
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        
        # Use synchronous LLM
        self.llm = LLMClient(api_key=self.api_key, provider="openai", model="gpt-4o")
        
        # Build graph
        self.graph = self._build_graph()
    
    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Call LLM synchronously."""
        return self.llm.complete(system_prompt, user_prompt)
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph."""
        
        workflow = StateGraph(OpusGraphState)
        
        # Add nodes
        workflow.add_node("seed", self.node_seed)
        workflow.add_node("one_sentence", self.node_one_sentence)
        workflow.add_node("one_paragraph", self.node_one_paragraph)
        workflow.add_node("character_sheets", self.node_character_sheets)
        workflow.add_node("four_page_outline", self.node_four_page_outline)
        workflow.add_node("character_charts", self.node_character_charts)
        workflow.add_node("scene_list", self.node_scene_list)
        workflow.add_node("scene_descriptions", self.node_scene_descriptions)
        workflow.add_node("style_guide", self.node_style_guide)
        workflow.add_node("write_chapters", self.node_write_chapters)
        workflow.add_node("complete", self.node_complete)
        
        # Edges
        workflow.set_entry_point("seed")
        workflow.add_edge("seed", "one_sentence")
        workflow.add_edge("one_sentence", "one_paragraph")
        workflow.add_edge("one_paragraph", "character_sheets")
        workflow.add_edge("character_sheets", "four_page_outline")
        workflow.add_edge("four_page_outline", "character_charts")
        workflow.add_edge("character_charts", "scene_list")
        workflow.add_edge("scene_list", "scene_descriptions")
        workflow.add_edge("scene_descriptions", "style_guide")
        workflow.add_edge("style_guide", "write_chapters")
        workflow.add_edge("write_chapters", "complete")
        
        checkpointer = MemorySaver()
        return workflow.compile(checkpointer=checkpointer)
    
    # ============== NODES ==============
    
    def node_seed(self, state: OpusGraphState) -> OpusGraphState:
        """Initialize from seed."""
        print(f"\n🌱 SEED: {state.seed_concept[:80]}...")
        state.messages.append(f"Started: {state.seed_concept[:50]}")
        state.stage = Stage.ONE_SENTENCE
        state.progress = 0.05
        return state
    
    def node_one_sentence(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 1: One sentence."""
        print("📝 STAGE 1: One sentence...")
        
        system_prompt = get_framework_prompt(StoryFramework(self.framework))
        user_prompt = f"""Create ONE SENTENCE that captures this story.

Must include:
- Protagonist
- Goal
- Conflict/obstacle
- Stakes

Seed: {state.seed_concept}
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        state.prewriting.one_sentence = result.strip()
        
        state.messages.append(f"One sentence: {state.prewriting.one_sentence[:60]}...")
        state.stage = Stage.ONE_SENTENCE
        state.progress = 0.12
        return state
    
    def node_one_paragraph(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 2: One paragraph."""
        print("📝 STAGE 2: One paragraph...")
        
        system_prompt = get_framework_prompt(StoryFramework(self.framework))
        user_prompt = f"""Expand to ONE PARAGRAPH (4-8 sentences):

Include: Opening, Setup, Catalyst, Rising Action, Midpoint, Complications, Crisis, Resolution

One sentence: {state.prewriting.one_sentence}
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        state.prewriting.one_paragraph = result.strip()
        
        state.messages.append("One paragraph complete")
        state.stage = Stage.ONE_PARAGRAPH
        state.progress = 0.20
        return state
    
    def node_character_sheets(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 3: Character sheets."""
        print("📝 STAGE 3: Character sheets...")
        
        system_prompt = "You are a character development expert."
        user_prompt = f"""Create character sheets for this story.

For each character:
- Name, Role (protagonist/antagonist/mentor/etc)
- Want (external goal)
- Need (internal growth)
- Fear

Story: {state.prewriting.one_paragraph}
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        
        # Parse characters
        characters = self._parse_characters(result)
        state.prewriting.characters = characters
        
        state.messages.append(f"Created {len(characters)} characters")
        state.stage = Stage.CHARACTER_SHEETS
        state.progress = 0.30
        return state
    
    def node_four_page_outline(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 4: Four-page outline."""
        print("📝 STAGE 4: Four-page outline...")
        
        system_prompt = get_framework_prompt(StoryFramework(self.framework))
        user_prompt = f"""Create a detailed outline.

Story: {state.prewriting.one_paragraph}
Characters: {', '.join(c.name for c in state.prewriting.characters)}
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        state.prewriting.outline_sections = [s.strip() for s in result.split("\n\n") if s.strip()]
        
        state.messages.append("Outline complete")
        state.stage = Stage.FOUR_PAGE_OUTLINE
        state.progress = 0.40
        return state
    
    def node_character_charts(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 5: Character charts."""
        print("📝 STAGE 5: Character charts...")
        
        system_prompt = "You are a character development expert."
        user_prompt = f"""Create detailed character profiles.

Characters: {', '.join(c.name for c in state.prewriting.characters)}

Include: Backstory, Psychology, Speech patterns, Key scenes
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        
        for char in state.prewriting.characters:
            state.prewriting.character_details[char.name] = result[:800]
        
        state.messages.append("Character charts complete")
        state.stage = Stage.CHARACTER_CHARTS
        state.progress = 0.50
        return state
    
    def node_scene_list(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 6: Scene list."""
        print("📝 STAGE 6: Scene list...")
        
        num_scenes = max(10, self.target_word_count // 1500)
        
        system_prompt = get_framework_prompt(StoryFramework(self.framework))
        user_prompt = f"""Create {num_scenes} scenes.

For each: name, description, POV, location

Story: {state.prewriting.one_paragraph}
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        
        scenes = self._parse_scenes(result)
        state.prewriting.scene_list = scenes
        
        # Create chapter plans
        num_chapters = max(3, self.target_word_count // 3000)
        scenes_per_ch = max(1, len(scenes) // num_chapters)
        
        for i in range(num_chapters):
            start = i * scenes_per_ch
            end = min(start + scenes_per_ch, len(scenes))
            state.prewriting.chapter_plans.append(ChapterPlan(
                chapter_number=i + 1,
                title=f"Chapter {i + 1}",
                summary=f"Chapter {i + 1}",
                word_count_target=self.target_word_count // num_chapters,
            ))
        
        state.messages.append(f"{len(scenes)} scenes, {num_chapters} chapters")
        state.stage = Stage.SCENE_LIST
        state.progress = 0.60
        return state
    
    def node_scene_descriptions(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 7: Scene descriptions."""
        print("📝 STAGE 7: Scene descriptions...")
        
        system_prompt = "You are a story architect."
        user_prompt = f"""Describe key scenes:

{chr(10).join(f"- {s.name}: {s.description[:80]}" for s in state.prewriting.scene_list[:10])}
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        state.prewriting.scene_descriptions = {"key_scenes": result[:2000]}
        
        state.messages.append("Scene descriptions complete")
        state.stage = Stage.SCENE_DESCRIPTIONS
        state.progress = 0.70
        return state
    
    def node_style_guide(self, state: OpusGraphState) -> OpusGraphState:
        """Create style guide."""
        print("🎨 STYLE GUIDE...")
        
        system_prompt = "You are a prose style expert."
        user_prompt = f"""Create a style guide for this story.

Genre: {self.genre}

Include: Tone, Voice, Sentence rhythm, Vocabulary level
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        state.style_guide = result.strip()
        
        state.messages.append("Style guide created")
        state.stage = Stage.STYLE_GUIDE
        state.progress = 0.75
        return state
    
    def node_write_chapters(self, state: OpusGraphState) -> OpusGraphState:
        """Write all chapters."""
        print("\n✍️  WRITING CHAPTERS...")
        
        system_prompt = f"""You are a professional novelist.
Style: {state.style_guide[:500] if state.style_guide else 'Professional fiction'}
"""
        
        for plan in state.prewriting.chapter_plans:
            print(f"   Writing chapter {plan.chapter_number}...")
            
            user_prompt = f"""Write Chapter {plan.chapter_number}: {plan.summary}

Story: {state.prewriting.one_sentence}
Characters: {', '.join(c.name for c in state.prewriting.characters[:3])}

Write ~{plan.word_count_target} words. Begin with chapter title.
"""
            
            result = self._call_llm(system_prompt, user_prompt)
            
            # Simple critique
            critique_score = 0.8  # Default for now
            
            state.chapters[plan.chapter_number] = ChapterState(
                content=result.strip(),
                word_count=len(result.split()),
                critique_score=critique_score,
                iterations=1,
                approved=critique_score >= 0.7,
            )
            
            state.messages.append(f"Chapter {plan.chapter_number}: {len(result.split())} words")
        
        state.stage = Stage.WRITING
        state.progress = 0.90
        return state
    
    def node_complete(self, state: OpusGraphState) -> OpusGraphState:
        """Complete."""
        # Compile manuscript
        parts = []
        for i in range(1, len(state.chapters) + 1):
            if i in state.chapters:
                parts.append(f"# Chapter {i}\n\n{state.chapters[i].content}")
        
        state.manuscript = "\n\n---\n\n".join(parts)
        state.total_word_count = sum(c.word_count for c in state.chapters.values())
        
        state.stage = Stage.COMPLETE
        state.progress = 1.0
        
        print(f"\n✅ COMPLETE!")
        print(f"   Chapters: {len(state.chapters)}")
        print(f"   Words: {state.total_word_count:,}")
        
        return state
    
    # ============== PARSING ==============
    
    def _parse_characters(self, text: str) -> list[Character]:
        """Parse characters from text."""
        characters = []
        
        for line in text.split("\n"):
            line = line.strip()
            lower = line.lower()
            
            if "name:" in lower and len(line) < 50:
                name = line.split(":", 1)[-1].strip()
                characters.append(Character(
                    name=name,
                    role="character",
                    description=line,
                    want="To be defined",
                    need="To be defined",
                    fear="Unknown",
                ))
        
        if not characters:
            characters.append(Character(
                name="Protagonist",
                role="protagonist",
                description="Main character",
                want="Complete the quest",
                need="Learn and grow",
                fear="Failure",
            ))
        
        return characters[:5]
    
    def _parse_scenes(self, text: str) -> list[PlotBeat]:
        """Parse scenes from text."""
        scenes = []
        
        for i, line in enumerate(text.split("\n")):
            line = line.strip()
            if line and len(line) > 10:
                scenes.append(PlotBeat(
                    name=f"Scene {i+1}",
                    description=line[:120],
                ))
        
        return scenes[:20] if scenes else [PlotBeat(name=f"Scene {i+1}", description=f"Beat {i+1}") for i in range(10)]
    
    # ============== RUN ==============
    
    def run(self, seed_concept: str, thread_id: str = "default") -> OpusGraphState:
        """Run the workflow."""
        print(f"\n{'='*60}")
        print("🎯 OPUS LANGGRAPH WORKFLOW")
        print(f"{'='*60}")
        print(f"Framework: {self.framework}")
        print(f"Target: {self.target_word_count:,} words\n")
        
        initial_state = OpusGraphState(
            seed_concept=seed_concept,
            framework=self.framework,
            genre=self.genre,
            target_word_count=self.target_word_count,
        )
        
        config = {"configurable": {"thread_id": thread_id}}
        
        # LangGraph stream - accumulate final state
        result_state = initial_state
        for node_output in self.graph.stream(initial_state, config):
            # node_output is {node_name: state}
            for key, state in node_output.items():
                if hasattr(state, 'stage'):  # It's an OpusGraphState
                    result_state = state
        
        return result_state


def run_opus(
    seed_concept: str,
    framework: str = "snowflake",
    genre: str = "general",
    target_word_count: int = 80000,
    thread_id: str = "default",
) -> OpusGraphState:
    """Convenience function."""
    api_key = os.environ.get("OPENAI_API_KEY")
    
    workflow = OpusGraph(
        framework=framework,
        genre=genre,
        target_word_count=target_word_count,
        api_key=api_key,
    )
    
    return workflow.run(seed_concept, thread_id)
