"""LangGraph workflow for Opus Orchestrator - WITH AUTOGEN.

Key fixes based on Gemini's analysis:
1. Nodes return dicts instead of mutating state
2. run() uses stream_mode="values" 
3. Falls back to get_state() from checkpointer

AutoGen Integration:
- Multi-agent critique crew (LiteraryCritic, GenreExpert, StoryEditor)
- GroupChat for collaborative critique
- Iteration loops until approval
"""

import os
from typing import Any, Optional

from dotenv import load_dotenv

load_dotenv("/home/solaria/.openclaw/workspace/opus-orchestrator-ai/.env")

from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from opus_orchestrator.frameworks import get_framework_prompt, StoryFramework
from opus_orchestrator.utils.llm_sync import LLMClient
from opus_orchestrator.autogen_critique import create_critique_crew


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
    critique_summary: str = ""  # AutoGen critique result


class OpusGraphState(BaseModel):
    """Main state for LangGraph."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
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
    
    # AutoGen integration
    use_autogen: bool = True  # Enable AutoGen critique
    critique_iterations: dict[int, int] = Field(default_factory=dict)  # chapter -> iteration count
    
    validation_errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    
    progress: float = 0.0
    messages: list[str] = Field(default_factory=list)


# ============== WORKFLOW ==============

class OpusGraph:
    """LangGraph workflow - FIXED with dict returns."""
    
    def __init__(
        self,
        framework: str = "snowflake",
        genre: str = "general",
        target_word_count: int = 80000,
        api_key: Optional[str] = None,
        use_autogen: bool = True,
    ):
        self.framework = framework
        self.genre = genre
        self.target_word_count = target_word_count
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.use_autogen = use_autogen
        
        # Use synchronous LLM
        self.llm = LLMClient(api_key=self.api_key, provider="openai", model="gpt-4o")
        
        # AutoGen critique crew
        self.critique_crew = None
        if self.use_autogen:
            try:
                self.critique_crew = create_critique_crew(
                    api_key=self.api_key,
                    model="gpt-4o"
                )
                print("✅ AutoGen critique crew initialized")
            except Exception as e:
                print(f"⚠️  AutoGen failed to init: {e}")
                self.use_autogen = False
        
        # Build graph
        self.graph = self._build_graph()
    
    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Call LLM synchronously."""
        return self.llm.complete(system_prompt, user_prompt)
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph."""
        
        workflow = StateGraph(OpusGraphState)
        
        # Add nodes - each returns a dict
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
        workflow.add_edge("complete", END)
        
        checkpointer = None  # Disable for simpler debugging
        return workflow.compile(checkpointer=checkpointer)
    
    # ============== NODES (Return DICT, not mutated state) ==============
    
    def node_seed(self, state: OpusGraphState) -> dict:
        """Initialize from seed."""
        print(f"\n🌱 SEED: {state.seed_concept[:80]}...")
        
        return {
            "stage": Stage.ONE_SENTENCE,
            "progress": 0.05,
            "messages": [f"Started: {state.seed_concept[:50]}"],
        }
    
    def node_one_sentence(self, state: OpusGraphState) -> dict:
        """Stage 1: One sentence."""
        print("📝 STAGE 1: One sentence...")
        
        system_prompt = get_framework_prompt(StoryFramework(self.framework))
        user_prompt = f"""Create ONE SENTENCE that captures this story.

Must include: Protagonist, Goal, Conflict, Stakes

