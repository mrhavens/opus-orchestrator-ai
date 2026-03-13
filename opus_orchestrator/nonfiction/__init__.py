"""Nonfiction submodule for Opus Orchestrator.

Key components:
- classifier: Classifies user input into ReaderPurpose
- intake: Conversational intake agent for high-fidelity intent
- content_infer: Infers purpose from existing blog/content
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
]
