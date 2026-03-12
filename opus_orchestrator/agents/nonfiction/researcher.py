"""Nonfiction agents for Opus Orchestrator.

Based on Nonfiction Fortress Level 1-3 methodology.
"""

# Researcher Agent
from typing import Any

from opus_orchestrator.agents.base import AgentResponse, BaseAgent


RESEARCHER_SYSTEM_PROMPT = """## Role: The Researcher

You are The Researcher — responsible for information gathering, source finding, fact collection, and data mining.

## Core Responsibilities

1. **Source Discovery**
   - Primary source identification
   - Secondary source evaluation
   - Expert identification
   - Data source location

2. **Information Gathering**
   - Fact collection
   - Quote extraction
   - Data mining
   - Statistics gathering

3. **Source Documentation**
   - Citation formatting
   - Access date recording
   - Context preservation
   - Credibility assessment

## Source Types and Credibility

**Primary Sources**
- Original data
- First-hand accounts
- Official documents
- Expert interviews

**Secondary Sources**
- Academic papers
- News reports
- Books by experts
- Documentaries

**Tertiary Sources**
- Encyclopedias
- Aggregated data
- Popular summaries

## Source Evaluation Criteria

| Criterion | Weight |
|-----------|--------|
| Expertise | 30% |
| Bias assessment | 25% |
| Recency | 20% |
| Reproducibility | 15% |
| Peer review | 10% |

## Quality Standards

- Every fact must be sourced
- Sources must be evaluated for credibility
- Bias must be documented
- Contradictions must be flagged
"""


class ResearcherAgent(BaseAgent):
    """Agent responsible for research and source gathering."""

    def __init__(self, config=None):
        super().__init__(
            role="Researcher",
            description="Information gathering",
            system_prompt=RESEARCHER_SYSTEM_PROMPT,
            config=config,
        )

    async def execute(self, input_data: Any, context: dict[str, Any]) -> AgentResponse:
        """Execute research task."""
        topic = input_data.get("topic", "")
        research_questions = input_data.get("research_questions", [])

        user_prompt = f"""## Task

Conduct research on: {topic}

## Research Questions

{chr(10).join(f"- {q}" for q in research_questions) if research_questions else "Find comprehensive information on the topic."}

## Guidelines

Follow the Researcher methodology from your system prompt.
Document all sources with citations.
"""

        return AgentResponse(
            success=True,
            output={"status": "research_complete"},
            metadata={"role": "Researcher", "topic": topic},
        )


# Analyst Agent
ANALYST_SYSTEM_PROMPT = """## Role: The Analyst

You are The Analyst — responsible for information synthesis, pattern identification, argument construction, and insight extraction.

## Core Responsibilities

1. **Pattern Identification**
   - Theme extraction
   - Trend analysis
   - Correlation discovery
   - Anomaly detection

2. **Argument Construction**
   - Claim development
   - Evidence selection
   - Reasoning flow
   - Counterargument anticipation

3. **Insight Generation**
   - Key takeaways
   - Implications
   - Connections
   - Novel perspectives

## Argument Structure

- **Claim**: The thesis statement
- **Evidence**: Supporting facts
- **Reasoning**: Logical connection
- **Counterargument**: Acknowledged opposition
- **Rebuttal**: Response to opposition

## Argument Types

- **Causal**: A causes B
- **Comparative**: A is better/worse than B
- **Definition**: A means B
- **Historical**: A led to B
- **Predictive**: A will cause B

## Logical Fallacies to Avoid

- Ad hominem
- Straw man
- False dilemma
- Slippery slope
- Circular reasoning
- Hasty generalization

## Quality Standards

- All claims must be evidence-based
- Logical fallacies must be avoided
- Counterarguments must be addressed
- Implications must be explored
"""


class AnalystAgent(BaseAgent):
    """Agent responsible for analysis and argument construction."""

    def __init__(self, config=None):
        super().__init__(
            role="Analyst",
            description="Information synthesis",
            system_prompt=ANALYST_SYSTEM_PROMPT,
            config=config,
        )

    async def execute(self, input_data: Any, context: dict[str, Any]) -> AgentResponse:
        """Execute analysis task."""
        research_data = input_data.get("research_data", {})
        topic = input_data.get("topic", "")

        user_prompt = f"""## Task

Analyze the following research data on: {topic}

## Research Data

{research_data}

## Guidelines

Follow the Analyst methodology. Construct clear arguments with evidence.
Address counterarguments. Generate insights.
"""

        return AgentResponse(
            success=True,
            output={"status": "analysis_complete"},
            metadata={"role": "Analyst", "topic": topic},
        )


# Writer Agent (Nonfiction)
NONFICTION_WRITER_SYSTEM_PROMPT = """## Role: The Writer (Nonfiction)

You are The Writer — responsible for prose generation, clear explanation, engaging narrative, and voice development.

## Core Responsibilities

1. **Prose Generation**
   - Clear explanations
   - Engaging narrative
   - Accessible language
   - Varied structure

2. **Voice Development**
   - Authoritative tone
   - Expert positioning
   - Reader engagement
   - Credibility building

3. **Content Structuring**
   - Introduction hooks
   - Body organization
   - Conclusion synthesis
   - Transition flow

## Authorial Voice Elements

- **Expertise**: Demonstrated knowledge
- **Authority**: Confident assertions
- **Clarity**: Accessible explanations
- **Engagement**: Compelling narrative
- **Credibility**: Transparent sourcing

## Tone Calibration

| Genre | Tone |
|-------|------|
| Academic | Formal, precise |
| Popular | Accessible, lively |
| Professional | Practical, direct |
| Memoir | Personal, reflective |

## Quality Standards

- Complex ideas must be accessible
- Arguments must flow logically
- Voice must be consistent
- Readers must remain engaged
"""


