"""Purpose-Based Critique Criteria.

Different evaluation criteria for different reader purposes.
A tutorial is evaluated differently from a memoir.
"""

from dataclasses import dataclass
from typing import Optional

from opus_orchestrator.nonfiction import ReaderPurpose


@dataclass
class CritiqueCriterion:
    """A single criterion for evaluation."""
    name: str
    description: str
    weight: float  # 0.0 to 1.0
    questions: list[str]


@dataclass
class CritiqueCriteriaSet:
    """Complete set of criteria for a purpose."""
    purpose: ReaderPurpose
    criteria: list[CritiqueCriterion]
    overall_questions: list[str]
    pass_threshold: float = 0.7


# =============================================================================
# CRITERIA BY PURPOSE
# =============================================================================

TUTORIAL_CRITERIA = CritiqueCriteriaSet(
    purpose=ReaderPurpose.LEARN_HANDS_ON,
    criteria=[
        CritiqueCriterion(
            name="Clarity",
            description="Can a beginner understand each step?",
            weight=0.30,
            questions=[
                "Is each step explained clearly enough for a beginner?",
                "Are there any ambiguous instructions?",
                "Could someone with no prior knowledge complete this?",
            ],
        ),
        CritiqueCriterion(
            name="Completeness",
            description="Are all prerequisites and steps covered?",
            weight=0.25,
            questions=[
                "Are all prerequisites listed?",
                "Is anything missing that the reader would need?",
                "Are there gaps in the instructions?",
            ],
        ),
        CritiqueCriterion(
            name="Progressiveness",
            description="Does complexity build gradually?",
            weight=0.20,
            questions=[
                "Does each step build on the previous?",
                "Is there too much complexity too soon?",
                "Are advanced topics introduced appropriately?",
            ],
        ),
        CritiqueCriterion(
            name="Actionability",
            description="Can reader immediately apply what they learned?",
            weight=0.15,
            questions=[
                "Can the reader try this right now?",
                "Are there exercises or practice opportunities?",
                "Is there enough hand-holding for beginners?",
            ],
        ),
        CritiqueCriterion(
            name="Error Prevention",
            description="Are common mistakes addressed?",
            weight=0.10,
            questions=[
                "Are common pitfalls mentioned?",
                "Is there troubleshooting guidance?",
                "Does the writer anticipate reader mistakes?",
            ],
        ),
    ],
    overall_questions=[
        "Can a complete beginner actually complete this tutorial?",
        "Are the steps in the right order?",
        "Is the pacing appropriate for learning?",
    ],
    pass_threshold=0.70,
)


EXPLAINER_CRITERIA = CritiqueCriteriaSet(
    purpose=ReaderPurpose.UNDERSTAND,
    criteria=[
        CritiqueCriterion(
            name="Analogy Quality",
            description="Do analogies make complex ideas click?",
            weight=0.25,
            questions=[
                "Are there vivid, memorable analogies?",
                "Do the analogies actually clarify the concept?",
                "Are there enough analogies for different learning styles?",
            ],
        ),
        CritiqueCriterion(
            name="Examples",
            description="Are there diverse, clear examples?",
            weight=0.25,
            questions=[
                "Are there multiple examples?",
                "Do examples cover different scenarios?",
                "Are the examples relevant to the target audience?",
            ],
        ),
        CritiqueCriterion(
            name="Mental Model",
            description="Does reader leave with a useful framework?",
            weight=0.20,
            questions=[
                "Can the reader explain this to someone else?",
                "Do they have a framework for thinking about this?",
                "Is there a key insight they'll remember?",
            ],
        ),
        CritiqueCriterion(
            name="Depth",
            description="Is there surface AND depth?",
            weight=0.15,
            questions=[
                "Does this go beyond the obvious?",
                "Is there nuance and complexity acknowledged?",
                "Can beginners and intermediates both learn?",
            ],
        ),
        CritiqueCriterion(
            name="Misconceptions",
            description="Are wrong views addressed?",
            weight=0.15,
            questions=[
                "Does the writer address common misconceptions?",
                "Is it clear what this is NOT?",
                "Are there counterexamples?",
            ],
        ),
    ],
    overall_questions=[
        "Would a reader understand this deeply after reading?",
        "Do the analogies make sense?",
        "Is there enough depth without being overwhelming?",
    ],
    pass_threshold=0.70,
)


