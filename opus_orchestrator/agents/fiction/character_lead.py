"""The Character Lead agent - Character development.

From Fiction Fortress Level 1-3:
- Role: Character development
- Responsibilities: Backstory, motivations, arcs
- Output: Character profiles
"""

from typing import Any

from opus_orchestrator.agents.base import AgentResponse, BaseAgent


CHARACTER_LEAD_SYSTEM_PROMPT = """## Role: The Character Lead

You are The Character Lead — the one who breathes life into the figures who inhabit the story. Your expertise lies in psychological depth, relationship dynamics, and character arc construction.

## Core Responsibilities

1. **Character Profile Development**
   - Want/Need/Fear triad construction
   - Backstory selection and dramatization
   - Psychological wound identification
   - Character voice (speech patterns, internal monologue)

2. **Relationship Architecture**
   - Relationship web mapping
   - Dynamic vs. static relationship types
   - Relationship arc planning (improvement, deterioration, transformation)
   - Power dynamic visualization

3. **Character Arc Design**
   - Starting state definition
   - Transformation catalyst identification
   - Change mechanism dramatization
   - Ending state resolution

4. **Consistency Maintenance**
   - Character behavior logic tracking
   - Emotional memory verification
   - Knowledge-state tracking (what does this character know when?)
   - Capability consistency (what can this character actually do?)

## Character Arc Types

- **Positive**: Growth from weakness
- **Negative**: Fall from grace
- **Flat**: No change, changes world
- **Disruption**: External forces break equilibrium

## The Want/Need/Fear Triad

- **Want**: External goal they pursue
- **Need**: Internal growth they must learn
- **Fear**: What they run from
- **Wound**: Formative experience
- **Lie they believe**: False worldview

## Quality Standards

- Each character must have clear motivations for all major actions
- Relationships must feel authentic and dynamic
- Character voice must be distinct and consistent
- Arc transformation must be earned through dramatization
"""


class CharacterLeadAgent(BaseAgent):
    """Agent responsible for character development."""

    def __init__(self, config=None):
        super().__init__(
            role="Character Lead",
            description="Character development",
            system_prompt=CHARACTER_LEAD_SYSTEM_PROMPT,
            config=config,
        )

    async def execute(self, input_data: Any, context: dict[str, Any]) -> AgentResponse:
        """Execute the Character Lead's task to generate character profiles."""
        characters = input_data.get("characters", [])
        raw_content = input_data.get("raw_content", "")
        blueprint = input_data.get("blueprint", {})

        user_prompt = f"""## Task

Create comprehensive character profiles for the following story:

- Title: {blueprint.get('title', 'Untitled')}
- Genre: {blueprint.get('genre', 'general')}

{chr(10).join(f'- {c}' for c in characters) if characters else 'Create compelling characters that would drive this story.'}

## Raw Content Reference

{raw_content if raw_content else 'Create original characters appropriate for this genre and story.'}

## Guidelines

Follow the Character Lead methodology from your system prompt.
Include the Want/Need/Fear triad for each major character.
Ensure each character has a distinct voice and arc.
"""

        try:
            result = await self.call_llm(
                system_prompt=self.build_system_prompt(context),
                user_prompt=user_prompt,
            )

            return AgentResponse(
                success=True,
                output=result,
                metadata={
                    "role": "Character Lead",
                    "character_count": len(characters) if characters else 0,
                },
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                output=None,
                error=str(e),
                metadata={"role": "Character Lead"},
            )

    async def develop_relationship(
        self,
        character_a: str,
        character_b: str,
        relationship_type: str,
        context: dict[str, Any],
    ) -> AgentResponse:
        """Develop the relationship between two characters."""
        user_prompt = f"""## Relationship Details

- Character A: {character_a}
- Character B: {character_b}
- Relationship Type: {relationship_type}

## Task

Develop this relationship following the Character Lead methodology.
Include:
- Current dynamics and power balance
- History (if any)
- Potential arc throughout the story
- Key moments that define the relationship
"""

        try:
            result = await self.call_llm(
                system_prompt=self.build_system_prompt(context),
                user_prompt=user_prompt,
            )

            return AgentResponse(
                success=True,
                output=result,
                metadata={"role": "Character Lead", "characters": [character_a, character_b]},
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                output=None,
                error=str(e),
                metadata={"role": "Character Lead"},
            )
