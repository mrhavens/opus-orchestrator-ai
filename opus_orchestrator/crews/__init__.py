"""Opus Orchestrator Crews.

CrewAI-powered crews for fiction and nonfiction book generation.
"""

from opus_orchestrator.crews.base_crew import OpusCrew
from opus_orchestrator.crews.fiction_crew import FictionCrew, create_fiction_crew
from opus_orchestrator.crews.nonfiction_crew import NonfictionCrew, create_nonfiction_crew

__all__ = [
    "OpusCrew",
    "FictionCrew",
    "NonfictionCrew",
    "create_fiction_crew",
    "create_nonfiction_crew",
]