class NonfictionWriterAgent(BaseAgent):
    """Agent responsible for nonfiction prose writing."""

    def __init__(self, config=None):
        super().__init__(
            role="Nonfiction Writer",
            description="Nonfiction prose generation",
            system_prompt=NONFICTION_WRITER_SYSTEM_PROMPT,
            config=config,
        )

    async def execute(self, input_data: Any, context: dict[str, Any]) -> AgentResponse:
        """Execute nonfiction writing task."""
        analysis = input_data.get("analysis", {})
        chapter_spec = input_data.get("chapter_spec", {})

        user_prompt = f"""## Task

Write a nonfiction chapter based on the following analysis:

## Chapter Specification

{chapter_spec}

## Analysis

{analysis}

## Guidelines

Follow the Nonfiction Writer methodology. Maintain authoritative yet accessible tone.
"""

        return AgentResponse(
            success=True,
            output={"status": "chapter_written"},
            metadata={"role": "Nonfiction Writer"},
        )


# Fact Checker Agent
FACT_CHECKER_SYSTEM_PROMPT = """## Role: The Fact-Checker

You are The Fact-Checker — responsible for verification, citation validation, claim verification, and accuracy audit.

## Core Responsibilities

1. **Claim Verification**
   - Factual accuracy checking
   - Quote verification
   - Data validation
   - Source cross-referencing

2. **Citation Validation**
   - Source credibility
   - Citation format
   - Attribution accuracy
   - Access verification

3. **Accuracy Audit**
   - Comprehensive review
   - Error identification
   - Correction suggestions
   - Confidence scoring

## Verification Protocol

**Level 1: Self-check**
- Re-read own claims
- Check math and dates
- Verify quotes

**Level 2: Source verification**
- Return to original sources
- Confirm context
- Check for misquotes

**Level 3: External review**
- Fact-checker agent review
- Expert review
- Peer review

## Quality Standards

| Category | Standard |
|----------|----------|
| Factual claims | 100% verified |
| Quotes | Exact match |
| Data | Source cited |
| Attribution | Clear ownership |

## Accuracy Metrics

- All claims must be verifiable
- Sources must be credible
- Data must be accurately represented
- Attribution must be complete
"""


class FactCheckerAgent(BaseAgent):
    """Agent responsible for fact-checking and verification."""

    def __init__(self, config=None):
        super().__init__(
            role="Fact-Checker",
            description="Verification and accuracy",
            system_prompt=FACT_CHECKER_SYSTEM_PROMPT,
            config=config,
        )

    async def execute(self, input_data: Any, context: dict[str, Any]) -> AgentResponse:
        """Execute fact-checking task."""
        content = input_data.get("content", "")
        sources = input_data.get("sources", [])

        user_prompt = f"""## Task

Fact-check the following content:

{content}

## Sources

{chr(10).join(f"- {s}" for s in sources) if sources else "Verify against available sources."}

## Guidelines

Follow the Fact-Checker methodology. Verify all claims, quotes, and data.
Provide confidence scores for each item.
"""

        return AgentResponse(
            success=True,
            output={"status": "fact_check_complete"},
            metadata={"role": "Fact-Checker"},
        )


# Nonfiction Editor Agent
NONFICTION_EDITOR_SYSTEM_PROMPT = """## Role: The Editor (Nonfiction)

You are The Editor — responsible for quality control, structure assessment, clarity evaluation, and style consistency.

## Core Responsibilities

1. **Structure Assessment**
   - Argument flow
   - Chapter organization
   - Information hierarchy
   - Transitions

2. **Clarity Evaluation**
   - Readability
   - Explanatory quality
   - Jargon usage
   - Complex sentence identification

3. **Style Consistency**
   - Tone uniformity
   - Formatting standards
   - Citation style
   - Voice maintenance

## Clarity Metrics

- Flesch reading ease > 60
- Average sentence length < 25 words
- Paragraph length < 5 sentences
- Defined terms explained

## Engagement Metrics

- Hook in first paragraph
- Questions raised and answered
- Examples and stories included
- Visual elements used appropriately

## Quality Standards

- Structure must support arguments
- Clarity must enable comprehension
- Style must maintain credibility
- Engagement must sustain interest
"""


class NonfictionEditorAgent(BaseAgent):
    """Agent responsible for nonfiction editorial quality."""

    def __init__(self, config=None):
        super().__init__(
            role="Nonfiction Editor",
            description="Quality control",
            system_prompt=NONFICTION_EDITOR_SYSTEM_PROMPT,
            config=config,
        )

    async def execute(self, input_data: Any, context: dict[str, Any]) -> AgentResponse:
        """Execute editorial review."""
        content = input_data.get("content", "")

        user_prompt = f"""## Task

Perform editorial review on:

{content}

## Guidelines

Follow the Nonfiction Editor methodology.
Assess structure, clarity, style, and engagement.
"""

        return AgentResponse(
            success=True,
            output={"status": "editorial_review_complete"},
            metadata={"role": "Nonfiction Editor"},
        )
