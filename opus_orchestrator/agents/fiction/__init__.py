"""Fiction agents for Opus Orchestrator.

Based on Fiction Fortress Level 1-3 methodology.
"""

from opus_orchestrator.agents.fiction.architect import ArchitectAgent
from opus_orchestrator.agents.fiction.character_lead import CharacterLeadAgent
from opus_orchestrator.agents.fiction.editor import EditorAgent
from opus_orchestrator.agents.fiction.voice import VoiceAgent
from opus_orchestrator.agents.fiction.worldsmith import WorldsmithAgent

__all__ = [
    "ArchitectAgent",
    "CharacterLeadAgent",
    "EditorAgent",
    "VoiceAgent",
    "WorldsmithAgent",
]
