"""Nonfiction submodule for Opus Orchestrator.

Key components:
- classifier: Classifies user input into ReaderPurpose
- intake: Conversational intake agent for high-fidelity intent
- content_infer: Infers purpose from existing blog/content
- critique_criteria: Purpose-specific evaluation criteria
- expanded_frameworks: 35+ expert-level frameworks
- research_integration: Connect research agent to pipeline
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
from opus_orchestrator.nonfiction.expanded_frameworks import (
    EXPANDED_FRAMEWORKS,
    FRAMEWORKS_BY_CATEGORY,
    get_frameworks_by_category,
    suggest_framework_for_book,
    get_total_framework_count,
)
from opus_orchestrator.nonfiction.research_integration import (
    ResearchIntegrator,
    ResearchRequest,
    ResearchResult,
    get_research_config_for_purpose,
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
    # Expanded Frameworks (35+)
    "EXPANDED_FRAMEWORKS",
    "FRAMEWORKS_BY_CATEGORY",
    "get_frameworks_by_category",
    "suggest_framework_for_book",
    "get_total_framework_count",
    # Research Integration
    "ResearchIntegrator",
    "ResearchRequest",
    "ResearchResult",
    "get_research_config_for_purpose",
]