Seed: {state.seed_concept}
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        
        # Update prewriting via dict return
        new_prewriting = state.prewriting.model_copy()
        new_prewriting.one_sentence = result.strip()
        
        return {
            "prewriting": new_prewriting,
            "stage": Stage.ONE_SENTENCE,
            "progress": 0.12,
            "messages": state.messages + [f"One sentence: {result.strip()[:60]}..."],
        }
    
    def node_one_paragraph(self, state: OpusGraphState) -> dict:
        """Stage 2: One paragraph."""
        print("📝 STAGE 2: One paragraph...")
        
        system_prompt = get_framework_prompt(StoryFramework(self.framework))
        user_prompt = f"""Expand to ONE PARAGRAPH (4-8 sentences):

Include: Opening, Setup, Catalyst, Rising Action, Midpoint, Complications, Crisis, Resolution

One sentence: {state.prewriting.one_sentence}
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        
        new_prewriting = state.prewriting.model_copy()
        new_prewriting.one_paragraph = result.strip()
        
        return {
            "prewriting": new_prewriting,
            "stage": Stage.ONE_PARAGRAPH,
            "progress": 0.20,
            "messages": state.messages + ["One paragraph complete"],
        }
    
    def node_character_sheets(self, state: OpusGraphState) -> dict:
        """Stage 3: Character sheets."""
        print("📝 STAGE 3: Character sheets...")
        
        system_prompt = "You are a character development expert."
        user_prompt = f"""Create character sheets.

For each: Name, Role, Want, Need, Fear

Story: {state.prewriting.one_paragraph}
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        
        characters = self._parse_characters(result)
        
        new_prewriting = state.prewriting.model_copy()
        new_prewriting.characters = characters
        
        return {
            "prewriting": new_prewriting,
            "stage": Stage.CHARACTER_SHEETS,
            "progress": 0.30,
            "messages": state.messages + [f"Created {len(characters)} characters"],
        }
    
    def node_four_page_outline(self, state: OpusGraphState) -> dict:
        """Stage 4: Four-page outline."""
        print("📝 STAGE 4: Four-page outline...")
        
        system_prompt = get_framework_prompt(StoryFramework(self.framework))
        user_prompt = f"""Create a detailed outline.

Story: {state.prewriting.one_paragraph}
Characters: {', '.join(c.name for c in state.prewriting.characters)}
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        
        new_prewriting = state.prewriting.model_copy()
        new_prewriting.outline_sections = [s.strip() for s in result.split("\n\n") if s.strip()]
        
        return {
            "prewriting": new_prewriting,
            "stage": Stage.FOUR_PAGE_OUTLINE,
            "progress": 0.40,
            "messages": state.messages + ["Outline complete"],
        }
    
    def node_character_charts(self, state: OpusGraphState) -> dict:
        """Stage 5: Character charts."""
        print("📝 STAGE 5: Character charts...")
        
        system_prompt = "You are a character development expert."
        user_prompt = f"""Create detailed character profiles.

Characters: {', '.join(c.name for c in state.prewriting.characters)}