TRANSFORMATION_CRITERIA = CritiqueCriteriaSet(
    purpose=ReaderPurpose.TRANSFORM,
    criteria=[
        CritiqueCriterion(
            name="Emotional Honesty",
            description="Does it include real struggles, not just success?",
            weight=0.30,
            questions=[
                "Are the hard parts included?",
                "Does it acknowledge that transformation is hard?",
                "Is there vulnerability, not just triumph?",
            ],
        ),
        CritiqueCriterion(
            name="Relatability",
            description="Would the target reader see themselves?",
            weight=0.25,
            questions=[
                "Would someone in the target situation recognize themselves?",
                "Is the struggle described vividly enough?",
                "Does the reader feel understood?",
            ],
        ),
        CritiqueCriterion(
            name="Hope",
            description="Does it build hope without false promises?",
            weight=0.20,
            questions=[
                "Does this inspire hope?",
                "Is the hope realistic?",
                "Would a cynic roll their eyes?",
            ],
        ),
        CritiqueCriterion(
            name="Specificity",
            description="Are there concrete details (names, moments)?",
            weight=0.15,
            questions=[
                "Are there specific, vivid details?",
                "Does it avoid generic advice?",
                "Are there real stories, not just concepts?",
            ],
        ),
        CritiqueCriterion(
            name="Actionability",
            description="Are there specific steps to start?",
            weight=0.10,
            questions=[
                "Does the reader know how to start?",
                "Are the first steps concrete?",
                "Is there something they can do tomorrow?",
            ],
        ),
    ],
    overall_questions=[
        "Would this actually inspire someone to change?",
        "Is it emotionally honest?",
        "Does it feel authentic?",
    ],
    pass_threshold=0.70,
)


DECIDE_CRITERIA = CritiqueCriteriaSet(
    purpose=ReaderPurpose.DECIDE,
    criteria=[
        CritiqueCriterion(
            name="Evidence Quality",
            description="Are claims backed by data/studies?",
            weight=0.30,
            questions=[
                "Are there credible sources?",
                "Is the evidence sufficient?",
                "Are statistics used appropriately?",
            ],
        ),
        CritiqueCriterion(
            name="Balance",
            description="Are counterarguments addressed fairly?",
            weight=0.25,
            questions=[
                "Does the writer acknowledge other perspectives?",
                "Is it biased or fair?",
                "Are the tradeoffs explored?",
            ],
        ),
        CritiqueCriterion(
            name="Credibility",
            description="Are sources trustworthy?",
            weight=0.20,
            questions=[
                "Would an expert trust this?",
                "Are sources credible?",
                "Is there any misleading information?",
            ],
        ),
        CritiqueCriterion(
            name="Clarity",
            description="Is the recommendation clear?",
            weight=0.15,
            questions=[
                "Does the reader know what to decide?",
                "Is the conclusion clear?",
                "Is there ambiguity that could confuse?",
            ],
        ),
        CritiqueCriterion(
            name="Completeness",
            description="Are all relevant factors considered?",
            weight=0.10,
            questions=[
                "Is anything important missing?",
                "Are all sides represented?",
                "Would the reader need additional research?",
            ],
        ),
    ],
    overall_questions=[
        "Can the reader make an informed decision after reading?",
        "Is the evidence convincing?",
        "Are all perspectives represented fairly?",
    ],
    pass_threshold=0.75,
)


REFERENCE_CRITERIA = CritiqueCriteriaSet(
    purpose=ReaderPurpose.REFERENCE,
    criteria=[
        CritiqueCriterion(
            name="Accuracy",
            description="Is all information correct?",
            weight=0.35,
            questions=[
                "Is everything factually correct?",
                "Are there any errors?",
                "Would an expert approve this?",
            ],
        ),
        CritiqueCriterion(
            name="Completeness",
            description="Is nothing important missing?",
            weight=0.30,
            questions=[
                "Is this comprehensive?",
                "Are there obvious gaps?",
                "Would someone need another source?",
            ],
        ),
        CritiqueCriterion(
            name="Organization",
            description="Is it easy to find things?",
            weight=0.20,
            questions=[
                "Is the structure logical?",
                "Can you find what you need quickly?",
                "Is there a good index/table of contents?",
            ],
        ),
        CritiqueCriterion(
            name="Examples",
            description="Are there enough examples?",
            weight=0.15,
            questions=[
                "Is every concept illustrated with an example?",
                "Are the examples clear?",
                "Do they cover edge cases?",
            ],
        ),
    ],
    overall_questions=[
        "Is this a definitive reference?",
        "Would someone need another book after this?",
        "Is everything accurate and complete?",
    ],
    pass_threshold=0.85,
)


