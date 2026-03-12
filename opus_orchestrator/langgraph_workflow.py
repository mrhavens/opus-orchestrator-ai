"""LangGraph workflow for Opus Orchestrator.

Real LangGraph implementation with:
- Compiled state graph
- Proper nodes for each stage
- Conditional edges for iteration
- Checkpoint state graph
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union

from dotenv import load_dotenv

load_dotenv("/home/solaria/.openclaw/workspace/opus-orchestrator-ai/.env")

from pydantic import BaseModel, Field
from enum import Enum

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from opus_orchestrator.agents.fiction import (
    ArchitectAgent,
    CharacterLeadAgent,
    EditorAgent,
    VoiceAgent,
)
from opus_orchestrator.config import AgentConfig
from opus_orchestrator.frameworks import get_framework_prompt, StoryFramework


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
    WRITING_CHAPTER = "writing_chapter"
    CRITIQUE_CHAPTER = "critique_chapter"
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
    chapter: Optional[int] = None


class ChapterPlan(BaseModel):
    """Chapter plan schema."""
    chapter_number: int = 0
    title: str = ""
    summary: str = ""
    word_count_target: int = 3000
    beats: list[str] = Field(default_factory=list)


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
    """Main state for LangGraph.
    
    This is the state that flows through the graph.
    """
    # Metadata
    stage: Stage = Stage.SEED
    framework: str = "snowflake"
    genre: str = "general"
    target_word_count: int = 80000
    seed_concept: str = ""
    
    # Pre-writing (structured)
    prewriting: PreWriting = Field(default_factory=PreWriting)
    
    # Style
    style_guide: str = ""
    
    # Writing
    current_chapter: int = 0
    chapters: dict[int, ChapterState] = Field(default_factory=dict)
    
    # Manuscript
    manuscript: str = ""
    total_word_count: int = 0
    
    # Validation & Errors
    validation_errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    
    # Progress
    progress: float = 0.0
    messages: list[str] = Field(default_factory=list)


# ============== VALIDATION ==============

def validate_all(state: OpusGraphState) -> OpusGraphState:
    """Run all validations."""
    errors = []
    warnings = []
    
    # Stage 1: One sentence
    if not state.prewriting.one_sentence:
        errors.append("Missing: one sentence")
    elif len(state.prewriting.one_sentence) > 200:
        warnings.append("One sentence is very long")
    
    # Stage 2: One paragraph
    if not state.prewriting.one_paragraph:
        errors.append("Missing: one paragraph")
    
    # Stage 3: Characters
    if not state.prewriting.characters:
        errors.append("Missing: characters")
    elif not any(c.role.lower() == "protagonist" for c in state.prewriting.characters):
        errors.append("Missing: protagonist")
    
    # Stage 4: Outline
    if not state.prewriting.outline_sections:
        errors.append("Missing: outline")
    
    # Stage 6: Scene list
    if len(state.prewriting.scene_list) < 5:
        errors.append(f"Too few scenes: {len(state.prewriting.scene_list)}")
    
    # Stage 7: Chapter plans
    if not state.prewriting.chapter_plans:
        errors.append("Missing: chapter plans")
    
    state.validation_errors = errors
    state.warnings = warnings
    
    return state


# ============== GRAPH NODES ==============

class OpusGraph:
    """LangGraph workflow for Opus."""
    
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
        
        # Initialize agents
        self.agent_config = AgentConfig(api_key=self.api_key)
        self.architect = ArchitectAgent(self.agent_config)
        self.character_lead = CharacterLeadAgent(self.agent_config)
        self.voice = VoiceAgent(self.agent_config)
        self.editor = EditorAgent(self.agent_config)
        
        # Build graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph."""
        
        # Create graph
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
        workflow.add_node("write_chapter", self.node_write_chapter)
        workflow.add_node("critique_chapter", self.node_critique_chapter)
        workflow.add_node("validate", self.node_validate)
        
        # Add edges
        workflow.set_entry_point("seed")
        
        workflow.add_edge("seed", "one_sentence")
        workflow.add_edge("one_sentence", "one_paragraph")
        workflow.add_edge("one_paragraph", "character_sheets")
        workflow.add_edge("character_sheets", "four_page_outline")
        workflow.add_edge("four_page_outline", "character_charts")
        workflow.add_edge("character_charts", "scene_list")
        workflow.add_edge("scene_list", "scene_descriptions")
        workflow.add_edge("scene_descriptions", "style_guide")
        workflow.add_edge("style_guide", "validate")
        
        # Conditional: continue writing or finish
        workflow.add_conditional_edges(
            "validate",
            self.should_continue_writing,
            {
                "continue": "write_chapter",
                "finish": END,
            }
        )
        
        # Writing loop
        workflow.add_edge("write_chapter", "critique_chapter")
        
        # Conditional: iterate or next chapter
        workflow.add_conditional_edges(
            "critique_chapter",
            self.should_iterate,
            {
                "iterate": "write_chapter",
                "next": "validate",
            }
        )
        
        # Compile with checkpointer
        checkpointer = MemorySaver()
        return workflow.compile(checkpointer=checkpointer)
    
    def should_continue_writing(self, state: OpusGraphState) -> str:
        """Decide whether to continue writing or finish."""
        # If no more chapters to write, finish
        if state.current_chapter >= len(state.prewriting.chapter_plans):
            return "finish"
        
        # Check for critical errors
        if len(state.validation_errors) > 3:
            print(f"⚠️  Too many validation errors: {state.validation_errors}")
            return "finish"
        
        return "continue"
    
    def should_iterate(self, state: OpusGraphState) -> str:
        """Decide whether to iterate on chapter or move on."""
        current = state.chapters.get(state.current_chapter, ChapterState())
        
        if current.approved:
            return "next"
        
        if current.iterations >= 3:
            print(f"⚠️  Max iterations reached for chapter {state.current_chapter}")
            return "next"
        
        if current.critique_score >= 0.8:
            return "next"
        
        return "iterate"
    
    # ============== NODE IMPLEMENTATIONS ==============
    
    def node_seed(self, state: OpusGraphState) -> OpusGraphState:
        """Initialize from seed."""
        print(f"\n🌱 SEED: {state.seed_concept[:100]}...")
        state.messages.append(f"Started with: {state.seed_concept[:100]}")
        state.stage = Stage.ONE_SENTENCE
        state.progress = 0.05
        return state
    
    def node_one_sentence(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 1: One sentence summary."""
        print("\n📝 STAGE 1: One sentence...")
        
        import asyncio
        framework_prompt = get_framework_prompt(StoryFramework(self.framework))
        
        user_prompt = f"""Create ONE SENTENCE that captures this entire story.

Requirements:
- Include protagonist
- Include their goal
- Include the conflict/obstacle
- Include the stakes

Seed: {state.seed_concept}
"""
        
        result = asyncio.run(self.architect.call_llm(framework_prompt, user_prompt))
        
        state.prewriting.one_sentence = result.strip()
        state.messages.append(f"One sentence: {state.prewriting.one_sentence[:80]}...")
        state.stage = Stage.ONE_SENTENCE
        state.progress = 0.10
        
        return state
    
    def node_one_paragraph(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 2: One paragraph outline."""
        print("📝 STAGE 2: One paragraph...")
        
        import asyncio
        framework_prompt = get_framework_prompt(StoryFramework(self.framework))
        
        user_prompt = f"""Expand to ONE PARAGRAPH (4-8 sentences):

Include:
- Opening image
- Setup/normal world
- Catalyst
- Rising action
- Midpoint
- Complications
- Crisis
- Resolution

One sentence: {state.prewriting.one_sentence}
"""
        
        result = asyncio.run(self.architect.call_llm(framework_prompt, user_prompt))
        
        state.prewriting.one_paragraph = result.strip()
        state.messages.append("One paragraph outline complete")
        state.stage = Stage.ONE_PARAGRAPH
        state.progress = 0.15
        
        return state
    
    def node_character_sheets(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 3: Character sheets."""
        print("📝 STAGE 3: Character sheets...")
        
        import asyncio
        result = asyncio.run(self.character_lead.execute(
            {"characters": [], "raw_content": state.prewriting.one_paragraph},
            {},
        ))
        
        # Parse characters
        text = result.output if isinstance(result.output, str) else str(result.output)
        characters = self._parse_characters(text)
        state.prewriting.characters = characters
        
        state.messages.append(f"Created {len(characters)} characters")
        state.stage = Stage.CHARACTER_SHEETS
        state.progress = 0.25
        
        return state
    
    def node_four_page_outline(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 4: Four page outline."""
        print("📝 STAGE 4: Four-page outline...")
        
        import asyncio
        framework_prompt = get_framework_prompt(StoryFramework(self.framework))
        
        user_prompt = f"""Create a detailed outline (4 pages worth):

Outline: {state.prewriting.one_paragraph}

Characters: {', '.join(c.name for c in state.prewriting.characters)}
"""
        
        result = asyncio.run(self.architect.call_llm(framework_prompt, user_prompt))
        
        state.prewriting.outline_sections = [s.strip() for s in result.split("\n\n") if s.strip()]
        state.messages.append("Four-page outline complete")
        state.stage = Stage.FOUR_PAGE_OUTLINE
        state.progress = 0.35
        
        return state
    
    def node_character_charts(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 5: Detailed character charts."""
        print("📝 STAGE 5: Character charts...")
        
        import asyncio
        result = asyncio.run(self.character_lead.execute(
            {"characters": [], "raw_content": state.prewriting.one_paragraph},
            {},
        ))
        
        text = result.output if isinstance(result.output, str) else str(result.output)
        
        for char in state.prewriting.characters:
            state.prewriting.character_details[char.name] = text[:1000]
        
        state.messages.append("Character charts complete")
        state.stage = Stage.CHARACTER_CHARTS
        state.progress = 0.40
        
        return state
    
    def node_scene_list(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 6: Scene list."""
        print("📝 STAGE 6: Scene list...")
        
        import asyncio
        framework_prompt = get_framework_prompt(StoryFramework(self.framework))
        
        num_scenes = max(10, self.target_word_count // 1500)
        
        user_prompt = f"""Create {num_scenes} scenes.

For each: name, description, POV character, location, purpose.
"""
        
        result = asyncio.run(self.architect.call_llm(framework_prompt, user_prompt))
        
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
                summary=f"Chapter {i + 1} covering scenes {start+1}-{end}",
                word_count_target=self.target_word_count // num_chapters,
                beats=[s.name for s in scenes[start:end]],
            ))
        
        state.messages.append(f"Created {len(scenes)} scenes, {num_chapters} chapters")
        state.stage = Stage.SCENE_LIST
        state.progress = 0.50
        
        return state
    
    def node_scene_descriptions(self, state: OpusGraphState) -> OpusGraphState:
        """Stage 7: Scene descriptions."""
        print("📝 STAGE 7: Scene descriptions...")
        
        import asyncio
        user_prompt = f"""Describe key scenes:

{chr(10).join(f"- {s.name}: {s.description}" for s in state.prewriting.scene_list[:10])}
"""
        
        result = asyncio.run(self.architect.call_llm(
            "You are an expert story architect. Create vivid scene descriptions.",
            user_prompt,
        ))
        
        state.prewriting.scene_descriptions = self._parse_descriptions(result)
        state.messages.append("Scene descriptions complete")
        state.stage = Stage.SCENE_DESCRIPTIONS
        state.progress = 0.55
        
        return state
    
    def node_style_guide(self, state: OpusGraphState) -> OpusGraphState:
        """Create style guide."""
        print("🎨 STYLE GUIDE...")
        
        import asyncio
        result = asyncio.run(self.voice.execute(
            {"genre": self.genre, "tone": "neutral", "target_audience": "adult readers"},
            {},
        ))
        
        state.style_guide = result.output if isinstance(result.output, str) else str(result.output)
        state.messages.append("Style guide created")
        state.stage = Stage.STYLE_GUIDE
        state.progress = 0.60
        
        return state
    
    def node_validate(self, state: OpusGraphState) -> OpusGraphState:
        """Validate and prepare for writing."""
        print("✅ VALIDATION...")
        state = validate_all(state)
        
        if state.validation_errors:
            print(f"⚠️  Validation errors: {state.validation_errors}")
        if state.warnings:
            print(f"💡 Warnings: {state.warnings}")
        
        # Initialize first chapter if needed
        if state.current_chapter == 0:
            state.current_chapter = 1
        
        state.progress = 0.65
        return state
    
    def node_write_chapter(self, state: OpusGraphState) -> OpusGraphState:
        """Write a chapter."""
        chapter_num = state.current_chapter
        
        # Get chapter plan
        plan = state.prewriting.chapter_plans[chapter_num - 1] if chapter_num <= len(state.prewriting.chapter_plans) else None
        
        print(f"\n✍️  Writing chapter {chapter_num}...")
        
        import asyncio
        
        # Build context
        context = f"""
## Story: {state.prewriting.one_sentence}

## Characters:
{chr(10).join(f"- {c.name} ({c.role}): {c.description[:100]}" for c in state.prewriting.characters[:5])}

## Style: {state.style_guide[:500]}...

## Chapter plan: {plan.summary if plan else 'Continue the story'}
"""
        
        result = asyncio.run(self.voice.write_chapter(
            {
                "chapter_number": chapter_num,
                "title": f"Chapter {chapter_num}",
                "summary": plan.summary if plan else "Continue",
                "word_count_target": plan.word_count_target if plan else 3000,
            },
            context,
            {},
        ))
        
        output = result.output if isinstance(result.output, dict) else {"content": str(result.output)}
        
        state.chapters[chapter_num] = ChapterState(
            content=output.get("content", ""),
            word_count=output.get("word_count", len(output.get("content", "").split())),
            iterations=state.chapters.get(chapter_num, ChapterState()).iterations + 1,
        )
        
        state.messages.append(f"Chapter {chapter_num} written: {state.chapters[chapter_num].word_count} words")
        
        return state
    
    def node_critique_chapter(self, state: OpusGraphState) -> OpusGraphState:
        """Critique a chapter."""
        chapter_num = state.current_chapter
        chapter = state.chapters.get(chapter_num, ChapterState())
        
        print(f"🔍 Critiquing chapter {chapter_num}...")
        
        import asyncio
        result = asyncio.run(self.editor.review_chapter(
            {
                "chapter_number": chapter_num,
                "title": f"Chapter {chapter_num}",
                "content": chapter.content[:3000],
            },
            {"title": state.prewriting.one_sentence, "genre": self.genre, "total_chapters": len(state.prewriting.chapter_plans)},
            {},
        ))
        
        output = result.output if isinstance(result.output, dict) else {"score": 0.7}
        
        chapter.critique_score = output.get("score", 0.7)
        chapter.approved = chapter.critique_score >= 0.8
        
        state.chapters[chapter_num] = chapter
        
        status = "✅ APPROVED" if chapter.approved else f"🔄 Score: {chapter.critique_score:.2f}"
        print(f"{status}")
        
        state.messages.append(f"Chapter {chapter_num} critique: {chapter.critique_score:.2f}")
        
        return state
    
    # ============== PARSING HELPERS ==============
    
    def _parse_characters(self, text: str) -> list[Character]:
        """Parse characters from text."""
        characters = []
        
        # Simple parsing - look for name patterns
        lines = text.split("\n")
        current = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            lower = line.lower()
            if "name:" in lower:
                if current and current.get("name"):
                    characters.append(Character(**current))
                current = {"name": line.split(":", 1)[-1].strip()}
            elif "role:" in lower:
                current["role"] = line.split(":", 1)[-1].strip()
            elif "want:" in lower:
                current["want"] = line.split(":", 1)[-1].strip()
            elif "need:" in lower:
                current["need"] = line.split(":", 1)[-1].strip()
            elif "fear:" in lower:
                current["fear"] = line.split(":", 1)[-1].strip()
        
        if current and current.get("name"):
            characters.append(Character(**current))
        
        # Ensure protagonist
        if not characters:
            characters.append(Character(
                name="Protagonist",
                role="protagonist",
                description="Main character",
                want="Complete the quest",
                need="Learn and grow",
                fear="Failure",
                arc="Transform through journey",
            ))
        
        return characters
    
    def _parse_scenes(self, text: str) -> list[PlotBeat]:
        """Parse scenes from text."""
        scenes = []
        
        for i, line in enumerate(text.split("\n")):
            line = line.strip()
            if line and len(line) > 10:
                scenes.append(PlotBeat(
                    name=f"Scene {i+1}",
                    description=line[:150],
                ))
        
        return scenes[:20] if scenes else [PlotBeat(name=f"Scene {i+1}", description=f"Story beat {i+1}") for i in range(10)]
    
    def _parse_descriptions(self, text: str) -> dict[str, str]:
        """Parse scene descriptions."""
        descriptions = {}
        sections = text.split("\n\n")
        
        for i, section in enumerate(sections):
            if section.strip():
                descriptions[f"scene_{i+1}"] = section.strip()[:500]
        
        return descriptions
    
    # ============== RUN ==============
    
    def run(
        self,
        seed_concept: str,
        thread_id: str = "default",
    ) -> OpusGraphState:
        """Run the workflow."""
        print(f"\n{'='*60}")
        print(f"🎯 OPUS LANGGRAPH WORKFLOW")
        print(f"{'='*60}")
        print(f"Framework: {self.framework}")
        print(f"Target: {self.target_word_count:,} words\n")
        
        # Initial state
        initial_state = OpusGraphState(
            seed_concept=seed_concept,
            framework=self.framework,
            genre=self.genre,
            target_word_count=self.target_word_count,
        )
        
        # Run with thread
        config = {"configurable": {"thread_id": thread_id}}
        
        final_state = None
        for state in self.graph.stream(initial_state, config):
            final_state = state
        
        if final_state:
            result = list(final_state.values())[0]
            
            # Compile manuscript
            manuscript_parts = []
            for i in range(1, len(result.chapters) + 1):
                if i in result.chapters:
                    manuscript_parts.append(f"# Chapter {i}\n\n{result.chapters[i].content}")
            
            result.manuscript = "\n\n---\n\n".join(manuscript_parts)
            result.total_word_count = sum(c.word_count for c in result.chapters.values())
            result.stage = Stage.COMPLETE
            result.progress = 1.0
            
            print(f"\n{'='*60}")
            print("✅ COMPLETE!")
            print(f"{'='*60}")
            print(f"📖 Chapters: {len(result.chapters)}")
            print(f"📄 Words: {result.total_word_count:,}")
            
            return result
        
        return initial_state


# Convenience function

def run_opus(
    seed_concept: str,
    framework: str = "snowflake",
    genre: str = "general",
    target_word_count: int = 80000,
    thread_id: str = "default",
) -> OpusGraphState:
    """Run Opus workflow."""
    api_key = os.environ.get("OPENAI_API_KEY")
    
    workflow = OpusGraph(
        framework=framework,
        genre=genre,
        target_word_count=target_word_count,
        api_key=api_key,
    )
    
    return workflow.run(seed_concept, thread_id)
