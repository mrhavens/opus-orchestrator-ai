"""The Editor agent - Quality control.

From Fiction Fortress Level 1-3:
- Role: Quality control
- Responsibilities: Continuity, pacing, quality checks
- Output: Editorial notes, revisions
"""

from typing import Any

from opus_orchestrator.agents.base import AgentResponse, BaseAgent


EDITOR_SYSTEM_PROMPT = """## Role: The Editor

You are The Editor — the quality control mechanism, identifying problems across all dimensions of the manuscript and directing revision.

## Core Responsibilities

1. **Continuity Verification**
   - Timeline consistency checking
   - Character knowledge tracking
   - Physical detail consistency (eye color, scars, clothing)
   - World-rule adherence verification

2. **Pacing Analysis**
   - Scene length distribution
   - Tension curve mapping
   - Reader fatigue prevention
   - Act break identification

3. **Quality Assessment**
   - Dialogue authenticity evaluation
   - Show vs. tell calibration
   - Emotional resonance verification
   - Prose quality grading

4. **Revision Direction**
   - Specific change identification
   - Priority sequencing (major vs. minor issues)
   - Revision scope definition
   - Polish vs. rewrite determination

## Supporting Capabilities

- Beta reader simulation
- Readability metrics interpretation
- Genre convention compliance
- Structural problem diagnosis

## Quality Metrics

| Check | Method |
|-------|--------|
| Pacing | Scene length analysis |
| Tension | Conflict per scene |
| Character consistency | Arc tracking |
| World consistency | Rule verification |
| Voice consistency | Prose sampling |

## Revision Priority Definitions

- **Major Revisions**: Structural issues, plot holes, character arc breaks
- **Minor Revisions**: Continuity errors, style inconsistencies, pacing tweaks
- **Polish**: Grammar, punctuation, word choice refinement

## Output Format

Provide your critique as a structured review with:
1. Overall score (0.0-1.0)
2. Strengths (list)
3. Weaknesses (list)
4. Specific revision suggestions (prioritized)
5. Final verdict: major_revisions / minor_revisions / approved
"""


class EditorAgent(BaseAgent):
    """Agent responsible for quality control and editorial direction."""

    def __init__(self, config=None):
        super().__init__(
            role="Editor",
            description="Quality control",
            system_prompt=EDITOR_SYSTEM_PROMPT,
            config=config,
        )

    async def execute(self, input_data: Any, context: dict[str, Any]) -> AgentResponse:
        """Execute the Editor's task to review content."""
        content = input_data.get("content", "")
        review_type = input_data.get("review_type", "full")

        user_prompt = f"""## Task

Perform a {review_type} editorial review on the following content:

{content}

## Review Type: {review_type}

## Guidelines

Follow the Editor methodology from your system prompt.
Be specific and actionable in your feedback.
Assign a clear revision priority.
"""

        try:
            result = await self.call_llm(
                system_prompt=self.build_system_prompt(context),
                user_prompt=user_prompt,
            )

            return AgentResponse(
                success=True,
                output=result,
                metadata={"role": "Editor", "review_type": review_type},
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                output=None,
                error=str(e),
                metadata={"role": "Editor"},
            )

    async def review_chapter(
        self,
        chapter: dict[str, Any],
        full_manuscript_context: dict[str, Any],
        context: dict[str, Any],
    ) -> AgentResponse:
        """Review a single chapter in full manuscript context."""
        user_prompt = f"""## Chapter to Review

- Chapter Number: {chapter.get('chapter_number')}
- Title: {chapter.get('title')}
- Content:

{chapter.get('content', '')}

## Full Manuscript Context

- Total Chapters: {full_manuscript_context.get('total_chapters', 0)}
- Book Title: {full_manuscript_context.get('title', 'Untitled')}
- Genre: {full_manuscript_context.get('genre', 'general')}

## Task

Perform a complete editorial review of this chapter, considering:
- Continuity with previous chapters
- Pacing within the chapter and in sequence
- Character consistency
- World-rule adherence
- Voice consistency
- Dialogue quality
- Show vs. tell balance

Provide:
1. Overall score (0.0-1.0)
2. Strengths (at least 3)
3. Weaknesses (at least 3)
4. Specific revision suggestions
5. Final verdict: major_revisions, minor_revisions, or approved
"""

        try:
            result = await self.call_llm(
                system_prompt=self.build_system_prompt(context),
                user_prompt=user_prompt,
            )

            # Try to extract score from result
            score = 0.5  # default
            for line in result.split('\n'):
                if 'score' in line.lower() or 'rating' in line.lower():
                    try:
                        # Look for number
                        import re
                        numbers = re.findall(r'0\.\d+|\d+\.\d+', line)
                        if numbers:
                            score = float(numbers[0])
                            break
                    except:
                        pass

            return AgentResponse(
                success=True,
                output={
                    "critique": result,
                    "score": score,
                    "chapter_number": chapter.get("chapter_number"),
                },
                metadata={"role": "Editor", "task": "chapter_review"},
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                output=None,
                error=str(e),
                metadata={"role": "Editor"},
            )

    async def generate_revision_notes(
        self,
        critiques: list[dict[str, Any]],
        context: dict[str, Any],
    ) -> AgentResponse:
        """Generate prioritized revision notes from multiple critiques."""
        critiques_text = "\n\n".join(f"### Critique {i+1}:\n{c.get('critique', str(c))}" for i, c in enumerate(critiques))

        user_prompt = f"""## Critiques to Synthesize

{critiques_text}

## Task

Synthesize these critiques into prioritized revision notes.
Group by:
1. Major revisions (structural, plot, arc issues) - must fix
2. Minor revisions (continuity, style, pacing) - should fix
3. Polish items (grammar, word choice) - nice to fix

For each item, provide specific, actionable feedback with location if possible.
"""

        try:
            result = await self.call_llm(
                system_prompt=self.build_system_prompt(context),
                user_prompt=user_prompt,
            )

            return AgentResponse(
                success=True,
                output=result,
                metadata={"role": "Editor", "critique_count": len(critiques)},
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                output=None,
                error=str(e),
                metadata={"role": "Editor"},
            )
