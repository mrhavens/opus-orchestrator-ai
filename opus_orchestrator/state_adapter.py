"""Unified State Adapter for Opus Orchestrator.

Provides adapters between OpusState and OpusGraphState to unify
the two state systems.
"""

from typing import Any, Optional

from opus_orchestrator.state import OpusState
from opus_orchestrator.langgraph_state import OpusGraphState


class StateAdapter:
    """Adapter to convert between OpusState and OpusGraphState."""
    
    @staticmethod
    def opus_to_graph(opus_state: OpusState) -> dict[str, Any]:
        """Convert OpusState to dict for OpusGraphState.
        
        Args:
            opus_state: The OpusState to convert
            
        Returns:
            Dict suitable for creating OpusGraphState
        """
        # Extract pre-writing data if available
        prewriting_data = {}
        
        if opus_state.blueprint:
            prewriting_data = {
                "one_sentence": opus_state.blueprint.title,  # Approximate
                "one_paragraph": opus_state.blueprint.subtitle or "",
            }
        
        return {
            "seed_concept": opus_state.raw_content.text[:500] if opus_state.raw_content else "",
            "framework": "snowflake",
            "genre": opus_state.intent.genre if opus_state.intent else "general",
            "target_word_count": opus_state.intent.target_word_count if opus_state.intent else 80000,
            "prewriting": prewriting_data,
        }
    
    @staticmethod
    def graph_to_opus(graph_state: OpusGraphState) -> OpusState:
        """Convert OpusGraphState back to OpusState.
        
        This is lossy - only preserves key fields.
        
        Args:
            graph_state: The OpusGraphState to convert
            
        Returns:
            OpusState with available data
        """
        from opus_orchestrator.schemas import BookIntent, BookType
        
        intent = BookIntent(
            book_type=BookType.FICTION,
            genre=graph_state.genre,
            target_word_count=graph_state.target_word_count,
            target_audience="general readers",
            intended_outcome="complete novel",
        )
        
        opus_state = OpusState(
            intent=intent,
            current_stage=graph_state.stage.value,
            progress=graph_state.progress,
        )
        
        # Add manuscript if available
        if graph_state.manuscript:
            from opus_orchestrator.schemas import Manuscript, Chapter
            chapters = []
            for i, ch_state in graph_state.chapters.items():
                chapters.append(Chapter(
                    chapter_number=i,
                    title=ch_state.content[:50],
                    content=ch_state.content,
                    word_count=ch_state.word_count,
                ))
            
            opus_state.manuscript = Manuscript(
                title="Untitled",
                book_type=BookType.FICTION,
                genre=graph_state.genre,
                chapters=chapters,
                total_word_count=graph_state.total_word_count,
            )
        
        return opus_state
    
    @staticmethod
    def create_unified_state(
        seed_concept: str,
        framework: str = "snowflake",
        genre: str = "general",
        target_word_count: int = 80000,
    ) -> dict[str, Any]:
        """Create initial state dict that works for both systems.
        
        Args:
            seed_concept: The seed concept for the book
            framework: Story framework to use
            genre: Genre of the book
            target_word_count: Target word count
            
        Returns:
            Dict that can initialize either state model
        """
        return {
            # Common fields
            "seed_concept": seed_concept,
            "framework": framework,
            "genre": genre,
            "target_word_count": target_word_count,
            # For OpusState compatibility
            "repo_url": None,
            "intent": None,
            "raw_content": None,
            # For OpusGraphState compatibility
            "prewriting": {},
            "style_guide": "",
            "current_chapter": 0,
            "chapters": {},
            "manuscript": "",
            "total_word_count": 0,
            "use_autogen": True,
            "critique_iterations": {},
            "validation_errors": [],
            "warnings": [],
            "progress": 0.0,
            "messages": [],
        }
