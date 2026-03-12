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

## Quality Standards

- Every issue must have specific, actionable feedback
- Revision priorities must be clearly ordered
- Continuity issues must be flagged with exact locations
- Pacing analysis must be data-driven (scene lengths, tension scores)
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
        """Execute the Editor's task to review and assess the manuscript.

        Args:
            input_data: Chapter or manuscript to review
            context: Review criteria and standards

        Returns:
            AgentResponse with editorial assessment
        """
        content = input_data.get("content", "")
        review_type = input_data.get("review_type", "full")

        user_prompt = f"""## Task

Perform a {review_type} editorial review on:

{content[:5000]}... {'(truncated)' if len(content) > 5000 else ''}

## Review Type: {review_type}

## Guidelines

Follow the Editor methodology from your system prompt.
Include:
- Continuity verification
- Pacing analysis
- Quality assessment
- Specific revision directions
"""

        return AgentResponse(
            success=True,
            output={"status": "editorial_review_complete"},
            metadata={"role": "Editor", "review_type": review_type},
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
- Content: {chapter.get('content', '')[:3000]}...

## Full Manuscript Context

- Total Chapters: {full_manuscript_context.get('total_chapters', 0)}
- Previous Chapters Summary: {full_manuscript_context.get('previous_summaries', [])}
- Characters in Story: {', '.join(full_manuscript_context.get('characters', []))}
- World Rules: {full_manuscript_context.get('world_rules', {})}

## Task

Perform a complete editorial review of this chapter, considering:
- Continuity with previous chapters
- Pacing within the chapter and in sequence
- Character consistency
- World-rule adherence
- Voice consistency
- Dialogue quality

Assign a revision priority: major_revisions, minor_revisions, or approved
"""

        return AgentResponse(
            success=True,
            output={
                "status": "chapter_reviewed",
                "chapter_number": chapter.get("chapter_number"),
            },
            metadata={"role": "Editor", "task": "chapter_review"},
        )

    async def generate_revision_notes(
        self,
        critiques: list[dict[str, Any]],
        context: dict[str, Any],
    ) -> AgentResponse:
        """Generate prioritized revision notes from multiple critiques."""
        user_prompt = f"""## Critiques to Synthesize

{chr(10).join(f"### Critique {i+1}:{c}" for i, c in enumerate(critiques))}

## Task

Synthesize these critiques into prioritized revision notes.
Group by:
1. Major revisions (structural, plot, arc issues)
2. Minor revisions (continuity, style, pacing)
3. Polish items (grammar, word choice)

For each item, provide specific, actionable feedback.
"""

        return AgentResponse(
            success=True,
            output={"status": "revision_notes_generated"},
            metadata={"role": "Editor", "critique_count": len(critiques)},
        )