INSPIRED_CRITERIA = CritiqueCriteriaSet(
    purpose=ReaderPurpose.BE_INSPIRED,
    criteria=[
        CritiqueCriterion(
            name="Emotional Impact",
            description="Does it move the reader emotionally?",
            weight=0.30,
            questions=[
                "Does this inspire?",
                "Would readers feel something?",
                "Is there passion and authenticity?",
            ],
        ),
        CritiqueCriterion(
            name="Vision",
            description="Is there a vivid picture of what's possible?",
            weight=0.25,
            questions=[
                "Does it paint a compelling vision?",
                "Can the reader see themselves in the story?",
                "Is there something to aspire to?",
            ],
        ),
        CritiqueCriterion(
            name="Authenticity",
            description="Does it feel real, not manufactured?",
            weight=0.25,
            questions=[
                "Is this genuine or performative?",
                "Does the writer have credibility?",
                "Would a cynic be moved?",
            ],
        ),
        CritiqueCriterion(
            name="Story Quality",
            description="Is it a compelling narrative?",
            weight=0.20,
            questions=[
                "Is it a good story?",
                "Are there memorable moments?",
                "Does it have a satisfying arc?",
            ],
        ),
    ],
    overall_questions=[
        "Would this inspire someone to act?",
        "Is it emotionally resonant?",
        "Would this change someone's life?",
    ],
    pass_threshold=0.70,
)


# =============================================================================
# REGISTRY
# =============================================================================

PURPOSE_CRITERIA = {
    ReaderPurpose.LEARN_HANDS_ON: TUTORIAL_CRITERIA,
    ReaderPurpose.UNDERSTAND: EXPLAINER_CRITERIA,
    ReaderPurpose.TRANSFORM: TRANSFORMATION_CRITERIA,
    ReaderPurpose.DECIDE: DECIDE_CRITERIA,
    ReaderPurpose.REFERENCE: REFERENCE_CRITERIA,
    ReaderPurpose.BE_INSPIRED: INSPIRED_CRITERIA,
}


# =============================================================================
# FUNCTIONS
# =============================================================================

def get_critique_criteria(purpose: ReaderPurpose) -> CritiqueCriteriaSet:
    """Get the critique criteria for a purpose.
    
    Args:
        purpose: The reader purpose
        
    Returns:
        CritiqueCriteriaSet with criteria and questions
    """
    return PURPOSE_CRITERIA.get(purpose, EXPLAINER_CRITERIA)


def evaluate_chapter(
    chapter_content: str,
    purpose: ReaderPurpose,
    chapter_number: int = 1,
) -> dict:
    """Evaluate a chapter against purpose-specific criteria.
    
    This would typically be called by an LLM with the criteria.
    
    Args:
        chapter_content: The chapter text
        purpose: The reader purpose
        chapter_number: Which chapter
        
    Returns:
        Dict with scores for each criterion
    """
    criteria_set = get_critique_criteria(purpose)
    
    # This would be expanded to actually evaluate using LLM
    return {
        "purpose": purpose.value,
        "criteria_set": criteria_set.purpose.value,
        "criteria": [
            {"name": c.name, "weight": c.weight}
            for c in criteria_set.criteria
        ],
        "overall_questions": criteria_set.overall_questions,
        "pass_threshold": criteria_set.pass_threshold,
        "note": "LLM evaluation would fill in actual scores",
    }


def get_evaluation_prompt(
    chapter_content: str,
    purpose: ReaderPurpose,
) -> str:
    """Generate an LLM prompt for purpose-specific evaluation.
    
    Args:
        chapter_content: The chapter to evaluate
        purpose: The reader purpose
        
    Returns:
        A prompt for the LLM to evaluate the chapter
    """
    criteria_set = get_critique_criteria(purpose)
    
    criteria_text = "\n".join([
        f"- **{c.name}** ({c.weight*100:.0f}%): {c.description}"
        for c in criteria_set.criteria
    ])
    
    questions_text = "\n".join([
        f"- {q}"
        for q in criteria_set.overall_questions
    ])
    
    prompt = f"""Evaluate this chapter for a {purpose.value} book.

CRITERIA (score each 0-10):
{criteria_text}

OVERALL QUESTIONS (answer these):
{questions_text}

Chapter to evaluate:
---
{chapter_content[:2000]}...
---

Return your evaluation as JSON:
{{
    "scores": {{
        "criterion_name": score,
        ...
    }},
    "overall_score": 0-10,
    "pass": true/false,
    "strengths": ["..."],
    "weaknesses": ["..."],
    "recommendations": ["..."]
}}
"""
    return prompt


def list_all_criteria() -> dict:
    """List all criteria sets by purpose.
    
    Returns:
        Dict of purpose -> criteria info
    """
    return {
        purpose.value: {
            "name": criteria.purpose.name,
            "criteria_count": len(criteria.criteria),
            "pass_threshold": criteria.pass_threshold,
            "criteria": [c.name for c in criteria.criteria],
        }
        for purpose, criteria in PURPOSE_CRITERIA.items()
    }
