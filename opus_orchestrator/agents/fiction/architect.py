"""The Architect agent - Story structure and plot design.

From Fiction Fortress Level 1-3:
- Role: Story structure and plot design
- Responsibilities: Outlines, pacing, scene planning
- Output: Story blueprint
"""

from typing import Any, Optional

from opus_orchestrator.agents.base import AgentResponse, BaseAgent
from opus_orchestrator.schemas import BookBlueprint, ChapterBlueprint


ARCHITECT_SYSTEM_PROMPT = """## Role: The Architect

You are The Architect — the story's structural engineer. Your expertise lies in narrative architecture across all genres, and you excel at translating high-level concepts into detailed scene breakdowns.

## Core Responsibilities

1. **Story Structure Mastery**
   - Three-act structure application across genres
   - Beat-by-beat scene planning
   - Subplot integration techniques
   - Pacing analysis and adjustment

2. **Genre Expertise**
   - Mystery: Clue placement, red herring distribution, revelation timing
   - Romance: Beat sheet adaptation for relationship arcs
   - Thriller: Tension escalation curves, set-piece design
   - Fantasy/Sci-Fi: World-rule integration with plot beats

3. **Outline Generation**
   - Story spine creation (primal narrative in 3-5 sentences)
   - Chapter-level beat mapping
   - Scene purpose identification (whose story, what changes, why this scene)
   - Backstory weaving into present-tense narrative

4. **Conflict Architecture**
   - Internal vs. external conflict layering
   - Antagonist motivation design
   - Stakes escalation planning
   - Tension and release rhythm

## Quality Standards

- Each scene must advance plot, character, or theme (or multiple)
- Stakes must escalate through Acts I-II
- Midpoint must fundamentally shift protagonist's understanding
- All subplots must resolve by climax
- Every chapter needs a clear purpose and payoff

## Output Format

When generating a blueprint, include:
1. Story spine (primal narrative in 3-5 sentences)
2. Three-act breakdown with specific beats
3. Chapter-level outline (numbered chapters with one-line descriptions)
4. Scene list with purpose tags
5. Key plot points with word count allocations
6. Subplot integration notes
"""


class ArchitectAgent(BaseAgent):
    """Agent responsible for story structure and plot design."""

    def __init__(self, config=None):
        super().__init__(
            role="Architect",
            description="Story structure and plot design",
            system_prompt=ARCHITECT_SYSTEM_PROMPT,
            output_schema=BookBlueprint,
            config=config,
        )

    async def execute(self, input_data: Any, context: dict[str, Any]) -> AgentResponse:
        """Execute the Architect's task to generate a story blueprint.

        Args:
            input_data: Raw content + intent from the orchestrator
            context: Additional context (genre, themes, etc.)

        Returns:
            AgentResponse with BookBlueprint
        """
        raw_content = input_data.get("raw_content", "")
        intent = input_data.get("intent", {})
        genre = intent.get("genre", "general")
        target_word_count = intent.get("target_word_count", 80000)
        themes = intent.get("themes", [])

        user_prompt = f"""## Input Content

{raw_content}

## Requirements

- Genre: {genre}
- Target word count: {target_word_count}
- Themes to incorporate: {', '.join(themes) if themes else 'None specified'}
- Target audience: {intent.get('target_audience', 'General readers')}

## Task

Generate a complete story blueprint following the Architect's methodology.
Include all sections specified in your system prompt.

Be specific and detailed. The blueprint should be comprehensive enough that another agent could write each chapter from it.
"""

        try:
            # Call the LLM
            result = await self.call_llm(
                system_prompt=self.build_system_prompt(context),
                user_prompt=user_prompt,
            )

            return AgentResponse(
                success=True,
                output=result,
                metadata={
                    "role": "Architect",
                    "input_word_count": len(raw_content.split()),
                    "target_word_count": target_word_count,
                    "genre": genre,
                },
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                output=None,
                error=str(e),
                metadata={"role": "Architect"},
            )

    async def expand_chapter(
        self,
        chapter: ChapterBlueprint,
        full_blueprint: BookBlueprint,
        context: dict[str, Any],
    ) -> AgentResponse:
        """Expand a single chapter beat into detailed scene specification.

        From Template B in Fiction Fortress Level 2:
        - Scene ID, Act/Chapter location
        - POV character, Scene goal, Scene conflict, Scene outcome
        - Opening beat, Conflict beat, Turn beat, Ending beat
        """
        user_prompt = f"""## Chapter to Expand

- Chapter Number: {chapter.chapter_number}
- Title: {chapter.title}
- Summary: {chapter.summary}
- Word Count Target: {chapter.word_count_target}
- POV Character: {chapter.pov_character or 'Narrator'}
- Key Events: {', '.join(chapter.key_events)}

## Full Blueprint Context

- Book Title: {full_blueprint.title}
- Genre: {full_blueprint.genre}
- Overall Structure: {full_blueprint.structure}

## Task

Expand this chapter beat into a detailed scene specification following
Template B from the Fiction Fortress methodology.

Include:
1. Opening beat - how the scene opens
2. Conflict beat - what escalates tension
3. Turn beat - what changes the situation
4. Ending beat - what hook or change ends the scene

Be specific about character motivations, dialogue objectives, and emotional progression.
"""

        try:
            result = await self.call_llm(
                system_prompt=self.build_system_prompt(context),
                user_prompt=user_prompt,
            )

            return AgentResponse(
                success=True,
                output=result,
                metadata={"role": "Architect", "task": "chapter_expansion"},
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                output=None,
                error=str(e),
                metadata={"role": "Architect"},
            )
