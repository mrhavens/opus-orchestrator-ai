"""LangGraph workflow nodes for Opus Orchestrator.

Contains the workflow graph with:
- Stage nodes (one sentence, character sheets, outline, etc.)
- Validation nodes
- Iteration loops for writing
- Checkpoint management
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

from opus_orchestrator.agents.fiction import (
    ArchitectAgent,
    CharacterLeadAgent,
    EditorAgent,
    VoiceAgent,
    WorldsmithAgent,
)
from opus_orchestrator.config import AgentConfig
from opus_orchestrator.frameworks import get_framework_prompt, StoryFramework
from opus_orchestrator.langgraph_state import (
    OpusState,
    Stage,
    Character,
    ChapterPlan,
    PlotBeat,
    PreWriting,
    WritingState,
    create_initial_state,
    get_progress,
    validate_character_sheets,
    validate_one_paragraph,
    validate_one_sentence,
    validate_prewriting_complete,
    validate_scene_list,
)
from opus_orchestrator.schemas import BookIntent, BookType


# Checkpoint management

CHECKPOINT_DIR = Path("./checkpoints")


def save_checkpoint(state: OpusState, checkpoint_id: str = "default") -> Path:
    """Save state checkpoint to disk."""
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    
    checkpoint_file = CHECKPOINT_DIR / f"checkpoint_{checkpoint_id}.json"
    
    # Convert to JSON-serializable dict
    data = {
        "stage": state.stage.value,
        "framework": state.framework,
        "genre": state.genre,
        "target_word_count": state.target_word_count,
        "seed_concept": state.seed_concept,
        "prewriting": state.prewriting.model_dump() if state.prewriting else {},
        "style_guide": state.style_guide,
        "writing": state.writing.model_dump() if state.writing else {},
        "manuscript": state.manuscript,
        "total_word_count": state.total_word_count,
        "validation_errors": state.validation_errors,
        "warnings": state.warnings,
        "progress": state.progress,
        "last_updated": datetime.utcnow().isoformat(),
    }
    
    with open(checkpoint_file, "w") as f:
        json.dump(data, f, indent=2)
    
    return checkpoint_file


def load_checkpoint(checkpoint_id: str = "default") -> Optional[OpusState]:
    """Load state checkpoint from disk."""
    checkpoint_file = CHECKPOINT_DIR / f"checkpoint_{checkpoint_id}.json"
    
    if not checkpoint_file.exists():
        return None
    
    with open(checkpoint_file, "r") as f:
        data = json.load(f)
    
    # Reconstruct state
    prewriting_data = data.get("prewriting", {})
    prewriting = PreWriting(**prewriting_data) if prewriting_data else PreWriting()
    
    writing_data = data.get("writing", {})
    writing = WritingState(**writing_data) if writing_data else WritingState()
    
    state = OpusState(
        stage=Stage(data.get("stage", "seed")),
        framework=data.get("framework", "snowflake"),
        genre=data.get("genre", "general"),
        target_word_count=data.get("target_word_count", 80000),
        seed_concept=data.get("seed_concept", ""),
        prewriting=prewriting,
        style_guide=data.get("style_guide", ""),
        writing=writing,
        manuscript=data.get("manuscript", ""),
        total_word_count=data.get("total_word_count", 0),
        validation_errors=data.get("validation_errors", []),
        warnings=data.get("warnings", []),
        progress=data.get("progress", 0.0),
    )
    
    return state


# Workflow nodes

class OpusWorkflow:
    """LangGraph workflow for Opus Orchestrator."""
    
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
        self.api_key = api_key
        
        # Initialize agents
        agent_config = AgentConfig(api_key=api_key)
        self.architect = ArchitectAgent(agent_config)
        self.character_lead = CharacterLeadAgent(agent_config)
        self.voice = VoiceAgent(agent_config)
        self.editor = EditorAgent(agent_config)
    
    def stage_1_one_sentence(self, state: OpusState) -> OpusState:
        """Generate one sentence summary."""
        # Use framework-specific prompting
        framework_prompt = get_framework_prompt(StoryFramework(self.framework))
        
        user_prompt = f"""Create a ONE SENTENCE summary of this story concept.

The sentence should contain:
- Protagonist's name (or descriptor)
- Their goal
- The conflict/obstacle
- The stakes

Example: "In a world where magic is forbidden, a young mage must master forbidden arts to save her dying brother, even if it means sparking a war with the ruling theocracy."

## Your seed concept:
{state.seed_concept}