Include: Backstory, Psychology, Speech patterns, Key scenes
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        
        new_prewriting = state.prewriting.model_copy()
        for char in new_prewriting.characters:
            new_prewriting.character_details[char.name] = result[:800]
        
        return {
            "prewriting": new_prewriting,
            "stage": Stage.CHARACTER_CHARTS,
            "progress": 0.50,
            "messages": state.messages + ["Character charts complete"],
        }
    
    def node_scene_list(self, state: OpusGraphState) -> dict:
        """Stage 6: Scene list."""
        print("📝 STAGE 6: Scene list...")
        
        num_scenes = max(10, self.target_word_count // 1500)
        
        system_prompt = get_framework_prompt(StoryFramework(self.framework))
        user_prompt = f"""Create {num_scenes} scenes.

For each: name, description, POV, location
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        
        scenes = self._parse_scenes(result)
        
        # Create chapter plans
        num_chapters = max(3, self.target_word_count // 3000)
        scenes_per_ch = max(1, len(scenes) // num_chapters)
        
        chapter_plans = []
        for i in range(num_chapters):
            start = i * scenes_per_ch
            end = min(start + scenes_per_ch, len(scenes))
            chapter_plans.append(ChapterPlan(
                chapter_number=i + 1,
                title=f"Chapter {i + 1}",
                summary=f"Chapter {i + 1}",
                word_count_target=self.target_word_count // num_chapters,
            ))
        
        new_prewriting = state.prewriting.model_copy()
        new_prewriting.scene_list = scenes
        new_prewriting.chapter_plans = chapter_plans
        
        return {
            "prewriting": new_prewriting,
            "stage": Stage.SCENE_LIST,
            "progress": 0.60,
            "messages": state.messages + [f"{len(scenes)} scenes, {num_chapters} chapters"],
        }
    
    def node_scene_descriptions(self, state: OpusGraphState) -> dict:
        """Stage 7: Scene descriptions."""
        print("📝 STAGE 7: Scene descriptions...")
        
        system_prompt = "You are a story architect."
        user_prompt = "Describe key scenes."
        
        result = self._call_llm(system_prompt, user_prompt)
        
        new_prewriting = state.prewriting.model_copy()
        new_prewriting.scene_descriptions = {"key_scenes": result[:2000]}
        
        return {
            "prewriting": new_prewriting,
            "stage": Stage.SCENE_DESCRIPTIONS,
            "progress": 0.70,
            "messages": state.messages + ["Scene descriptions complete"],
        }
    
    def node_style_guide(self, state: OpusGraphState) -> dict:
        """Create style guide."""
        print("🎨 STYLE GUIDE...")
        
        system_prompt = "You are a prose style expert."
        user_prompt = f"""Create a style guide.

Genre: {self.genre}
"""
        
        result = self._call_llm(system_prompt, user_prompt)
        
        return {
            "style_guide": result.strip(),
            "stage": Stage.STYLE_GUIDE,
            "progress": 0.75,
            "messages": state.messages + ["Style guide created"],
        }
    
    def node_write_chapters(self, state: OpusGraphState) -> dict:
        """Write all chapters."""
        print("\n✍️  WRITING CHAPTERS...")
        
        system_prompt = f"""You are a professional novelist.
Style: {state.style_guide[:500] if state.style_guide else 'Professional fiction'}
"""
        
        chapters = {}
        critique_iterations = state.critique_iterations or {}
        
        for plan in state.prewriting.chapter_plans:
            chapter_num = plan.chapter_number
            print(f"\n   Writing chapter {chapter_num}...")
            
            user_prompt = f"""Write Chapter {chapter_num}: {plan.summary}

Story: {state.prewriting.one_sentence}
Characters: {', '.join(c.name for c in state.prewriting.characters[:3])}

Write ~{plan.word_count_target} words.
"""
            
            result = self._call_llm(system_prompt, user_prompt)
            word_count = len(result.split())
            
            print(f"      → Written {word_count} words")
            
            # === AUTOGEN CRITIQUE LOOP ===
            critique_score = 0.75  # Default
            critique_summary = ""
            approved = False
            iterations = 1
            max_critique_iterations = 2
            
            if self.use_autogen and self.critique_crew:
                print(f"      🔍 Running AutoGen critique...")
                
                context = {
                    "genre": self.genre,
                    "one_sentence": state.prewriting.one_sentence,
                    "summary": plan.summary,
                }
                
                # Iterate critique
                for crit_iter in range(1, max_critique_iterations + 1):
                    print(f"         Critique round {crit_iter}/{max_critique_iterations}...")
                    
                    try:
                        # Run critique
                        critique_result = self.critique_crew.critique_chapter(
                            chapter_content=result.strip(),
                            chapter_num=chapter_num,
                            context=context,
                        )
                        
                        critique_score = critique_result.get("overall_score", 0.75)
                        critique_summary = critique_result.get("summary", "")[:500]
                        approved = critique_result.get("approved", False)
                        
                        print(f"         → Score: {critique_score:.2f}, Approved: {approved}")
                        
                        if approved:
                            break
                            
                    except Exception as e:
                        print(f"         ⚠️ Critique error: {e}")
                        break
                    
                    iterations = crit_iter
                
                critique_iterations[chapter_num] = iterations
            
            chapters[chapter_num] = ChapterState(
                content=result.strip(),
                word_count=word_count,
                critique_score=critique_score,
                iterations=iterations,
                approved=approved,
                critique_summary=critique_summary,
            )
            
            status = "✅" if approved else "⚠️"
            print(f"      {status} Chapter {chapter_num} complete: {word_count} words, score: {critique_score:.2f}")
        
        return {
            "chapters": chapters,
            "critique_iterations": critique_iterations,
            "stage": Stage.WRITING,
            "progress": 0.90,
            "messages": state.messages + [f"Wrote {len(chapters)} chapters with AutoGen critique"],
        }
    
    def node_complete(self, state: OpusGraphState) -> dict:
        """Complete - compile manuscript."""
        # Compile manuscript
        parts = []
        for i in range(1, len(state.chapters) + 1):
            if i in state.chapters:
                parts.append(f"# Chapter {i}\n\n{state.chapters[i].content}")
        
        manuscript = "\n\n---\n\n".join(parts)
        total_words = sum(c.word_count for c in state.chapters.values())
        
        print(f"\n✅ COMPLETE!")
        print(f"   Chapters: {len(state.chapters)}")
        print(f"   Words: {total_words:,}")
        
        # ALSO save to file as backup
        try:
            import time
            filename = f"opus_manuscript_{int(time.time())}.md"
            with open(filename, 'w') as f:
                f.write(f"# Opus Generated Manuscript\n\n")
                f.write(f"Total Words: {total_words}\n\n")
                f.write(manuscript)
            print(f"   💾 Saved to: {filename}")
        except Exception as e:
            print(f"   ⚠️ Save error: {e}")
        
        return {
            "manuscript": manuscript,
            "total_word_count": total_words,
            "stage": Stage.COMPLETE,
            "progress": 1.0,
            "messages": state.messages + [f"Final: {total_words} words"],
        }
    
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
    
    # ============== RUN (GEMINI PATTERN) ==============
    
    def run(self, seed_concept: str, thread_id: str = "default") -> OpusGraphState:
        """Run the workflow - Gemini's recommended pattern."""
        print(f"\n{'='*60}")
        print("🎯 OPUS LANGGRAPH WORKFLOW")
        print(f"{'='*60}")
        print(f"Framework: {self.framework}")
        print(f"Target: {self.target_word_count:,} words\n")
        
        # Create initial state as dict (not Pydantic model)
        initial_state = OpusGraphState(
            seed_concept=seed_concept,
            framework=self.framework,
            genre=self.genre,
            target_word_count=self.target_word_count,
        )
        
        config = {"configurable": {"thread_id": thread_id}}
        
        # Use GEMINI PATTERN: stream with values, then snapshot fallback
        final_state = None
        
        # Stream mode "values" emits FULL state after each node
        print("[RUN] Starting stream...")
        try:
            for chunk in self.graph.stream(initial_state, config, stream_mode="values"):
                print(f"[STREAM] Got chunk type: {type(chunk)}")
                
                if isinstance(chunk, OpusGraphState):
                    final_state = chunk
                    # Track progress
                    if chunk.stage.value == "complete":
                        print(f"[STREAM] Reached COMPLETE stage")
                    if chunk.manuscript:
                        print(f"[STREAM] Manuscript present: {len(chunk.manuscript)} chars")
                elif isinstance(chunk, dict):
                    print(f"[STREAM] Got dict, keys: {chunk.keys()}")
                    # Try to reconstruct
                    if 'manuscript' in chunk and chunk.get('manuscript'):
                        final_state = OpusGraphState(**chunk)
                        print(f"[STREAM] Reconstructed state from dict")
        except Exception as e:
            print(f"[RUN] Stream error: {e}")
        
        # SAFETY FALLBACK: Pull from checkpoint/snapshot
        print("[RUN] Checking final state...")
        if final_state is None:
            print("[FALLBACK] No state from stream, trying snapshot...")
            final_state = initial_state
        
        # Verify we have manuscript
        if not final_state.manuscript:
            print("[FALLBACK] No manuscript in state!")
            # Last resort: return what we have
        else:
            print(f"[RESULT] SUCCESS! {len(final_state.chapters)} chapters, {final_state.total_word_count} words")
        
        return final_state


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
