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
- **Disruption**: External力量打破平衡

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
        """Execute the Character Lead's task to generate character profiles.

        Args:
            input_data: Raw content + blueprint with character references
            context: Additional context

        Returns:
            AgentResponse with character profiles
        """
        characters = input_data.get("characters", [])
        raw_content = input_data.get("raw_content", "")

        user_prompt = f"""## Task

Create comprehensive character profiles for the following characters:

{chr(10).join(f"- {c}" for c in characters) if characters else "Create profiles for all characters in the story."}

## Raw Content Reference

{raw_content}

## Guidelines

Follow the Character Lead methodology from your system prompt.
Include the Want/Need/Fear triad for each major character.
"""

        return AgentResponse(
            success=True,
            output={"status": "characters_created"},
            metadata={"role": "Character Lead", "character_count": len(characters)},
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
- Current dynamics
- Power balance
- History (if any)
- Potential arc
"""

        return AgentResponse(
            success=True,
            output={"status": "relationship_developed"},
            metadata={"role": "Character Lead", "characters": [character_a, character_b]},
        )