## Task:
Write ONE compelling sentence that captures the entire story.
"""
        
        # Call LLM
        import asyncio
        result = asyncio.run(self.architect.call_llm(framework_prompt, user_prompt))
        
        # Parse and validate
        state.prewriting.one_sentence = result.strip()
        state.validation_errors = validate_one_sentence(state)
        state.stage = Stage.ONE_SENTENCE
        state.progress = get_progress(Stage.ONE_SENTENCE)
        state.last_updated = datetime.utcnow().isoformat()
        
        # Save checkpoint
        save_checkpoint(state)
        
        return state
    
    def stage_2_one_paragraph(self, state: OpusState) -> OpusState:
        """Generate one paragraph outline."""
        framework_prompt = get_framework_prompt(StoryFramework(self.framework))
        
        user_prompt = f"""Expand this one-sentence summary into a full one-paragraph story outline.

Include:
- Opening image (the "before" state)
- Setup (normal world, who the protagonist is)
- Catalyst (what changes everything)
- Rising action (attempts to solve the problem)
- Midpoint (major twist or revelation)
- Complications (things get worse)
- Crisis (lowest point)
- Resolution (how it ends)

## One sentence:
{state.prewriting.one_sentence}

## Task:
Write one detailed paragraph (4-8 sentences) that tells the complete story arc.
"""
        
        import asyncio
        result = asyncio.run(self.architect.call_llm(framework_prompt, user_prompt))
        
        state.prewriting.one_paragraph = result.strip()
        state.validation_errors = validate_one_paragraph(state)
        state.stage = Stage.ONE_PARAGRAPH
        state.progress = get_progress(Stage.ONE_PARAGRAPH)
        state.last_updated = datetime.utcnow().isoformat()
        
        save_checkpoint(state)
        
        return state
    
    def stage_3_character_sheets(self, state: OpusState) -> OpusState:
        """Generate character sheets (structured)."""
        user_prompt = f"""Create character sheets for all major characters in this story.

For each character, provide:
- Name
- Role (protagonist, antagonist, love interest, mentor, etc.)
- Age and physical description
- Background/history (2-3 sentences)
- Want (external goal)
- Need (internal growth)
- Fear
- Secret (if any)
- Character arc (how do they change?)

## Story outline:
{state.prewriting.one_paragraph}

## Task:
Create comprehensive character sheets. Return as a list with each character clearly defined.
"""
        
        import asyncio
        result = asyncio.run(self.character_lead.execute(
            {"characters": [], "raw_content": state.prewriting.one_paragraph},
            {},
        ))
        
        # Parse characters from result (basic parsing - could be improved)
        text = result.output if isinstance(result.output, str) else str(result.output)
        
        # Extract characters (simplified - in production would use better parsing)
        characters = self._parse_characters(text)
        
        state.prewriting.characters = characters
        state.prewriting.framework_used = self.framework
        state.validation_errors = validate_character_sheets(state)
        state.stage = Stage.CHARACTER_SHEETS
        state.progress = get_progress(Stage.CHARACTER_SHEETS)
        state.last_updated = datetime.utcnow().isoformat()
        
        save_checkpoint(state)
        
        return state
    
    def stage_4_four_page_outline(self, state: OpusState) -> OpusState:
        """Generate four-page outline."""
        framework_prompt = get_framework_prompt(StoryFramework(self.framework))
        
        user_prompt = f"""Expand this one-paragraph outline into a detailed four-page outline.

For each major section, provide:
- Multiple scenes
- Character motivations
- Plot developments
- World details
- Dialogue hooks

## Current outline:
{state.prewriting.one_paragraph}

## Characters:
{', '.join(c.name for c in state.prewriting.characters)}

