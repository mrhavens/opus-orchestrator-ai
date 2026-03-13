"""Nonfiction submodule for Opus Orchestrator.

Key components:
- classifier: Classifies user input into ReaderPurpose
"""

from opus_orchestrator.nonfiction.classifier import (
    PurposeClassifier,
    ClassificationResult,
    classify_purpose,
    ReaderPurpose,
)

__all__ = [
    "PurposeClassifier",
    "ClassificationResult", 
    "classify_purpose",
    "ReaderPurpose",
]
