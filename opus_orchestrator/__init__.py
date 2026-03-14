"""Opus Orchestrator - AI Book Generation System.

Version: 0.2.0

Quick Start:
    opus generate --concept "Your book idea"
    opus serve --port 8000

For full documentation, see README.md
"""

# Lazy imports to avoid circular dependency on cold starts
# See: https://peps.python.org/pep-0562/
def __getattr__(name: str):
    """Lazy import for module-level attributes to break circular imports."""
    
    # Core exports
    if name == "OpusOrchestrator":
        from opus_orchestrator.orchestrator import OpusOrchestrator
        return OpusOrchestrator
    if name == "run_opus":
        from opus_orchestrator.langgraph_workflow import run_opus
        return run_opus
    if name == "OpusConfig":
        from opus_orchestrator.config import OpusConfig
        return OpusConfig
    if name == "get_config":
        from opus_orchestrator.config import get_config
        return get_config
    if name == "set_config":
        from opus_orchestrator.config import set_config
        return set_config
    if name == "OpusState":
        from opus_orchestrator.state import OpusState
        return OpusState
    if name == "NonfictionGenerator":
        from opus_orchestrator.nonfiction_generator import NonfictionGenerator
        return NonfictionGenerator
    if name == "OpusLogger":
        from opus_orchestrator.logging import OpusLogger
        return OpusLogger
    if name == "get_logger":
        from opus_orchestrator.logging import get_logger
        return get_logger
    
    # Frameworks
    if name == "StoryFramework":
        from opus_orchestrator.frameworks import StoryFramework
        return StoryFramework
    if name == "FRAMEWORKS":
        from opus_orchestrator.frameworks import FRAMEWORKS
        return FRAMEWORKS
    if name == "get_framework_for_genre":
        from opus_orchestrator.frameworks import get_framework_for_genre
        return get_framework_for_genre
    if name == "get_framework_prompt":
        from opus_orchestrator.frameworks import get_framework_prompt
        return get_framework_prompt
    
    # Schemas
    if name == "BookBlueprint":
        from opus_orchestrator.schemas import BookBlueprint
        return BookBlueprint
    if name == "BookIntent":
        from opus_orchestrator.schemas import BookIntent
        return BookIntent
    if name == "BookType":
        from opus_orchestrator.schemas import BookType
        return BookType
    if name == "Chapter":
        from opus_orchestrator.schemas import Chapter
        return Chapter
    if name == "ChapterBlueprint":
        from opus_orchestrator.schemas import ChapterBlueprint
        return ChapterBlueprint
    if name == "ChapterCritique":
        from opus_orchestrator.schemas import ChapterCritique
        return ChapterCritique
    if name == "ChapterDraft":
        from opus_orchestrator.schemas import ChapterDraft
        return ChapterDraft
    if name == "Manuscript":
        from opus_orchestrator.schemas import Manuscript
        return Manuscript
    if name == "RawContent":
        from opus_orchestrator.schemas import RawContent
        return RawContent
    
    # Utilities
    if name == "LLMClient":
        from opus_orchestrator.utils.llm import LLMClient
        return LLMClient
    if name == "get_llm_client":
        from opus_orchestrator.utils.llm import get_llm_client
        return get_llm_client
    if name == "RetryHandler":
        from opus_orchestrator.utils.retry import RetryHandler
        return RetryHandler
    if name == "CircuitBreaker":
        from opus_orchestrator.utils.retry import CircuitBreaker
        return CircuitBreaker
    if name == "with_retry":
        from opus_orchestrator.utils.retry import with_retry
        return with_retry
    
    # Scrivener Export
    if name == "ScrivenerExporter":
        from opus_orchestrator.scrivener_export import ScrivenerExporter
        return ScrivenerExporter
    if name == "export_to_scrivener":
        from opus_orchestrator.scrivener_export import export_to_scrivener
        return export_to_scrivener
    if name == "ExportOptions":
        from opus_orchestrator.scrivener_export import ExportOptions
        return ExportOptions
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__version__ = "0.2.0"

# Explicit __all__ for static analysis and IDE support
__all__ = [
    # Core
    "OpusOrchestrator",
    "OpusConfig",
    "get_config",
    "set_config",
    "OpusState",
    "NonfictionGenerator",
    "run_opus",
    # Logging
    "OpusLogger",
    "get_logger",
    # Frameworks
    "StoryFramework",
    "FRAMEWORKS",
    "get_framework_for_genre",
    "get_framework_prompt",
    # Schemas
    "BookBlueprint",
    "BookIntent",
    "BookType",
    "Chapter",
    "ChapterBlueprint",
    "ChapterCritique",
    "ChapterDraft",
    "Manuscript",
    "RawContent",
    # Utilities
    "LLMClient",
    "get_llm_client",
    "RetryHandler",
    "CircuitBreaker",
    "with_retry",
    # Scrivener Export
    "ScrivenerExporter",
    "export_to_scrivener",
    "ExportOptions",
    "ExportOptions",
]

def __getattr__(name):
    if name == "LaTeXExporter":
        from opus_orchestrator.latex_compile import LaTeXExporter
        return LaTeXExporter
    if name == "CompileOptions":
        from opus_orchestrator.latex_compile import CompileOptions
        return CompileOptions
    if name == "export_to_latex":
        from opus_orchestrator.latex_compile import export_to_latex
        return export_to_latex
    if name == "compile_pdf":
        from opus_orchestrator.latex_compile import compile_pdf
        return compile_pdf
    raise AttributeError(f"module has no attribute {name!r}")