## Task:
Write a comprehensive four-page outline covering the entire story.
"""
        
        import asyncio
        result = asyncio.run(self.architect.call_llm(framework_prompt, user_prompt))
        
        # Parse outline sections
        state.prewriting.outline_sections = [s.strip() for s in result.split("\n\n") if s.strip()]
        state.stage = Stage.FOUR_PAGE_OUTLINE
        state.progress = get_progress(Stage.FOUR_PAGE_OUTLINE)
        state.last_updated = datetime.utcnow().isoformat()
        
        save_checkpoint(state)
        
        return state
    
    def stage_5_character_charts(self, state: OpusState) -> OpusState:
        """Generate detailed character charts."""
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
{chr(10).join(f"- {c.name}: {c.role}" for c in state.prewriting.characters)}

## Task:
Write comprehensive, detailed character charts.
"""
        
        import asyncio
        result = asyncio.run(self.character_lead.execute(
            {"characters": [], "raw_content": state.prewriting.one_paragraph},
            {},
        ))
        
        text = result.output if isinstance(result.output, str) else str(result.output)
        
        # Store character details
        for char in state.prewriting.characters:
            state.prewriting.character_details[char.name] = text
        
        state.stage = Stage.CHARACTER_CHARTS
        state.progress = get_progress(Stage.CHARACTER_CHARTS)
        state.last_updated = datetime.utcnow().isoformat()
        
        save_checkpoint(state)
        
        return state
    
    def stage_6_scene_list(self, state: OpusState) -> OpusState:
        """Generate scene list (structured)."""
        framework_prompt = get_framework_prompt(StoryFramework(self.framework))
        
        words_per_scene = 1500
        num_scenes = max(10, self.target_word_count // words_per_scene)
        
        user_prompt = f"""Create a SCENE LIST for this story.

For each scene, provide:
- Scene name/number
- What happens (brief description)
- POV character
- Location
- Purpose (advances plot? reveals character?)

Target: {num_scenes} scenes

## Outline:
{chr(10).join(state.prewriting.outline_sections[:3])}

## Characters:
{', '.join(c.name for c in state.prewriting.characters)}

## Task:
Create a comprehensive scene list.
"""
        
        import asyncio
        result = asyncio.run(self.architect.call_llm(framework_prompt, user_prompt))
        
        # Parse scenes
        scenes = self._parse_scenes(result)
        state.prewriting.scene_list = scenes
        
        # Also create chapter plans
        num_chapters = max(3, self.target_word_count // 3000)
        state.prewriting.chapter_plans = self._create_chapter_plans(num_chapters, scenes)
        
        state.validation_errors = validate_scene_list(state)
        state.stage = Stage.SCENE_LIST
        state.progress = get_progress(Stage.SCENE_LIST)
        state.last_updated = datetime.utcnow().isoformat()
        
        save_checkpoint(state)
        
        return state
    
    def stage_7_scene_descriptions(self, state: OpusState) -> OpusState:
        """Generate scene descriptions."""
        user_prompt = f"""Expand key scenes into detailed descriptions.

For each key scene, provide:
- Opening beat
- Key dialogue points
- Conflict moment
- Turning point
- Closing beat

## Scene list:
{chr(10).join(f"- {s.name}: {s.description}" for s in state.prewriting.scene_list[:10])}

## Task:
Write detailed descriptions for at least 10 key scenes.
"""
        
        import asyncio
        result = asyncio.run(self.architect.call_llm(
            "You are an expert story architect. Create vivid scene descriptions.",
            user_prompt,
        ))
        
        # Parse into dict
        state.prewriting.scene_descriptions = self._parse_scene_descriptions(result)
        
        state.stage = Stage.SCENE_DESCRIPTIONS
        state.progress = get_progress(Stage.SCENE_DESCRIPTIONS)
        state.last_updated = datetime.utcnow().isoformat()
        
        save_checkpoint(state)
        
        return state
    
    def create_style_guide(self, state: OpusState) -> OpusState:
        """Create style guide."""
        user_prompt = f"""Create a voice/style guide for this story.

- Genre: {self.genre}
- Target audience: adult readers

## One sentence:
{state.prewriting.one_sentence}

## Task:
Create a comprehensive style guide.
"""
        
        import asyncio
        result = asyncio.run(self.voice.execute(
            {"genre": self.genre, "tone": "neutral", "target_audience": "adult readers"},
            {},
        ))
        
        state.style_guide = result.output if isinstance(result.output, str) else str(result.output)
        
        state.stage = Stage.STYLE_GUIDE
        state.progress = get_progress(Stage.STYLE_GUIDE)
        state.last_updated = datetime.utcnow().isoformat()
        
        save_checkpoint(state)
        
        return state
    
    # Helper parsing functions
    
    def _parse_characters(self, text: str) -> list[Character]:
        """Parse characters from LLM output."""
        characters = []
        lines = text.split("\n")
        current_char = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Simple parsing - look for patterns
            lower = line.lower()
            if "name:" in lower or (line and line[0].isupper() and len(line) < 30):
                if current_char and "name" in current_char:
                    characters.append(Character(**current_char))
                current_char = {"name": line.split(":")[-1].strip() if ":" in line else line}
            elif "role:" in lower:
                current_char["role"] = line.split(":")[-1].strip()
            elif "want:" in lower:
                current_char["want"] = line.split(":")[-1].strip()
            elif "need:" in lower:
                current_char["need"] = line.split(":")[-1].strip()
            elif "fear:" in lower:
                current_char["fear"] = line.split(":")[-1].strip()
            elif "arc:" in lower:
                current_char["arc"] = line.split(":")[-1].strip()
        
        # Add last character
        if current_char and "name" in current_char:
            characters.append(Character(**current_char))
        
        # Ensure at least one character
        if not characters:
            characters.append(Character(
                name="Protagonist",
                role="protagonist",
                description="Main character",
                want="Complete the quest",
                need="Learn to trust others",
                fear="Failure",
                arc="Grows from isolated to connected",
            ))
        
        return characters
    
    def _parse_scenes(self, text: str) -> list[PlotBeat]:
        """Parse scenes from LLM output."""
        scenes = []
        lines = text.split("\n")
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Extract scene info
            parts = line.split("-", 1)
            if len(parts) > 1:
                scenes.append(PlotBeat(
                    name=f"Scene {i+1}",
                    description=parts[1].strip()[:200],
                ))
        
        # Ensure minimum scenes
        if not scenes:
            scenes = [PlotBeat(name=f"Scene {i+1}", description=f"Story beat {i+1}") 
                      for i in range(10)]
        
        return scenes[:20]  # Limit to 20
    
    def _parse_scene_descriptions(self, text: str) -> dict[str, str]:
        """Parse scene descriptions from LLM output."""
        descriptions = {}
        sections = text.split("\n\n")
        
        for i, section in enumerate(sections):
            if section.strip():
                descriptions[f"scene_{i+1}"] = section.strip()[:500]
        
        return descriptions
    
    def _create_chapter_plans(self, num_chapters: int, scenes: list[PlotBeat]) -> list[ChapterPlan]:
        """Create chapter plans from scenes."""
        scenes_per_chapter = max(1, len(scenes) // num_chapters)
        plans = []
        
        for i in range(num_chapters):
            start_idx = i * scenes_per_chapter
            end_idx = min(start_idx + scenes_per_chapter, len(scenes))
            chapter_scenes = scenes[start_idx:end_idx] if scenes else []
            
            plans.append(ChapterPlan(
                chapter_number=i + 1,
                title=f"Chapter {i + 1}",
                summary=f"Chapter {i + 1} with {len(chapter_scenes)} scenes",
                word_count_target=self.target_word_count // num_chapters,
                beats=[s.name for s in chapter_scenes],
            ))
        
        return plans


# Simplified workflow runner (would use actual LangGraph in production)

def run_workflow(
    seed_concept: str,
    framework: str = "snowflake",
    genre: str = "general",
    target_word_count: int = 80000,
    api_key: Optional[str] = None,
    checkpoint_id: Optional[str] = None,
) -> OpusState:
    """Run the complete workflow.
    
    In production, this would use actual LangGraph graph.walk()
    For now, uses sequential execution with checkpoints.
    """
    
    # Try to load checkpoint
    if checkpoint_id:
        state = load_checkpoint(checkpoint_id)
        if state:
            print(f"📂 Loaded checkpoint: {state.stage}")
    else:
        state = None
    
    # Create workflow
    workflow = OpusWorkflow(
        framework=framework,
        genre=genre,
        target_word_count=target_word_count,
        api_key=api_key,
    )
    
    # Run stages in order (skipping completed)
    if not state or state.stage == Stage.SEED:
        state = create_initial_state(seed_concept, framework, genre, target_word_count)
        state = workflow.stage_1_one_sentence(state)
    
    if state.stage == Stage.ONE_SENTENCE:
        state = workflow.stage_2_one_paragraph(state)
    
    if state.stage == Stage.ONE_PARAGRAPH:
        state = workflow.stage_3_character_sheets(state)
    
    if state.stage == Stage.CHARACTER_SHEETS:
        state = workflow.stage_4_four_page_outline(state)
    
    if state.stage == Stage.FOUR_PAGE_OUTLINE:
        state = workflow.stage_5_character_charts(state)
    
    if state.stage == Stage.CHARACTER_CHARTS:
        state = workflow.stage_6_scene_list(state)
    
    if state.stage == Stage.SCENE_LIST:
        state = workflow.stage_7_scene_descriptions(state)
    
    if state.stage == Stage.SCENE_DESCRIPTIONS:
        state = workflow.create_style_guide(state)
    
    state.stage = Stage.COMPLETE
    state.progress = 1.0
    save_checkpoint(state, checkpoint_id or "final")
    
    return state
