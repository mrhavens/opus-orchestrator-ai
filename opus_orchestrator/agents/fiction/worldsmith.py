"""The Worldsmith agent - Setting and world-building.

From Fiction Fortress Level 1-3:
- Role: Setting and world-building
- Responsibilities: Locations, cultures, technology, history
- Output: World bible
"""

from typing import Any

from opus_orchestrator.agents.base import AgentResponse, BaseAgent


WORLDSMITH_SYSTEM_PROMPT = """## Role: The Worldsmith

You are The Worldsmith — the creator of the stage upon which characters act. Your expertise lies in generating internally consistent settings that enhance rather than distract from the narrative.

## Core Responsibilities

1. **World-Building Frameworks**
   - ICE Method implementation (Internal Consistency, Cultural Depth, Environmental Detail)
   - Magic/technology system design with explicit rules
   - Political and economic system creation
   - Historical timeline construction

2. **Geographic Design**
   - Climate-driven ecology
   - Settlement placement rationale
   - Transportation and trade route logic
   - Territorial conflict origins

3. **Cultural Creation**
   - Belief system development (religion, philosophy, mythology)
   - Language patterns (without inventing full languages)
   - Social hierarchy construction
   - Daily life visualization (food, clothing, housing, work)

4. **World Document Generation**
   - Scalable detail (novel-length vs. short story)
   - Referenceable format for other agents
   - Searchable information architecture
   - Consistency tracking across documents

## The ICE Method

- **Internal Consistency**: Rules of magic/technology, geography, social structures, economics
- **Cultural Depth**: History, mythology, language patterns, beliefs, daily life
- **Environmental Detail**: Sensory descriptions, ecology, architecture, clothing, food

## Quality Standards

- All elements must be internally consistent
- Details must support story needs
- Cultural elements must have logical origins
- History must create present conflicts

## Output Structure

For each world element, include:
- Geography with climate and natural resources
- History with pivotal events
- Cultures with beliefs, customs, appearance
- Politics with power structures
- Economics with trade and class
- Daily life details
- Rules (for magic/technology)
"""


class WorldsmithAgent(BaseAgent):
    """Agent responsible for world-building and setting creation."""

    def __init__(self, config=None):
        super().__init__(
            role="Worldsmith",
            description="Setting and world-building",
            system_prompt=WORLDSMITH_SYSTEM_PROMPT,
            config=config,
        )

    async def execute(self, input_data: Any, context: dict[str, Any]) -> AgentResponse:
        """Execute the Worldsmith's task to generate world documents."""
        blueprint = input_data.get("blueprint", {})
        genre = input_data.get("genre", "fantasy")
        setting_type = input_data.get("setting_type", "fantasy")
        raw_content = input_data.get("raw_content", "")

        user_prompt = f"""## Task

Create a comprehensive world bible for the following story:

- Genre: {genre}
- Setting Type: {setting_type}
- Story Title: {blueprint.get('title', 'Untitled')}

## Guidelines

Follow the ICE Method and output structure from your system prompt.
Ensure all elements are internally consistent and support the story.

## Content Seed

{raw_content if raw_content else 'Create an original world that would support a compelling story in this genre.'}
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
                    "role": "Worldsmith",
                    "genre": genre,
                    "setting_type": setting_type,
                },
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                output=None,
                error=str(e),
                metadata={"role": "Worldsmith"},
            )

    async def expand_location(
        self,
        location_name: str,
        story_relevance: str,
        tone: str,
        pov_character: str,
        context: dict[str, Any],
    ) -> AgentResponse:
        """Generate detailed location description."""
        user_prompt = f"""## Location Details

- Location Name: {location_name}
- Story Relevance: {story_relevance}
- Tone Needed: {tone}
- POV Character: {pov_character}

## Task

Generate a 300-600 word location description following the Fiction Fortress methodology.
Include sensory details (visual, auditory, olfactory, tactile).
Make it atmospheric and story-relevant.
"""

        try:
            result = await self.call_llm(
                system_prompt=self.build_system_prompt(context),
                user_prompt=user_prompt,
            )

            return AgentResponse(
                success=True,
                output=result,
                metadata={"role": "Worldsmith", "location": location_name},
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                output=None,
                error=str(e),
                metadata={"role": "Worldsmith"},
            )
