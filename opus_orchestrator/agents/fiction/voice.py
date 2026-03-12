"""The Voice agent - Prose style and tone.

From Fiction Fortress Level 1-3:
- Role: Prose style and tone
- Responsibilities: Sentence-level writing, voice consistency
- Output: Prose samples, style guide
"""

from typing import Any

from opus_orchestrator.agents.base import AgentResponse, BaseAgent


VOICE_SYSTEM_PROMPT = """## Role: The Voice

You are The Voice — the owner of the prose itself, the sound, rhythm, and texture of the language. Your expertise lies in maintaining consistent style across thousands of words while adapting to scene-specific demands.

## Core Responsibilities

1. **Prose Style Control**
   - Sentence rhythm variation (short/medium/long calibration)
   - Vocabulary level management
   - Figurative language deployment (metaphor, simile, symbolism density)
   - Point of view intimacy maintenance

2. **Voice Consistency**
   - Style guide creation and adherence
   - Word bank maintenance
   - Phrase pattern tracking
   - Tone range specification (warm/cool, dark/light, etc.)

3. **Scene-Type Adaptation**
   - Action scene pacing (sentence shortening)
   - Emotional scene density (sentence complexity)
   - Dialogue scene formatting
   - Descriptive scene rhythm
   - Exposition handling (invisible vs. visible)

4. **Point of View Management**
   - Deep POV techniques
   - Perspective consistency
   - Head-hopping prevention
   - Internal monologue integration

## Supporting Capabilities

- Dialogue attribution (said vs. action beats vs. no attribution)
- Punctuation style consistency
- Paragraph rhythm (white space management)
- Reader proximity calibration

## Voice Consistency Protocol

Maintain:
1. **Word bank** - Preferred vocabulary
2. **Phrase patterns** - Recurring constructions
3. **Rhythm map** - Sentence length distribution
4. **Tone guide** - Emotional range

## Quality Standards

- Voice must remain consistent across entire manuscript
- Scene type must inform prose style
- POV must be maintained without head-hopping
- Dialogue must sound distinct for each character
"""


class VoiceAgent(BaseAgent):
    """Agent responsible for prose style and voice consistency."""

    def __init__(self, config=None):
        super().__init__(
            role="Voice",
            description="Prose style and tone",
            system_prompt=VOICE_SYSTEM_PROMPT,
            config=config,
        )

    async def execute(self, input_data: Any, context: dict[str, Any]) -> AgentResponse:
        """Execute the Voice agent's task to create style guide and samples.

        Args:
            input_data: Genre, tone, target audience
            context: Additional context

        Returns:
            AgentResponse with style guide and prose samples
        """
        genre = input_data.get("genre", "general")
        tone = input_data.get("tone", "neutral")

        user_prompt = f"""## Task

Create a voice/style guide and prose samples for:

- Genre: {genre}
- Tone: {tone}
- Target Audience: {input_data.get('target_audience', 'General readers')}

## Guidelines

Follow the Voice agent methodology from your system prompt.
Include:
- Word bank
- Phrase patterns
- Rhythm map
- Tone guide
- 3 sample scenes (opening, dialogue, descriptive)
"""

        return AgentResponse(
            success=True,
            output={"status": "voice_created"},
            metadata={"role": "Voice", "genre": genre, "tone": tone},
        )

    async def write_chapter(
        self,
        chapter_spec: dict[str, Any],
        style_guide: dict[str, Any],
        context: dict[str, Any],
    ) -> AgentResponse:
        """Write a complete chapter following the style guide.

        This is the main writing task for the Voice agent.
        """
        user_prompt = f"""## Chapter Specification

- Chapter Number: {chapter_spec.get('chapter_number')}
- Title: {chapter_spec.get('title')}
- Summary: {chapter_spec.get('summary')}
- Word Count Target: {chapter_spec.get('word_count_target')}
- POV Character: {chapter_spec.get('pov_character', 'Narrator')}
- Key Events: {', '.join(chapter_spec.get('key_events', []))}

## Style Guide

{style_guide}

## Task

Write the complete chapter following the style guide and chapter specification.
Maintain consistent voice throughout.
"""

        return AgentResponse(
            success=True,
            output={
                "status": "chapter_written",
                "chapter_number": chapter_spec.get("chapter_number"),
            },
            metadata={"role": "Voice"},
        )

    async def polish_chapter(
        self,
        chapter_content: str,
        style_guide: dict[str, Any],
        context: dict[str, Any],
    ) -> AgentResponse:
        """Polish an existing chapter for voice consistency."""
        user_prompt = f"""## Chapter to Polish

{chapter_content}

## Style Guide

{style_guide}

## Task

Polish this chapter for voice consistency. Ensure:
- Sentence rhythm varies appropriately
- Word choice matches the style guide
- Tone remains consistent
- POV is maintained
- Prose flows smoothly
"""

        return AgentResponse(
            success=True,
            output={"status": "chapter_polished"},
            metadata={"role": "Voice", "task": "polish"},
        )
