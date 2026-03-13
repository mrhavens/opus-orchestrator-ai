"""Nonfiction submodule for Opus Orchestrator.

Key components:
- classifier: Classifies user input into ReaderPurpose
- intake: Conversational intake agent for high-fidelity intent
- content_infer: Infers purpose from existing blog/content
- critique_criteria: Purpose-specific evaluation criteria
"""

from opus_orchestrator.nonfiction.classifier import (
    PurposeClassifier,
    ClassificationResult,
    classify_purpose,
    ReaderPurpose,
)
from opus_orchestrator.nonfiction.intake import (
    IntakeAgent,
    IntakeInput,
    IntakeResult,
    IntakeMode,
    determine_intake,
)
from opus_orchestrator.nonfiction.content_infer import (
    ContentPurposeInferer,
    ContentAnalysis,
    infer_purpose_from_content,
)
from opus_orchestrator.nonfiction.critique_criteria import (
    CritiqueCriterion,
    CritiqueCriteriaSet,
    get_critique_criteria,
    evaluate_chapter,
    get_evaluation_prompt,
    list_all_criteria,
)

__all__ = [
    # Classifier
    "PurposeClassifier",
    "ClassificationResult", 
    "classify_purpose",
    "ReaderPurpose",
    # Intake Agent
    "IntakeAgent",
    "IntakeInput",
    "IntakeResult",
    "IntakeMode",
    "determine_intake",
    # Content Inference
    "ContentPurposeInferer",
    "ContentAnalysis",
    "infer_purpose_from_content",
    # Critique Criteria
    "CritiqueCriterion",
    "CritiqueCriteriaSet",
    "get_critique_criteria",
    "evaluate_chapter",
    "get_evaluation_prompt",
    "list_all_criteria",
]
