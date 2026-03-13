"""Nonfiction submodule for Opus Orchestrator.

Key components:
- classifier: Classifies user input into ReaderPurpose
- intake: Conversational intake agent for high-fidelity intent
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
]
